import asyncio

from base64 import b64decode
from base64 import b64encode

from datetime import datetime

from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from .decop import UserLevel

from .decop import DecopType
from .decop import DecopMetaType
from .decop import DecopStreamType
from .decop import DecopStreamMetaType
from .decop import DecopError
from .decop import DecopValueError
from .decop import DecopCallback

from .decop import decode_value
from .decop import decode_value_inferred
from .decop import encode_value
from .decop import parse_monitoring_line

from .asyncio.connection import Connection
from .asyncio.connection import NetworkConnection
from .asyncio.connection import SerialConnection
from .asyncio.connection import DeviceNotFoundError
from .asyncio.connection import DeviceTimeoutError

__all__ = ['UserLevel', 'Connection', 'Client', 'Subscription', 'DecopCallback', 'NetworkConnection', 'SerialConnection',

           'DecopError', 'DecopValueError', 'DeviceTimeoutError', 'DeviceNotFoundError',

           'DecopBoolean', 'DecopInteger', 'DecopReal', 'DecopString', 'DecopBinary',
           'MutableDecopBoolean', 'MutableDecopInteger', 'MutableDecopReal', 'MutableDecopString', 'MutableDecopBinary']


class Client:
    """A synchronous DeCoP client.

    Attributes:
        connection (Connection): A connection that is used to communicate with the device.

    """

    def __init__(self, connection: Connection) -> None:
        self._connection = connection
        self._subscriptions = {}  # type: Dict[str, Tuple[DecopMetaType, List[Subscription]]]
        self._sleep_future = None  # type: Optional[asyncio.Future]
        self._timer_handle = None  # type: Optional[asyncio.TimerHandle]

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def open(self) -> None:
        """Opens a connection to a DeCoP device."""
        self._async_run(self._connection.open())

        if self._connection.monitoring_line_supported:
            self._connection.subscribe_monitoring_line(self._monitoring_line_callback)

    def close(self) -> None:
        """Closes the connection to the DeCoP device."""
        async def async_close():
            await self._connection.close()

        subscribers = []

        for _, value in self._subscriptions.values():
            subscribers += value

        for subscriber in subscribers:
            subscriber.cancel()

        self._async_run(async_close())
        self._subscriptions = {}

    def change_ul(self, ul: UserLevel, password: str) -> UserLevel:
        """Changes the current user level of the command and monitoring line.

        Args:
            ul (UserLevel): The requested user level.
            password (str): The password for the requested user level.

        Returns:
            UserLevel: The new user level or the previous one if the password was incorrect.

        """
        async def async_change_ul() -> None:
            """Wraps the communication in an asynchronous function."""
            await self._connection.write_monitoring_line('(change-ul {} "{}")\r\n'.format(int(ul), password))

        # Empty passwords are only allowed for UserLevel.NORMAL and UserLevel.READONLY
        if not password and ul != UserLevel.NORMAL and ul != UserLevel.READONLY:
            return UserLevel(self.get('ul', int))

        # Change the user level for the command line
        result = UserLevel(self.exec('change-ul', int(ul), password, return_type=int))

        # Change the user level for the monitoring line
        if self._connection.monitoring_line_supported and result == ul:
            self._async_run(async_change_ul())

        return result

    def run(self, timeout: int = None) -> None:
        """Runs the event loop for the monitoring line.

        Args:
            timeout (int): An timeout after this function will return.

        """
        if timeout:
            self._sleep_future = self._connection.loop.create_future()
            self._timer_handle = self._connection.loop.call_later(timeout, self._sleep_timeout)
            self._connection.loop.run_until_complete(self._sleep_future)
        else:
            self._connection.loop.run_forever()
            self._sleep_future = None
            self._timer_handle = None

    def stop(self) -> None:
        """Stops the event loop for the monitoring line."""
        if self._sleep_future and self._timer_handle:
            self._timer_handle.cancel()
            if not self._sleep_future.done():
                self._sleep_future.set_result(0)
            self._sleep_future = None
            self._timer_handle = None
        else:
            self._connection.loop.stop()

    def poll(self) -> None:
        """Runs all currently scheduled callbacks and returns."""
        self._connection.loop.stop()
        self._connection.loop.run_forever()

    def get(self, param_name: str, *param_types: DecopMetaType) -> DecopType:
        """Returns the current value of a DeCoP parameter.

        Args:
            param_name (str): The name of the DeCoP parameter (e.g. 'laser1:enabled').
            param_types (DecopMetaType): One or more types of the DeCoP parameter.

        Returns:
            DecopType: The current value of the parameter.

        """
        async def async_get() -> str:
            """Wraps the communication in an asynchronous function."""
            await self._connection.write_command_line("(param-ref '{})\n".format(param_name))
            return await self._connection.read_command_line()

        result = self._async_run(async_get())

        if not param_types:
            return decode_value_inferred(result)
        elif len(param_types) == 1:
            return decode_value(result, param_types[0])
        else:
            values = result[1:-1].split(' ')
            if len(values) == len(param_types):
                return tuple(decode_value(pair[0], pair[1]) for pair in zip(values, param_types))
            else:
                raise DecopError("Invalid type list: '{}' for value '{}'".format(param_types, values))

    def get_set_value(self, param_name: str, *param_types: DecopMetaType) -> DecopType:
        """Returns the current 'set value' of a DeCoP parameter.

        Args:
            param_name (str): The name of the DeCoP parameter (e.g. 'laser1:enabled').
            param_types (DecopMetaType): One or more types of the DeCoP parameter.

        Returns:
            DecopType: The current value of the parameter.

        """
        async def async_get_set_value() -> str:
            """Wraps the communication in an asynchronous function."""
            await self._connection.write_command_line("(param-gsv '{})\n".format(param_name))
            return await self._connection.read_command_line()

        result = self._async_run(async_get_set_value())

        if not param_types:
            return decode_value_inferred(result)
        elif len(param_types) == 1:
            return decode_value(result, param_types[0])
        else:
            values = result[1:-1].split(' ')
            if len(values) == len(param_types):
                return tuple(decode_value(pair[0], pair[1]) for pair in zip(values, param_types))
            else:
                raise DecopError("Invalid type list: '{}' for value '{}'".format(param_types, values))

    def set(self, param_name: str, *param_values: DecopType) -> None:
        """Set a new value for a DeCoP parameter.

        Args:
            param_name (str): The name of the DeCoP parameter (e.g. 'laser1:enabled').
            param_values (DecopType): One or more parameter values.

        Raises:
            DecopError: If the device returned an error when setting the new value.

        """
        async def async_set() -> str:
            """Wraps the communication in an asynchronous function."""
            values = [encode_value(x) for x in param_values]
            fmt = "(param-set! '{} {})\n" if len(values) == 1 else "(param-set! '{} '({}))\n"

            await self._connection.write_command_line(fmt.format(param_name, ' '.join(values)))
            return await self._connection.read_command_line()

        result = self._async_run(async_set())

        # Skip any additional output before the status code
        result = result.splitlines()
        result = result[-1]

        status = decode_value(result, int)
        if status != 0:
            raise DecopError("Setting parameter '{}' to '{}' failed: '{}'".format(param_name, param_values, status))

    def exec(self, name: str, *args, input_stream: DecopStreamType = None, output_type: DecopStreamMetaType = None,
             return_type: DecopMetaType = None) -> Optional[DecopType]:
        """Execute a DeCoP command.

        Args:
            name (str): The name of the command.
            *args: The parameters of the command.
            input_stream (DecopStreamType): The input stream data of the command.
            output_type (DecopStreamMetaType): The type of the output stream of the command.
            return_type (DecopMetaType): The type of the optional return value.

        Returns:
            Optional[DecopType]: Either the output stream, the return value or a tuple of both.

        """
        async def async_exec() -> str:
            """Wraps the communication in an asynchronous function."""
            param_list = ''
            for param in args:
                param_list += ' ' + encode_value(param)
            await self._connection.write_command_line("(exec '" + name + param_list + ")\n")

            if isinstance(input_stream, str):
                await self._connection.write_command_line(input_stream + '#')
            elif isinstance(input_stream, bytes):
                await self._connection.write_command_line(b64encode(input_stream).decode('ascii') + '#')

            return await self._connection.read_command_line()

        result = self._async_run(async_exec())

        lines = str.splitlines(result, keepends=True)

        if not lines:
            raise DecopError("Missing response for command '" + name + "'")

        if lines[0].lower().startswith('error:'):
            # Error in the first line of the response: use the whole response as error message
            raise DecopError(result)

        if lines[-1].lower().startswith('error:'):
            # Error in the last line of the response: use only this line as error message
            raise DecopError(lines[-1])

        output_value, return_value = None, None

        if output_type is bytes:
            output_value = b64decode(''.join(lines[:-1]).encode())

        if output_type is str:
            output_value = ''.join(lines[:-1])

        if return_type is not None:
            return_value = decode_value(lines[-1], return_type)

        if output_type is not None and return_type is not None:
            return output_value, return_value
        elif output_type is not None:
            return output_value
        elif return_type is not None:
            return return_value

        return None
        
    def subscribe(self, param_name: str, param_type: DecopMetaType, callback: DecopCallback = None) -> 'Subscription':
        """Creates a new subscription to updates of a parameter.

        Args:
            param_name (str): The name of the parameter.
            param_type (DecopMetaType): The type of the parameter.
            callback (DecopCallback): The callback that will be invoked on parameter updates.

        Returns:
            Subscription: A subscription to updates of the parameter.

        Raises:
            DecopError: If the current connection doesn't support parameter subscriptions.

        """
        if not self._connection.monitoring_line_supported:
            raise DecopError("Current connection does not support parameter subscriptions")

        subscription = Subscription(self, param_name, callback)

        if param_name in self._subscriptions:
            _, subscribers = self._subscriptions[param_name]
            subscribers.append(subscription)
        else:
            self._async_run(self._connection.write_monitoring_line("(add '{})\r\n".format(param_name)))
            self._subscriptions[param_name] = (param_type, [subscription])

        return subscription

    def unsubscribe(self, subscription: 'Subscription') -> None:
        """Cancels a subscription for parameter updates.

        Args:
            subscription (Subscription): The subscription to cancel.

        """
        try:
            _, subscribers = self._subscriptions[subscription.name]
            subscribers.remove(subscription)

            if not subscribers:
                self._async_run(self._connection.write_monitoring_line("(remove '{})\r\n".format(subscription.name)))
                self._subscriptions.pop(subscription.name)
        except KeyError:
            pass

    def _sleep_timeout(self):
        """Completes the future when the run() function has timed out."""
        if not self._sleep_future.done():
            self._sleep_future.set_result(0)

    def _monitoring_line_callback(self, message: str) -> None:
        """Routes updates of the monitoring line to subscribed callbacks.

        Args:
            message (str): The update message from the monitoring line.

        """
        timestamp, name, value = parse_monitoring_line(message)

        try:
            value_type, subscribers = self._subscriptions[name]

            if isinstance(value, DecopError):
                for subscriber in subscribers:
                    subscriber.update(timestamp, value_type(), value)
            else:
                result = decode_value(value, value_type)
                for subscriber in subscribers:
                    subscriber.update(timestamp, result, None)
        except KeyError:
            pass

    def _async_run(self, coro):
        return self._connection.loop.run_until_complete(coro)


class Subscription:
    """A subscription to updates of a parameter.

    Attributes:
        client (Client): A DeCoP client that is used to access the parameter on a device.
        name (str): The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').
        callback (DecopCallback): A callback that will be invoked when the value of the parameter has changed.

    """

    def __init__(self, client: Client, name: str, callback: DecopCallback = None) -> None:
        self._client = client
        self._name = name
        self._callback = callback

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._client is not None:
            self.cancel()

    def update(self, timestamp: datetime, value: DecopType, exc: DecopError = None) -> None:
        """Invokes the callback with an updated parameter value.

        Args:
            timestamp (datetime): The timestamp of the parameter update.
            value (DecopType): The updated parameter value.
            exc (DecopError): An optional exception that may have occurred.

        """
        if self._callback is not None:
            self._callback(timestamp, self._name, value, exc)

    def cancel(self) -> None:
        """Cancels the subscription for parameter updates."""
        self._client.unsubscribe(self)
        self._name = self._client = self._callback = None

    @property
    def name(self) -> str:
        """Returns the name of the parameter this subscription is bound to."""
        return self._name


class DecopBoolean:
    """A read-only DeCoP boolean parameter.

    Attributes:
        client (Client): A DeCoP client that is used to access the parameter on a device.
        name (str): The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    def get(self) -> bool:
        """Returns the current value of the parameter.

        Returns:
            bool: The current value of the parameter.

        """
        result = self._client.get(self._name, bool)
        assert isinstance(result, bool)
        return result

    def subscribe(self, callback: DecopCallback = None) -> 'Subscription':
        """Creates a subscription to updates of the parameter.

        Args:
            callback (DecopCallback): A callback that will be invoked when the value of the parameter has changed.

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return self._client.subscribe(self._name, bool, callback)


class MutableDecopBoolean:
    """A read/write DeCoP boolean parameter.

    Attributes:
        client (Client): A DeCoP client that is used to access the parameter on a device.
        name (str): The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    def get(self) -> bool:
        """Returns the current value of the parameter.

        Returns:
            bool: The current value of the parameter.

        """
        result = self._client.get(self._name, bool)
        assert isinstance(result, bool)
        return result

    def set(self, value: bool) -> None:
        """Updates the value of the parameter.

        Args:
            value (bool): The new value of the parameter.

        """
        assert isinstance(value, bool), "expected type 'bool' for 'value', got '{}'".format(type(value))
        self._client.set(self._name, value)

    def subscribe(self, callback: DecopCallback = None) -> 'Subscription':
        """Creates a subscription to updates of the parameter.

        Args:
            callback (DecopCallback): A callback that will be invoked when the value of the parameter has changed.

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return self._client.subscribe(self._name, bool, callback)


class DecopInteger:
    """A read-only DeCoP integer parameter.

    Attributes:
        client (Client): A DeCoP client that is used to access the parameter on a device.
        name (str): The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    def get(self) -> int:
        """Returns the current value of the parameter.

        Returns:
            int: The current value of the parameter.

        """
        result = self._client.get(self._name, int)
        assert isinstance(result, int)
        return result

    def subscribe(self, callback: DecopCallback = None) -> 'Subscription':
        """Creates a subscription to updates of the parameter.

        Args:
            callback (DecopCallback): A callback that will be invoked when the value of the parameter has changed.

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return self._client.subscribe(self._name, int, callback)


class MutableDecopInteger:
    """A read/write DeCoP integer parameter.

    Attributes:
        client (Client): A DeCoP client that is used to access the parameter on a device.
        name (str): The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    def get(self) -> int:
        """Returns the current value of the parameter.

        Returns:
            int: The current value of the parameter.

        """
        result = self._client.get(self._name, int)
        assert isinstance(result, int)
        return result

    def set(self, value: int):
        """Updates the value of the parameter.

        Args:
            value (int): The new value of the parameter.

        """
        assert isinstance(value, int), "expected type 'int' for 'value', got '{}'".format(type(value))
        self._client.set(self._name, value)

    def subscribe(self, callback: DecopCallback = None) -> 'Subscription':
        """Creates a subscription to updates of the parameter.

        Args:
            callback (DecopCallback): A callback that will be invoked when the value of the parameter has changed.

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return self._client.subscribe(self._name, int, callback)


class DecopReal:
    """A read-only DeCoP floating point parameter.

    Attributes:
        client (Client): A DeCoP client that is used to access the parameter on a device.
        name (str): The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    def get(self) -> float:
        """Returns the current value of the parameter.

        Returns:
            float: The current value of the parameter.

        """
        result = self._client.get(self._name, float)
        assert isinstance(result, float)
        return result

    def subscribe(self, callback: DecopCallback = None) -> 'Subscription':
        """Creates a subscription to updates of the parameter.

        Args:
            callback (DecopCallback): A callback that will be invoked when the value of the parameter has changed.

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return self._client.subscribe(self._name, float, callback)


class MutableDecopReal:
    """A read/write DeCoP floating point parameter.

    Attributes:
        client (Client): A DeCoP client that is used to access the parameter on a device.
        name (str): The fully qualified name of the parameter (e.g. 'laser1:amp:ontime').

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    def get(self) -> float:
        """Returns the current value of the parameter.

        Returns:
            float: The current value of the parameter.

        """
        result = self._client.get(self._name, float)
        assert isinstance(result, float)
        return result

    def set(self, value: float) -> None:
        """Updates the value of the parameter.

        Args:
            value (float): The new value of the parameter.

        """
        assert isinstance(value, float), "expected type 'float' for 'value', got '{}'".format(type(value))
        self._client.set(self._name, value)

    def subscribe(self, callback: DecopCallback = None) -> 'Subscription':
        """Creates a subscription to updates of the parameter.

        Args:
            callback (DecopCallback): A callback that will be invoked when the value of the parameter has changed.

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return self._client.subscribe(self._name, float, callback)


class DecopString:
    """A read-only DeCoP string parameter.

    Attributes:
        client (Client): A DeCoP client that is used to access the parameter on a device
        name (str): The fully qualified name of the parameter (e.g. 'laser1:amp:ontime')

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    def get(self) -> str:
        """Returns the current value of the parameter.

        Returns:
            str: The current value of the parameter.

        """
        result = self._client.get(self._name, str)
        assert isinstance(result, str)
        return result

    def subscribe(self, callback: DecopCallback = None) -> 'Subscription':
        """Creates a subscription to updates of the parameter.

        Args:
            callback (DecopCallback): A callback that will be invoked when the value of the parameter has changed.

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return self._client.subscribe(self._name, str, callback)


class MutableDecopString:
    """A read/write DeCoP string parameter.

    Attributes:
        client (Client): A DeCoP client that is used to access the parameter on a device
        name (str): The fully qualified name of the parameter (e.g. 'laser1:amp:ontime')

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    def get(self) -> str:
        """Returns the current value of the parameter.

        Returns:
            str: The current value of the parameter.

        """
        result = self._client.get(self._name, str)
        assert isinstance(result, str)
        return result

    def set(self, value: str) -> None:
        """Updates the value of the parameter.

        Args:
            value (str): The new value of the parameter.

        """
        assert isinstance(value, str), "expected type 'str' for 'value', got '{}'".format(type(value))
        self._client.set(self._name, value)

    def subscribe(self, callback: DecopCallback = None) -> 'Subscription':
        """Creates a subscription to updates of the parameter.

        Args:
            callback (DecopCallback): A callback that will be invoked when the value of the parameter has changed.

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return self._client.subscribe(self._name, str, callback)


class DecopBinary:
    """A read-only DeCoP binary parameter.

    Attributes:
        client (Client): A DeCoP client that is used to access the parameter on a device
        name (str): The fully qualified name of the parameter (e.g. 'laser1:amp:ontime')

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    def get(self) -> bytes:
        """Returns the current value of the parameter.

        Returns:
            bytes: The current value of the parameter.

        """
        result = self._client.get(self._name, bytes)
        assert isinstance(result, bytes)
        return result

    def subscribe(self, callback: DecopCallback = None) -> 'Subscription':
        """Creates a subscription to updates of the parameter.

        Args:
            callback (DecopCallback): A callback that will be invoked when the value of the parameter has changed.

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return self._client.subscribe(self._name, bytes, callback)


class MutableDecopBinary:
    """A read/write DeCoP binary parameter.

    Attributes:
        client (Client): A DeCoP client that is used to access the parameter on a device
        name (str): The fully qualified name of the parameter (e.g. 'laser1:amp:ontime')

    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

    @property
    def name(self) -> str:
        """str: The fully qualified name of the parameter."""
        return self._name

    def get(self) -> bytes:
        """Returns the current value of the parameter.

        Returns:
            bytes: The current value of the parameter.

        """
        result = self._client.get(self._name, bytes)
        assert isinstance(result, bytes)
        return result

    def set(self, value: bytes) -> None:
        """Updates the value of the parameter.

        Args:
            value (bytes): The new value of the parameter.

        """
        assert isinstance(value, bytes), "expected type 'bytes' for 'value', got '{}'".format(type(value))
        self._client.set(self._name, value)

    def subscribe(self, callback: DecopCallback = None) -> 'Subscription':
        """Creates a subscription to updates of the parameter.

        Args:
            callback (DecopCallback): A callback that will be invoked when the value of the parameter has changed.

        Returns:
            Subscription: A subscription to updates of the parameter.

        """
        return self._client.subscribe(self._name, bytes, callback)
