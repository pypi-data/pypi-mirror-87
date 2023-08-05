import asyncio
import logging
import re
import socket
import warnings

from asyncio import AbstractEventLoop
from ipaddress import ip_address, IPv4Network

from abc import ABCMeta
from abc import abstractmethod

from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple


MAX_COMMAND_LINE_RESPONSE = 8*1024*1024  # 8 MiB

MessageCallback = Callable[[str], None]


class DeviceNotFoundError(Exception):
    """An exception that is raised when a device couldn't be found."""


class DeviceTimeoutError(Exception):
    """An exception that is raised when a timeout has occurred."""


class Connection(metaclass=ABCMeta):
    @abstractmethod
    async def open(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def write_command_line(self, message: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def write_monitoring_line(self, message: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read_command_line(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def subscribe_monitoring_line(self, callback: MessageCallback) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def monitoring_line_supported(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def loop(self) -> AbstractEventLoop:
        raise NotImplementedError


class DiscoveryProtocol(asyncio.DatagramProtocol):
    """An implementation of a DatagramProtocol for device discovery.

    Attributes:
        device_name (str): The name of the DeCoP device.

    """
    import ifaddr

    def __init__(self, device_name: str) -> None:
        self._device_name = device_name
        self._regex = re.compile(r'\("(.*?)" "(.*?)" "(.*?)" "(.*?)" "(.*?)" "(.*?)" (\d+) "(.*?)" (\d+) (\d+)\)')
        self._result = asyncio.Future()  # type: asyncio.Future

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        sock = transport.get_extra_info('socket')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

        for adapter in self.ifaddr.get_adapters():
            for ip in adapter.ips:
                if ip.is_IPv4:
                    net = IPv4Network("{}/{}".format(ip.ip, ip.network_prefix), strict=False)
                    if not net.is_link_local and not net.is_loopback:
                        transport.sendto(b'whoareyou?', (str(net.broadcast_address), 60010))

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        match = self._regex.match(data.decode('utf-8', 'replace'))
        if match:
            ls = match.groups()
            if len(ls) == 10 and (ls[0] == self._device_name or ls[5] == self._device_name):
                self.result.set_result((ip_address(ls[7]), int(ls[8]), int(ls[9])))

    @property
    def result(self) -> asyncio.Future:
        """asyncio.Future: The result of the discovery process."""
        return self._result


class MonitoringLineProtocol(asyncio.Protocol):
    """An implementation of an asyncio protocol that routes monitoring line updates to callbacks.

    Attributes:
        loop (AbstractEventLoop): An asyncio event loop.
        callbacks (List[MessageCallback]): A list of callbacks.
        host (str): A host identifier, can be an IP address, a hostname, or a system label.
        monitoring_line_port (int): The network port of the monitoring line.

    """

    def __init__(self, loop: AbstractEventLoop, callbacks: List[MessageCallback], host: str, monitoring_line_port: int) -> None:
        self._logger = logging.getLogger(__name__)
        self._loop = loop
        self._callbacks = callbacks
        self._host = host
        self._monitoring_port = monitoring_line_port
        self._regex = re.compile(r'\(.*? .*? ((\"(\\.|[^"\\])*\")|.*?)\)\r?\n')
        self._stream_buffer = ''

    def connection_made(self, transport):
        pass

    def data_received(self, data):
        line, self._stream_buffer = self._readline(self._stream_buffer + data.decode('utf-8', 'replace'))

        while line:
            self._logger.debug("%s:%d - MON RX: %s", self._host, self._monitoring_port, repr(line))

            for callback in self._callbacks:
                callback(line)

            line, self._stream_buffer = self._readline(self._stream_buffer)

    def connection_lost(self, exc):
        pass

    def _readline(self, buffer: str) -> Tuple[str, str]:
        """Reads a line from a monitoring line buffer.

        Args:
            buffer: A monitoring line buffer.

        Returns:
            Tuple[str, str]: A tuple containing the extracted line and the remaining buffer.

        """
        m = self._regex.match(buffer)

        if m is not None:
            start, end = m.span()
            return buffer[start:end], buffer[end:]
        else:
            return '', buffer


class NetworkConnection(Connection):
    """A network connection for the command and monitoring lines.

    Attributes:
        host (str): A host identifier, can be an IP address, a hostname, or
        a system label.
        command_line_port (int): The network port of the command line.
        monitoring_line_port (int): The network port of the monitoring line.
        timeout (int): Timeout in seconds.
        loop (AbstractEventLoop): The event loop.

    """

    def __init__(self, host: str, command_line_port: int = 1998, monitoring_line_port: int = 1999, timeout: int = 5, loop: AbstractEventLoop = None) -> None:
        self._logger = logging.getLogger(__name__)
        self._host = host
        self._command_port = command_line_port
        self._monitoring_port = monitoring_line_port
        self._timeout = timeout
        self._loop = asyncio.get_event_loop() if loop is None else loop
        self._command_line_reader = None  # type: Optional[asyncio.StreamReader]
        self._command_line_writer = None  # type: Optional[asyncio.StreamWriter]
        self._monitor_callbacks = []  # type: List[MessageCallback]
        self._monitor_protocol = None  # type: Optional[MonitoringLineProtocol]
        self._monitor_transport = None  # type: Optional[asyncio.WriteTransport]
        if loop:
            warnings.warn('"loop" parameter is deprecated and will be removed in a future version', DeprecationWarning, stacklevel=2)

    async def open(self) -> None:
        """Opens a connection to the device.

        Raises:
            DeviceNotFoundError: If connecting to the device failed.

        """
        try:
            # Try to parse as IP address e.g. '192.168.1.32'
            self._host = ip_address(self._host)
        except ValueError:
            try:
                # Try to resolve DNS entry e.g. 'dlcpro.host.com'
                self._host = ip_address(socket.gethostbyname(self._host))
            except (ValueError, OSError):
                # Try to find system-label via UDP broadcast
                self._host, self._command_port, self._monitoring_port = await self.find_device(self._host)

        self._logger.debug("Opening network connection to '%s:%d,%d'", self._host, self._command_port, self._monitoring_port)

        if self._host is None:
            raise DeviceNotFoundError()

        # Open command line
        self._command_line_reader, self._command_line_writer = await asyncio.open_connection(self._host.compressed, self._command_port, limit=MAX_COMMAND_LINE_RESPONSE, loop=self._loop)

        try:
            # Purge welcome message
            await asyncio.wait_for(self._command_line_reader.readuntil(b'\n> '), self._timeout)
        except asyncio.TimeoutError as exc:
            raise DeviceTimeoutError('Timeout while waiting for command prompt') from exc

        # Open monitoring line
        if self._monitoring_port is not None and self._monitoring_port > 0:
            protocol = MonitoringLineProtocol(self._loop, self._monitor_callbacks, self._host, self._monitoring_port)
            self._monitor_transport, self._monitor_protocol = await self._loop.create_connection(lambda: protocol, self._host.compressed, self._monitoring_port)

    async def close(self) -> None:
        """Closes the network connection."""

        self._logger.debug("Closing network connection to '%s'", self._host)

        if self._command_line_writer is not None:
            self._command_line_writer.close()
            self._command_line_writer = None

        if self._monitor_transport is not None:
            self._monitor_transport.close()
            self._monitor_transport = None

        self._monitor_callbacks = []

    async def write_command_line(self, message: str) -> None:
        """Sends a message to the command line.

        Args:
            message (str): The message to send to the command line.

        """
        self._logger.debug("%s:%d - CMD TX: %s", self._host, self._command_port, repr(message))
        self._command_line_writer.write(message.encode())

    async def read_command_line(self) -> str:
        """Reads a message from the command line of the device.

        Returns:
            str: The message read from the command line.

        Raises:
            DeviceTimeoutError: If there was a timeout while waiting for the message.

        """
        try:
            result = await asyncio.wait_for(self._command_line_reader.readuntil(b'\n> '), self._timeout)
        except asyncio.TimeoutError as exc:
            raise DeviceTimeoutError('Timeout while waiting for response') from exc

        result = result.decode('utf-8', 'replace')

        if result.endswith('\n> '):
            self._logger.debug("%s:%d - CMD RX: %s", self._host, self._command_port, repr(result[:-3]))
            return result[:-3]
        return str()

    async def write_monitoring_line(self, message: str) -> None:
        """Sends a message to the monitoring line.

        Args:
            message: The message to send to the monitoring line.

        """
        self._logger.debug("%s:%d - MON TX: %s", self._host, self._monitoring_port, repr(message))
        self._monitor_transport.write(message.encode())

    def subscribe_monitoring_line(self, callback: MessageCallback) -> None:
        self._monitor_callbacks.append(callback)

    @property
    def monitoring_line_supported(self) -> bool:
        return self._monitor_transport is not None

    @property
    def loop(self) -> AbstractEventLoop:
        return self._loop

    async def find_device(self, device_name: str) -> Tuple[Optional[ip_address], int, int]:
        """Try to find a device in the network by name.

        Args:
            device_name (str): The name of the device.

        Returns:
            Tuple[Optional[ip_address], int, int]: A tuple containing the IP address and the command line and monitoring line ports.

        """
        protocol = DiscoveryProtocol(device_name)
        transport, _ = await self._loop.create_datagram_endpoint(lambda: protocol, local_addr=('0.0.0.0', 0))
        try:
            return await asyncio.wait_for(protocol.result, self._timeout, loop=self._loop)
        except asyncio.TimeoutError:
            return None, 0, 0
        finally:
            transport.close()


class SerialConnection(Connection):
    """A serial connection for the command line.

    Attributes:
        port (str): The name of the serial port (e.g. 'COM1' or '/dev/ttyUSB0').
        baudrate (int): The number of transferred bits per second.
        timeout (int): The communication timeout (in seconds).
        loop (int): An asyncio event loop.

    """
    import serial

    def __init__(self, port: str, baudrate: int = 115200, timeout: int = 5, loop: AbstractEventLoop = None) -> None:
        self._logger = logging.getLogger(__name__)
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._loop = asyncio.get_event_loop() if loop is None else loop
        self._serial = None
        if loop:
            warnings.warn('"loop" parameter is deprecated and will be removed in a future version', DeprecationWarning, stacklevel=2)

    async def open(self) -> None:
        """Opens a connection to the device.

        Raises:
            DeviceNotFoundError: If connecting to the device failed.

        """
        try:
            self._logger.debug("Opening serial connection to '%s' with %d baud", self._port, self._baudrate)
            self._serial = self.serial.serial_for_url(self._port, baudrate=self._baudrate)
        except self.serial.serialutil.SerialException as ex:
            raise DeviceNotFoundError() from ex

        # Temporarily set shorter timeout
        self._serial.timeout = 0.5

        # Disable serial echo (\x12) and cancel the device interpreter state (\x03)
        await self.write_command_line('\x12\x03')

        # Purge the input buffer by reading a possible welcome message and the
        # prompt created by the cancel
        await self._loop.run_in_executor(None, lambda: self._serial.read_until(b'\n> '))
        await self._loop.run_in_executor(None, lambda: self._serial.read_until(b'\n> '))

        # Restore the original timeout
        self._serial.timeout = self._timeout

    async def close(self) -> None:
        """Closes the serial connection."""
        if self._serial is not None:
            self._logger.debug("Closing serial connection to '%s'", self._port)
            self._serial.close()
            self._serial = None

    async def write_command_line(self, message: str) -> None:
        """Sends a message to the command line.

        Args:
            message (str): The message to send to the command line.

        """
        self._logger.debug("%s - CMD TX: %s", self._port, repr(message))
        await self._loop.run_in_executor(None, lambda: self._serial.write(message.encode()))

    async def write_monitoring_line(self, message: str) -> None:
        raise NotImplementedError

    async def read_command_line(self) -> str:
        """Reads a message from the command line of the device.

        Returns:
            str: The message read from the command line.

        Raises:
            DeviceTimeoutError: If there was a timeout while waiting for the message.

        """
        result = await self._loop.run_in_executor(None, lambda: self._serial.read_until(b'\n> '))
        result = result.decode('utf-8', 'replace')

        if result.endswith('\r\n> '):
            self._logger.debug("%s - CMD RX: %s", self._port, repr(result[:-4]))
            return result[:-4]

        if result.endswith('\n> '):
            self._logger.debug("%s - CMD RX: %s", self._port, repr(result[:-3]))
            return result[:-3]

        raise DeviceTimeoutError('Timeout while waiting for response')

    def subscribe_monitoring_line(self, callback: MessageCallback) -> None:
        raise NotImplementedError

    @property
    def monitoring_line_supported(self) -> bool:
        return False

    @property
    def loop(self) -> AbstractEventLoop:
        return self._loop
