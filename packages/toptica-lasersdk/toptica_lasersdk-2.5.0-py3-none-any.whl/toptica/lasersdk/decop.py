import re

from collections import OrderedDict
from datetime import datetime
from enum import Enum, IntEnum

from base64 import b64encode
from base64 import b64decode

from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import fromstring


class DecopError(Exception):
    """A generic DeCoP error."""


class DecopValueError(Exception):
    """A DeCoP value conversion error."""
    def __init__(self, value: str, expected_type: Optional[type] = None):
        if expected_type:
            super().__init__("Failed to convert '{!r}' to type '{}'".format(value, expected_type))
        else:
            super().__init__("Failed to infer type for '{!r}'".format(value))


DecopType = Union[bool, int, float, str, bytes, tuple]
DecopMetaType = Type[DecopType]

DecopStreamType = Union[str, bytes]
DecopStreamMetaType = Type[DecopStreamType]

DecopCallback = Callable[[datetime, str, DecopType, DecopError], None]
DecopMonitoringLine = Tuple[datetime, str, Union[str, DecopError]]


class UserLevel(IntEnum):
    """A user level of a parameter in a DeCoP system model."""
    INTERNAL = 0
    SERVICE = 1
    MAINTENANCE = 2
    NORMAL = 3
    READONLY = 4


class ParamMode(Enum):
    """An access mode of a parameter in a DeCoP system model."""
    READONLY = 1
    WRITEONLY = 2
    READWRITE = 3
    READSET = 4


class StreamType(Enum):
    """A stream type of a command in a DeCoP system model."""
    TEXT = 1
    BASE64 = 2


def user_level(user_level_str: Optional[str]) -> Optional[UserLevel]:
    """Converts a string with a parameter user level to the corresponding type.

    Args:
        user_level_str (str): The string with the parameter user level.

    Returns:
        Optional[UserLevel]: The type of the parameter user level.

    """
    if not user_level_str:
        return None

    table = {'internal':    UserLevel.INTERNAL,
             'service':     UserLevel.SERVICE,
             'maintenance': UserLevel.MAINTENANCE,
             'normal':      UserLevel.NORMAL,
             'readonly':    UserLevel.READONLY}

    try:
        return table[user_level_str.strip().lower()]
    except KeyError:
        return None


def access_mode(access_mode_str: Optional[str]) -> Optional[ParamMode]:
    """Converts a string with a parameter access mode to the corresponding type.

    Args:
        access_mode_str (str): The string with the parameter access mode.

    Returns:
        Optional[ParamMode]: The type of the parameter access mode.

    """
    if not access_mode_str:
        return None

    table = {'readonly':  ParamMode.READONLY,
             'writeonly': ParamMode.WRITEONLY,
             'readwrite': ParamMode.READWRITE,
             'readset':   ParamMode.READSET}

    try:
        return table[access_mode_str.strip().lower()]
    except KeyError:
        return None


def stream_type(stream_type_str: Optional[str]) -> Optional[StreamType]:
    """Converts a string with a command stream type to the corresponding type.

    Args:
        stream_type_str (str): The string with the command stream type.

    Returns:
        Optional[StreamType]: The type of the command stream type.

    """
    if not stream_type_str:
        return None

    table = {'base64': StreamType.BASE64,
             'text':   StreamType.TEXT}

    try:
        return table[stream_type_str.strip().lower()]
    except KeyError:
        return None


def encode_value(value: DecopType) -> str:
    """Encodes a value to a string.

    Args:
        value (DecopType): The value of the parameter.

    Returns:
        str: The encoded value.

    """
    if isinstance(value, bool):
        return '#t' if value else '#f'

    if isinstance(value, (int, float)):
        return str(value)

    if isinstance(value, str):
        return '"' + value + '"'

    if isinstance(value, bytes):
        return '"' + b64encode(value).decode() + '"'

    raise DecopError('Invalid type for value: {}'.format(type(value)))


def decode_value(result: str, expected_type: DecopMetaType) -> DecopType:
    """Converts a DeCoP parameter string to a Python value.

    Args:
        result (str): The string returned by the command line.
        expected_type (DecopTypeList): The expected type of the result.

    Returns:
        DecopType: The value of the command line result.

    Raises:
        DecopError: If the command line returned an error message
        DecopValueError: If the command line result couldn't be converted to the expected type.

    """
    if result.lower().startswith('error'):
        raise DecopError(result)

    try:
        if expected_type is int:
            return int(result)
    except ValueError as exc:
        raise DecopValueError(result, int) from exc

    try:
        if expected_type is float:
            return float(result)
    except ValueError as exc:
        raise DecopValueError(result, float) from exc

    if expected_type is bool:
        if result in ['#t', '#T']:
            return True
        if result in ['#f', '#F']:
            return False
        raise DecopValueError(result, bool)

    if expected_type is str:
        if not result.startswith('"') or not result.endswith('"'):
            raise DecopValueError(result, str)
        return result.strip('"')

    if expected_type is bytes:
        if result.startswith('&'):
            return b64decode(result[1:])
        if result.startswith('"') and result.endswith('"'):
            return b64decode(result[1:-1])
        raise DecopValueError(result, bytes)

    if expected_type is tuple:
        if result.startswith("'(") and result.endswith(")"):
            return tuple(result[2:-1].split(' '))
        raise DecopValueError(result, tuple)

    raise DecopError("Unexpected type while decoding a DeCoP value: '{}'".format(expected_type))


def decode_value_inferred(param_str: str) -> DecopType:
    """Tries to convert a DeCoP parameter string to a Python type by inferring its data type.

    Args:
        param_str (str): The string containing the parameter value.

    Returns:
        DecopType: The value of the parameter string.

    Raises:
        DecopError: If the parameter string contains an error message.
        DecopValueError: If the data type of the parameter string couldn't be inferred.

    """
    if param_str.lower().startswith('error'):
        raise DecopError(param_str)

    if param_str in ['#t', '#T']:
        return True
    if param_str in ['#f', '#F']:
        return False

    if param_str.startswith('&'):
        return b64decode(param_str[1:])

    if param_str.startswith('"') and param_str.endswith('"'):
        return param_str[1:-1]

    if param_str.startswith('(') and param_str.endswith(')'):
        _, value = _match_tuple(param_str)
        if value is None:
            raise DecopValueError(param_str)
        return value

    try:
        return int(param_str)
    except ValueError:
        try:
            return float(param_str)
        except ValueError as exc:
            raise DecopValueError(param_str) from exc


def _match_bool(text: str) -> Tuple[str, Optional[bool]]:
    """Tries to match a boolean value.

    Args:
        text (str): The string containing the boolean value.

    Returns:
        Tuple[str, Optional[bool]]: A tuple containing the remaining text and boolean value if the
                                    match was successful, the original text and None otherwise.

    """
    if len(text) < 2 or text[0] != '#':
        return text, None
    if text[1] in 'tT':
        return text[2:], True
    if text[1] in 'fF':
        return text[2:], False
    return text, None


def _match_int(text: str) -> Tuple[str, Optional[int]]:
    """Tries to match an integer value.

    Args:
        text (str): The string containing the integer value.

    Returns:
        Tuple[str, Optional[int]]: A tuple containing the remaining text and integer value if the
                                   match was successful, the original text and None otherwise.

    """
    if len(text) == 0:
        return '', None

    # Match sign
    i = 1 if text[0] in '+-' else 0

    has_value = False

    for i in range(i, len(text)):
        if text[i] in '0123456789':
            has_value = True
        elif text[i] in '() \t\v\f\r\n':
            return (text[i:], int(text[:i])) if has_value else (text, None)
        else:
            return text, None

    return (text[i+1:], int(text[:i+1])) if has_value else (text, None)


def _match_float(text: str) -> Tuple[str, Optional[float]]:
    """Tries to match a floating point (real) value.

    Args:
        text (str): The string containing the floating point value.

    Returns:
        Tuple[str, Optional[float]]: A tuple containing the remaining text and floating point value if the
                                     match was successful, the original text and None otherwise.

    """
    if len(text) == 0:
        return '', None

    # Match sign
    i = 1 if text[0] in '+-' else 0

    has_dot = False
    has_value = False

    for i in range(i, len(text)):
        if text[i] in '0123456789':
            has_value = True
        elif text[i] in '.':
            if has_dot:
                return text, None
            has_dot = True
        elif text[i] in '() \t\v\f\r\n':
            return (text[i:], float(text[:i])) if has_dot and has_value else (text, None)
        elif text[i] in 'eE' and has_value and i != len(text) - 1:
            break  # Continue by matching exponent
        else:
            return text, None
    else:
        return (text[i+1:], float(text[:i+1])) if has_dot and has_value else (text, None)

    # Match 'e|E', match sign
    i += 2 if text[i+1] in '+-' else 1

    has_value = False

    for i in range(i, len(text)):
        if text[i] in '0123456789':
            has_value = True
        elif text[i] in '() \t\v\f\r\n':
            return (text[i:], float(text[:i])) if has_value else (text, None)
        else:
            return text, None

    return (text[i+1:], float(text[:i+1])) if has_value else (text, None)


def _match_string(text: str) -> Tuple[str, Optional[str]]:
    """Tries to match a string value.

    Args:
        text (str): The string containing the string value.

    Returns:
        Tuple[str, Optional[str]]: A tuple containing the remaining text and string value if the
                                   match was successful, the original text and None otherwise.

    """
    if len(text) < 2 or text[0] != '"':
        return text, None

    is_escaped = False

    for i in range(1, len(text)):
        if text[i] == '\\':
            is_escaped = True if not is_escaped else False
        elif text[i] == '"' and not is_escaped:
            return text[i+1:], text[1:i]
        else:
            is_escaped = False

    return text, None


def _match_bytes(text: str) -> Tuple[str, Optional[bytes]]:
    """Tries to match a bytes value.

    Args:
        text (str): The string containing the bytes value.

    Returns:
        Tuple[str, Optional[bytes]]: A tuple containing the remaining text and bytes value if the
                                     match was successful, the original text and None otherwise.

    """
    if len(text) == 0 or text[0] != '&':
        return text, None

    for i in range(1, len(text)):
        if text[i] in '() \t\v\f\r\n':
            return text[i:], b64decode(text[1:i])
        if not text[i].isalnum() and text[i] not in '+/=':
            return text, None

    return '', b64decode(text[1:])


def _match_tuple(text: str) -> Tuple[str, Optional[tuple]]:
    """Tries to match a tuple value.

    Args:
        text (str): The string containing the tuple value.

    Returns:
        Tuple[str, Optional[tuple]]: A tuple containing the remaining text and tuple value if the
                                     match was successful, the original text and None otherwise.

    """
    if len(text) < 2 or text[0] != '(':
        return text, None

    ls = []
    original = text[:]
    text = text[1:]

    while len(text) > 0:
        value = None
        if text[0] == '#':
            text, value = _match_bool(text)
        elif text[0] == '"':
            text, value = _match_string(text)
        elif text[0] == '&':
            text, value = _match_bytes(text)
        elif text[0] == '.':
            text, value = _match_float(text)
        elif text[0] in '0123456789+-':
            text, value = _match_int(text)
            if value is None:
                text, value = _match_float(text)
        elif text[0] == '(':
            text, value = _match_tuple(text)
        elif text[0] == ')':
            return text[1:], tuple(ls)

        if value is None:
            return original, None

        ls.append(value)
        text = text.lstrip()

    return original, None


def parse_monitoring_line(line: str) -> DecopMonitoringLine:
    """Parses a monitoring line message.

    Args:
        line (str): A monitoring line message.

    Returns:
        DecopMonitoringLine: A tuple containing the timestamp, parameter name and value/exception.

    """
    datetime_fmt = '%Y-%m-%dT%H:%M:%S.%fZ'

    if line.lower().startswith('(error: '):
        match = re.match(r"\(Error: (.*?) \((.*?) '(.*?)\) (.*?)\)\r?\n", line, re.IGNORECASE)

        if match is not None:
            ls = match.groups()
            timestamp = datetime.strptime(ls[1], datetime_fmt)
            error = DecopError('Error: {} {}'.format(ls[0], ls[3]))
            return timestamp, ls[2], error
    else:
        match = re.match(r"\((.*?) '(.*?) (.*?)\)\r?\n", line)

        if match is not None:
            ls = match.groups()
            timestamp = datetime.strptime(ls[0], datetime_fmt)
            return timestamp, ls[1], ls[2]

    error = DecopError('Invalid monitoring line message: {!r}'.format(line))
    return datetime.now(), '', error


class Parameter:
    """A parameter in a DeCoP system model.

    Attributes:
        name (str): The name of the parameter.
        typestr (str): The type of the parameter.
        mode (ParamMode): The access mode of the parameter.
        readlevel(UserLevel): The required user level to read the parameter.
        writelevel(UserLevel): The required user level to write the parameter.

    """
    def __init__(self, name: str, typestr: str, description: str, mode: ParamMode, readlevel: Optional[UserLevel], writelevel: Optional[UserLevel]) -> None:
        self.name = name
        self.paramtype = typestr
        self.description = description
        self.mode = mode
        self.readlevel = readlevel
        self.writelevel = writelevel


class Command:
    """A command in the DeCoP system model.

    Attributes:
        name(str): The name of the command.
        input_type(StreamType): The type of the input stream.
        output_type (StreamType): The type of the output stream.
        execlevel (UserLevel): The required user level to execute the command.
        params (List[Tuple[str, str]]): The list of parameter names and types of the command.
        return_type (str): The type of the return value.

    """
    def __init__(self, name: str, description: str, input_type: Optional[StreamType], output_type: Optional[StreamType], execlevel: Optional[UserLevel], params: List[Tuple[str, str]], return_type: str) -> None:
        self.name = name
        self.description = description
        self.input_type = input_type
        self.output_type = output_type
        self.execlevel = execlevel
        self.params = params
        self.return_type = return_type


class Typedef:
    """A typedef in a DeCoP system model.

    Attributes:
        name (str): The name of the typedef.
        is_atomic (bool): True if the typedef is atomic, False otherwise.

    """

    def __init__(self, name: str, is_atomic: bool) -> None:
        self.name = name
        self.is_atomic = is_atomic
        self.params = OrderedDict()  # type: OrderedDict[str, Parameter]
        self.cmds = OrderedDict()  # type: OrderedDict[str, Command]


class Module:
    """A module in a DeCoP system model.

    Attributes:
        name (str): The name of the module.

    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.params = OrderedDict()  # type: OrderedDict[str, Parameter]
        self.cmds = OrderedDict()  # type: OrderedDict[str, Command]


class SystemModel:
    """A DeCoP system model."""

    def __init__(self) -> None:
        self.name = ''
        self.typedefs = OrderedDict()  # type: OrderedDict[str, Typedef]
        self.modules = OrderedDict()  # type: OrderedDict[str, Module]

    def build_from_file(self, filename: str) -> None:
        """Loads a DeCoP system model from an XML file.

        Args:
            filename (str): The name of the XML file with the DeCoP system model.

        """
        xml = ElementTree(file=filename)
        self._build_model(xml)

    def build_from_string(self, xml_str: str) -> None:
        """Loads a DeCoP system model form a string.

        Args:
            xml_str (str): A string containing the XML description of the DeCoP system model.

        """
        xml = ElementTree(fromstring(xml_str))
        self._build_model(xml)

    def _build_model(self, xml: ElementTree) -> None:
        """Builds the system model from an XML tree.

        Args:
            xml (ElementTree): The DeCoP system model.

        """
        self._read_system(xml)
        self._read_xtypedefs(xml)
        self._read_modules(xml)

    def _read_system(self, xml: ElementTree) -> None:
        """Reads system definition from the DeCoP system model.

        Args:
            xml (ElementTree): The DeCoP system model.

        """
        self.name = xml.getroot().get('name')

    def _read_xtypedefs(self, xml: ElementTree) -> None:
        """Reads all typedefs from the DeCoP system model.

        Args:
            xml (ElementTree): The DeCoP system model.

        """
        for xtypedef in xml.iter(tag='xtypedef'):
            name = xtypedef.get('name')
            is_atomic = str(xtypedef.get('is_atomic')).lower() == 'true'
            node = Typedef(name, is_atomic)
            self._read_params(xtypedef, node, None)
            self._read_cmds(xtypedef, node)
            self.typedefs[name] = node

    def _read_modules(self, xml: ElementTree) -> None:
        """Reads all modules from the DeCoP system model.

        Args:
            xml (ElementTree): The DeCoP system model.

        """
        for mod in xml.iter(tag='module'):
            name = mod.get('name')
            node = Module(name)
            self._read_params(mod, node, UserLevel.NORMAL)
            self._read_cmds(mod, node)
            self.modules[name] = node

    @staticmethod
    def _read_params(element: Element, node: Union[Module, Typedef], default_level: Optional[UserLevel]) -> None:
        """Reads all parameters of a DeCoP system model node.

        Args:
            element (ElementTree): The DeCoP system model node.
            node (Node): The node in this system model.

        """
        for param in element.iter(tag='param'):
            param_name = param.get('name')
            param_type = param.get('type')
            param_mode = access_mode(param.get('mode'))
            readlevel = user_level(param.get('readlevel'))
            writelevel = user_level(param.get('writelevel'))
            if readlevel is None and param_mode != ParamMode.WRITEONLY:
                readlevel = default_level
            if writelevel is None and param_mode != ParamMode.READONLY:
                writelevel = default_level
            param_description = ''
            for desc in param.iter(tag='description'):
                param_description += desc.text
            node.params[param_name] = Parameter(param_name, param_type, param_description, param_mode, readlevel, writelevel)

    @staticmethod
    def _read_cmds(element: Element, node: Union[Module, Typedef]) -> None:
        """Reads all commands of a DeCoP system model node.

        Args:
            element (ElementTree): The DeCoP system model node.
            node (Node): The node in this system model.

        """
        for cmd in element.iter(tag='cmd'):
            cmd_name = cmd.get('name')
            cmd_in = stream_type(cmd.get('input'))
            cmd_out = stream_type(cmd.get('output'))
            execlevel = user_level(cmd.get('execlevel'))
            ret_type = None
            for ret in cmd.iter(tag='ret'):
                ret_type = ret.get('type')
            desc = ''
            for item in cmd.iter(tag='description'):
                desc += item.text
            params = []
            for arg in cmd.iter(tag='arg'):
                arg_name = arg.get('name')
                arg_type = arg.get('type')
                params.append((arg_name, arg_type))
            node.cmds[cmd_name] = Command(cmd_name, desc, cmd_in, cmd_out, execlevel, params, ret_type)
