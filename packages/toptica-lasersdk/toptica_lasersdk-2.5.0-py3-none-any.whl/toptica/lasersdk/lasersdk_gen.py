#!/usr/bin/python3

import argparse
import asyncio
import collections
import ipaddress
import keyword
import os
import socket
import sys
import urllib.error
import urllib.request

from datetime import datetime
from textwrap import dedent

from typing import List
from typing import Optional
from typing import Tuple
from typing import Dict
from typing import Set

from .decop import UserLevel
from .decop import ParamMode
from .decop import Parameter
from .decop import StreamType
from .decop import SystemModel
from .decop import Typedef

from .asyncio.connection import NetworkConnection

TypeNameMap = Dict[Tuple[str, UserLevel, UserLevel], str]
UserLevelMap = Dict[str, Set[Tuple[UserLevel, UserLevel]]]


def download_system_xml(ip_or_name: str) -> Tuple[str, Optional[str]]:
    """Downloads a DeCoP system model from a device.

    Args:
        ip_or_name (str): The IP address or name of the device.

    Returns:
        Optional[str]: An XML description of the DeCoP system model.

    """
    try:
        host = ipaddress.ip_address(ip_or_name)
    except ValueError:
        try:
            host = ipaddress.ip_address(socket.gethostbyname(ip_or_name))
        except (ValueError, OSError):
            net = NetworkConnection('')
            print("Searching for device '{}'...".format(ip_or_name))
            host, _, _ = asyncio.get_event_loop().run_until_complete(net.find_device(ip_or_name))
            if host is None:
                print("Host not found: '{}'".format(ip_or_name))
                return '', None

    url = 'http://{}/system.xml'.format(host)

    try:
        print("Downloading system model from {}...".format(url))
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError as ex:
        print("Unable to download: '{}'".format(ex))
        return url, None

    return url, response.read().decode('utf-8')


def make_parameter(param: Parameter, typenames: TypeNameMap, readlevel: UserLevel, writelevel: UserLevel, ul: UserLevel) -> Tuple[str, str]:
    """Infers the actual name and type for a parameter depending on the required user levels.

    Args:
        param (Parameter): A DeCoP system model parameter.
        typenames (TypeNameMap): A list of type name substitutions.
        readlevel (UserLevel): The required user level to read the parameter.
        writelevel (UserLevel): The required user level to write the parameter.
        ul (UserLevel): The highest user level for which code will be generated.

    Returns:
        Tuple[str, str]: A tuple containing the inferred name and type of the parameter.

    """
    _readlevel = readlevel if param.readlevel is None or param.readlevel > readlevel else param.readlevel
    _writelevel = writelevel if param.writelevel is None or param.writelevel > writelevel else param.writelevel

    is_readable = param.mode != ParamMode.WRITEONLY and _readlevel >= min(ul, UserLevel.NORMAL)
    is_writeable = param.mode != ParamMode.READONLY and _writelevel >= ul

    py_name, py_type = None, None

    if is_readable:
        py_name = make_name(param.name)
        if is_scalar_type(param.paramtype):
            py_type = make_type(param.paramtype, is_readable, is_writeable)
        else:
            py_type = make_type(typenames[(param.paramtype, _readlevel, _writelevel)], is_readable, is_writeable)

    return py_name, py_type


def infer_access(param: Parameter, user_level: int) -> Tuple[bool, bool]:
    """Tests if a parameter is readable and/or writeable.

    Args:
        param (Parameter): The parameter to test.
        user_level (UserLevel): The user level to test for.

    Returns:
        Tuple[bool, bool]: A tuple of two boolean values that are true if the parameter is readable/writeable

    """
    if param.readlevel is not None:
        is_readable = param.readlevel >= user_level and param.mode != ParamMode.WRITEONLY
    else:
        is_readable = UserLevel.NORMAL >= user_level and param.mode != ParamMode.WRITEONLY

    if param.writelevel is not None:
        is_writeable = param.writelevel >= user_level and param.mode != ParamMode.READONLY
    else:
        is_writeable = UserLevel.NORMAL >= user_level and param.mode != ParamMode.READONLY

    return is_readable, is_writeable


def make_stream_type(stream_type: Optional[StreamType]) -> str:
    """Converts a stream type to a Python type string.

    Args:
        stream_type (Optional[StreamType]): The type of the data stream.

    Returns:
        str: A string containing a Python type.

    """
    mapping = {StreamType.TEXT: 'str', StreamType.BASE64: 'bytes'}

    try:
        return mapping[stream_type]
    except KeyError:
        return 'None'


def make_type(name: str, is_readable: bool = True, is_writeable: bool = True) -> str:
    """Converts a DeCoP type name to a Python type name.

    Args:
        name (str): The name of the parameter.
        is_readable (bool): True if the parameter is readable, false otherwise.
        is_writeable (bool):  True if the parameter is writeable, false otherwise.

    Returns:
        str: A string containing the Python type name.

    """
    if name.lower() == 'integer':
        if is_readable and is_writeable:
            return 'MutableDecopInteger'
        if is_readable:
            return 'DecopInteger'

    if name.lower() == 'real':
        if is_readable and is_writeable:
            return 'MutableDecopReal'
        if is_readable:
            return 'DecopReal'

    if name.lower() == 'boolean':
        if is_readable and is_writeable:
            return 'MutableDecopBoolean'
        if is_readable:
            return 'DecopBoolean'

    if name.lower() == 'string':
        if is_readable and is_writeable:
            return 'MutableDecopString'
        if is_readable:
            return 'DecopString'

    if name.lower() == 'binary':
        if is_readable and is_writeable:
            return 'MutableDecopBinary'
        if is_readable:
            return 'DecopBinary'

    name = name.title()

    for c in '-#*%.:':
        name = name.replace(c, '')

    if keyword.iskeyword(name):
        return name + '_'

    return name


def make_name(name: str) -> str:
    """Generates a valid Python name from a system model name.

    Args:
        name (str): The system model name.

    Returns:
        str: The generated name.

    """
    for c in '-#*%.:':
        name = name.replace(c, '_')

    if keyword.iskeyword(name):
        return name + '_'

    if name == 'id':
        return 'id_'
    if name == 'type':
        return 'type_'

    return name


def make_cmd_type(typename: Optional[str]) -> str:
    """Translates a DeCoP parameter type name to a Python type name for commands.

    Args:
        typename: A system model parameter type (e.g. 'BOOLEAN').

    Returns:
        str:  A string containing a Python type name (e.g. 'bool').

    """
    try:
        mapping = {'integer': 'int', 'real': 'float', 'boolean': 'bool', 'string': 'str', 'binary': 'bytes'}
        return mapping[typename.lower()]
    except (AttributeError, KeyError):
        return 'None'


def is_scalar_type(param_type: str) -> bool:
    """Tests if a parameter type is a scalar DeCoP value (e.g. boolean).

    Args:
        param_type (str): The type name of the parameter.

    Returns:
        bool: True if the type is scalar, false if it is complex.

    """
    return param_type.lower() in {'boolean', 'integer', 'real', 'string', 'binary'}


def is_accessible(param: Parameter, ul: UserLevel) -> bool:
    """Tests if a parameter is accessible at the specified user level.

    Args:
        param (Parameter): A DeCoP parameter.
        ul (UserLevel): The highest user level for which code will be generated.

    Returns:
        bool: True if the parameter is accessible, false otherwise.

    """
    if param.mode != ParamMode.WRITEONLY and param.readlevel >= min(ul, UserLevel.NORMAL):
        return True
    if param.mode != ParamMode.READONLY and param.writelevel >= ul:
        return True
    return False


def infer_type_names_helper(model: SystemModel, user_levels: UserLevelMap, typedef: Typedef, readlevel: UserLevel, writelevel: UserLevel, ul: UserLevel) -> None:
    """Recursively walks

    Args:
        model (SystemModel): A DeCoP system model.
        user_levels (UserLevelMap): A list of user levels every type uses.
        typedef (Typedef): A DeCoP typedef.
        readlevel (UserLevel): The currently required user level to read a parameter.
        writelevel (UserLevel): The currently required user level to write a parameter.
        ul (UserLevel): The highest user level for which code will be generated.

    """
    for param in typedef.params.values():
        # Inherit or limit user levels if necessary
        _readlevel = readlevel if param.readlevel is None or param.readlevel > readlevel else param.readlevel
        _writelevel = writelevel if param.writelevel is None or param.writelevel > writelevel else param.writelevel

        if param.mode is None:
            param.mode = ParamMode.READWRITE

        if (param.mode != ParamMode.WRITEONLY and _readlevel >= min(ul, UserLevel.NORMAL)) or (param.mode != ParamMode.READONLY and _writelevel >= ul):
            if not is_scalar_type(param.paramtype):
                user_levels[param.paramtype].add((_readlevel, _writelevel))
                infer_type_names_helper(model, user_levels, model.typedefs[param.paramtype], _readlevel, _writelevel, ul)


def infer_type_names(model: SystemModel, ul: UserLevel) -> TypeNameMap:
    """Generates a list of unique type names for all typedefs depending on the user levels.

    Args:
        model (SystemModel): A DeCoP system model.
        ul (UserLevel): The highest user level for which code will be generated.

    Returns:
        TypeNameMap: A list of type name substitutions.

    """
    user_levels = collections.defaultdict(set)  # type: UserLevelMap

    # Infer the used user levels for all used typedef
    for node in model.modules.values():
        for param in node.params.values():
            if not is_scalar_type(param.paramtype) and is_accessible(param, ul):
                user_levels[param.paramtype].add((param.readlevel, param.writelevel))
                infer_type_names_helper(model, user_levels, model.typedefs[param.paramtype], param.readlevel, param.writelevel, ul)

    result = {}  # type: TypeNameMap

    # Generate a unique name for each typedef and user level
    for typename, userlevel_list in user_levels.items():
        if len(userlevel_list) == 1:
            for entry in userlevel_list:
                readlevel, writelevel = entry[0], entry[1]
                result[(typename, readlevel, writelevel)] = typename
        else:
            for entry, i in zip(userlevel_list, range(len(userlevel_list))):
                readlevel, writelevel = entry[0], entry[1]
                result[(typename, readlevel, writelevel)] = typename + str(i + 1)

    return result


def generate_change_ul(use_async: bool) -> str:
    """Generate the special 'change-ul' command.

    Args:
        use_async (bool): True if asynchronous code should be generated, false otherwise.

    Returns:
        str: A string containing the Python code for the 'change-ul' command.

    """
    result = ""

    result += "    {_async}def change_ul(self, ul: UserLevel, passwd: str) -> int:\n".format(_async='async ' if use_async else '')
    result += "        assert isinstance(ul, UserLevel), \"expected type 'UserLevel' for parameter 'ul', got '{}'\".format(type(ul))\n"
    result += "        assert isinstance(passwd, str), \"expected type 'str' for parameter 'passwd', got '{}'\".format(type(passwd))\n"
    result += "        return {_await}self.__client.change_ul(ul, passwd)".format(_await='await ' if use_async else '')

    return result


def generate_cmd(name: str, params: List[Tuple[str, str]], return_type: Optional[str], input_type: Optional[StreamType], output_type: Optional[StreamType], use_async: bool, is_typedef_cmd: bool) -> str:
    """Generates a Python class method for a system model command.

    Args:
        name (str): The name of the system model command.
        params (List[Tuple[str, str]]): A list of parameter names and types of the command e.g. [('ul', 'int'), ('passwd', 'str')]
        return_type (Optional[str]): A string of the python return type or None e.g. 'int'.
        input_type (Optional[StreamType]): The type of the input stream data.
        output_type (Optional[StreamType]): The type of the output stream data.
        use_async (bool): True if asynchronous code should be generated, false otherwise.
        is_typedef_cmd (bool): True if this command is part of a typedef, False if this command is part of the device class.

    Returns:
        str: A string containing the Python code for the class method.

    """
    _async = 'async ' if use_async else ''
    _await = 'await ' if use_async else ''

    result = "    {_async}def {name}(self".format(_async=_async, name=make_name(name))

    if input_type is not None:
        result += ", input_stream: {type}".format(type=make_stream_type(input_type))

    for param_name, param_type in params:
        result += ", {name}: {type}".format(name=make_name(param_name), type=make_cmd_type(param_type))

    if return_type is not None and output_type is not None:
        result += ") -> Tuple[{stream}, {result}]:\n".format(stream=make_stream_type(output_type), result=make_cmd_type(return_type))
    elif return_type is not None:
        result += ") -> {result}:\n".format(result=make_cmd_type(return_type))
    elif output_type is not None:
        result += ") -> {stream}:\n".format(stream=make_stream_type(output_type))
    else:
        result += ") -> None:\n"

    if input_type is not None:
        result += "        assert isinstance(input_stream, {type}), \"expected type '{type}' for parameter 'input_stream', got '{{}}'\".format(type(input_stream))\n".format(type=make_stream_type(input_type))

    for param_name, param_type in params:
        result += "        assert isinstance({name}, {type}), \"expected type '{type}' for parameter '{name}', got '{{}}'\".format(type({name}))\n".format(name=make_name(param_name), type=make_cmd_type(param_type))

    cmd_name = "self.__name + ':" + name + "'" if is_typedef_cmd else "'" + name + "'"

    if output_type is not None or return_type is not None:
        result += "        return {_await}self.__client.exec({name}".format(_await=_await, name=cmd_name)
    else:
        result += "        {_await}self.__client.exec({name}".format(_await=_await, name=cmd_name)

    # Generate remaining parameters
    for param_name, _ in params:
        result += ', ' + make_name(param_name)

    # Input stream parameter
    result += ", input_stream=input_stream" if input_type else ", input_stream=None"

    result += ", output_type=" + make_stream_type(output_type)
    result += ", return_type=" + make_cmd_type(return_type)

    result += ')'

    return result


def generate_param_getter(param_name: str, param_type: str) -> str:
    """Generates Python code for a parameter getter.

    Args:
        param_name: The name of the parameter
        param_type: The type of the parameter.

    Returns:
        str: Python code for the parameter getter.

    """
    return "    @property\n" \
           "    def " + param_name + "(self) -> '" + param_type + "':\n" \
           "        return self._" + param_name + "\n\n"


def generate_device_class(system_model: SystemModel, typenames: TypeNameMap, ul: UserLevel, use_async: bool) -> str:
    """Generate the main class for the device.

    Args:
        system_model (SystemModel): A DeCoP system model.
        typenames (TypeNameMap): A list of type name substitutions.
        ul (UserLevel): The highest user level for which code will be generated.
        use_async (bool): True if asynchronous code should be generated, false otherwise.

    Returns:
        str: The Python code for the device class.

    """
    result = "class " + system_model.name + ":\n" \
             "    def __init__(self, connection: Connection) -> None:\n" \
             "        self.__client = Client(connection)\n"

    # Generate initializers for module parameters
    for node in system_model.modules.values():
        for param in node.params.values():
            py_name, py_type = make_parameter(param, typenames, param.readlevel, param.writelevel, ul)
            if py_name is not None:
                result += "        self._" + py_name + " = " + py_type + "(self.__client, '" + param.name + "')\n"

    # Generate general methods for the device class (open, close, etc.)
    result += generate_device_class_methods(use_async)

    # Generate parameter properties
    for node in system_model.modules.values():
        for param in node.params.values():
            py_name, py_type = make_parameter(param, typenames, param.readlevel, param.writelevel, ul)
            if py_name is not None:
                result += generate_param_getter(py_name, py_type)

    # Generate module commands
    if ul <= UserLevel.NORMAL:
        for node in system_model.modules.values():
            for cmd in node.cmds.values():
                if (cmd.execlevel is None and ul <= UserLevel.NORMAL) or cmd.execlevel >= ul:
                    if cmd.name == 'change-ul':
                        result += generate_change_ul(use_async)
                    else:
                        result += generate_cmd(cmd.name, cmd.params, cmd.return_type, cmd.input_type, cmd.output_type, use_async, is_typedef_cmd=False)
                    result += '\n\n'

    return result


def generate_typedef(typedef: Typedef, typenames: TypeNameMap, readlevel: UserLevel, writelevel: UserLevel, ul: UserLevel, use_async: bool) -> str:
    """Generates a Python class for a system model typedef.

    Args:
        typedef (Typedef): A DeCoP typedef.
        typenames (TypeNameMap): A list of type name substitutions.
        readlevel (UserLevel): The required user level to read a parameter.
        writelevel (UserLevel): The required user level to write a parameter.
        ul (UserLevel): The highest user level for which code will be generated.
        use_async (bool): True if asynchronous code should be generated, false otherwise.

    Returns:
        str: The Python code for the typedef.

    """
    unique_name = typenames[(typedef.name, readlevel, writelevel)]

    result = ""
    result += "class " + make_type(unique_name) + ":\n"
    result += "    def __init__(self, client: Client, name: str) -> None:\n"
    result += "        self.__client = client\n"
    result += "        self.__name = name\n"

    # Generate member variables
    for param in typedef.params.values():
        py_name, py_type = make_parameter(param, typenames, readlevel, writelevel, ul)
        if py_name is not None:
            result += "        self._" + py_name + " = " + py_type + "(client, name + ':" + param.name + "')\n"

    result += "\n"

    # Generate parameter properties
    for param in typedef.params.values():
        py_name, py_type = make_parameter(param, typenames, readlevel, writelevel, ul)
        if py_name is not None:
            result += generate_param_getter(py_name, py_type)

    # Generate command implementations
    if ul <= UserLevel.NORMAL:
        for cmd in typedef.cmds.values():
            if cmd.execlevel is None:
                if ul <= writelevel:
                    result += generate_cmd(cmd.name, cmd.params, cmd.return_type, cmd.input_type, cmd.output_type, use_async, is_typedef_cmd=True)
                    result += '\n\n'
            else:
                _exec = min(cmd.execlevel, writelevel)
                if _exec >= ul:
                    result += generate_cmd(cmd.name, cmd.params, cmd.return_type, cmd.input_type, cmd.output_type, use_async, is_typedef_cmd=True)
                    result += '\n\n'

    return result + "\n"


def generate_atomic_typedef(typedef: Typedef, typenames: TypeNameMap, readlevel: UserLevel, writelevel: UserLevel, ul: UserLevel, use_async: bool) -> str:
    """Generates a Python class for a system model atomic typedef.

    Args:
        typedef (Typedef): A DeCoP typedef.
        typenames (TypeNameMap): A list of type name substitutions.
        readlevel (UserLevel): The required user level to read a parameter.
        writelevel (UserLevel): The required user level to write a parameter.
        ul (UserLevel): The highest user level for which code will be generated.
        use_async (bool): True if asynchronous code should be generated, false otherwise.

    Returns:
        str: The Python code for the typedef.

    """
    unique_name = typenames[(typedef.name, readlevel, writelevel)]

    source = "class " + make_type(unique_name) + ":\n" \
             "    def __init__(self, client: Client, name: str) -> None:\n" \
             "        self.__client = client\n" \
             "        self.__name = name\n\n"

    _async = 'async ' if use_async else ''
    _await = 'await ' if use_async else ''

    # Getter
    type_list = [make_cmd_type(x.paramtype) for x in typedef.params.values()]

    source += "    {}def get(self) -> Tuple[".format(_async) + ', '.join(type_list) + "]:\n"
    source += "        return {}self.__client.get(self.__name)\n\n".format(_await)

    # Setter
    tmpl0 = "    {prefix}def set(self, {param_list}) -> None:\n"
    tmpl1 = "        assert isinstance({x}, {type}), \"expected type '{type}' for '{x}', got '{{}}'\".format(type({x}))\n"
    tmpl2 = "        {prefix}self.__client.set(self.__name, {param_names})\n\n"

    param_list = [make_name(x.name) + ': ' + make_cmd_type(x.paramtype) for x in typedef.params.values()]
    source += tmpl0.format(prefix=_async, param_list=', '.join(param_list))

    for param in typedef.params.values():
        source += tmpl1.format(x=make_name(param.name), type=make_cmd_type(param.paramtype))

    source += tmpl2.format(prefix=_await, param_names=', '.join([make_name(x.name) for x in typedef.params.values()]))

    # Commands
    if ul <= UserLevel.NORMAL:
        for cmd in typedef.cmds.values():
            if cmd.execlevel is None:
                if ul <= writelevel:
                    source += generate_cmd(cmd.name, cmd.params, cmd.return_type, cmd.input_type, cmd.output_type, use_async, is_typedef_cmd=True)
                    source += '\n\n'
            else:
                _exec = min(cmd.execlevel, writelevel)
                if _exec >= ul:
                    source += generate_cmd(cmd.name, cmd.params, cmd.return_type, cmd.input_type, cmd.output_type, use_async, is_typedef_cmd=True)
                    source += '\n\n'

    return source + "\n"


def generate_typedefs_helper(model: SystemModel, typedef: Typedef, typenames: TypeNameMap, generated_types, readlevel: UserLevel, writelevel: UserLevel, ul: UserLevel, use_async: bool) -> str:

    result = ''

    for param in typedef.params.values():
        # Inherit or limit user levels if necessary
        _readlevel = readlevel if param.readlevel is None or param.readlevel > readlevel else param.readlevel
        _writelevel = writelevel if param.writelevel is None or param.writelevel > writelevel else param.writelevel

        if (param.mode != ParamMode.WRITEONLY and _readlevel >= min(ul, UserLevel.NORMAL)) or (param.mode != ParamMode.READONLY and _writelevel >= ul):
            if not is_scalar_type(param.paramtype):
                typedef = model.typedefs[param.paramtype]
                name = typenames[(param.paramtype, _readlevel, _writelevel)]

                if name not in generated_types:
                    if typedef.is_atomic:
                        result += generate_atomic_typedef(typedef, typenames, _readlevel, _writelevel, ul, use_async)
                    else:
                        result += generate_typedef(typedef, typenames, _readlevel, _writelevel, ul, use_async)

                    generated_types.append(name)

                    result += generate_typedefs_helper(model, model.typedefs[param.paramtype], typenames, generated_types, _readlevel, _writelevel, ul, use_async)

    return result


def generate_typedefs(model: SystemModel, typenames: TypeNameMap, ul: UserLevel, use_async: bool) -> str:
    """Generate Python code for all typedefs in the system model.

    Args:
        model (SystemModel): A DeCoP system model.
        typenames (TypeNameMap): A list of type name substitutions.
        ul (UserLevel): The highest user level for which code will be generated.
        use_async (bool): True if asynchronous code should be generated, false otherwise.

    Returns:
        str: The generated Python code for all typedefs.

    """
    result = str()
    generated_types = []

    for node in model.modules.values():
        for param in node.params.values():
            if not is_scalar_type(param.paramtype) and is_accessible(param, ul):
                typedef = model.typedefs[param.paramtype]
                name = typenames[(param.paramtype, param.readlevel, param.writelevel)]

                if name not in generated_types:
                    if typedef.is_atomic:
                        result += generate_atomic_typedef(typedef, typenames, param.readlevel, param.writelevel, ul, use_async)
                    else:
                        result += generate_typedef(typedef, typenames, param.readlevel, param.writelevel, ul, use_async)

                    generated_types.append(name)

                    result += generate_typedefs_helper(model, typedef, typenames, generated_types, param.readlevel, param.writelevel, ul, use_async)

    return result


def generate_device_class_methods(use_async: bool) -> str:
    """Generates the default methods for a device class.

    Args:
        use_async (bool): True if asynchronous code should be generated, false otherwise.

    Returns:
        str: The Python code for the default methods of a device class.

    """
    if use_async:
        return """
    def __enter__(self):
        return self

    def __exit__(self):
        raise RuntimeError()

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, *args):
        await self.close()

    def __await__(self):
        return self.__aenter__().__await__()

    async def open(self) -> None:
        await self.__client.open()

    async def close(self) -> None:
        await self.__client.close()

"""
    else:
        return """
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def open(self) -> None:
        self.__client.open()

    def close(self) -> None:
        self.__client.close()

    def run(self, timeout: int = None) -> None:
        self.__client.run(timeout)

    def stop(self) -> None:
        self.__client.stop()

    def poll(self) -> None:
        self.__client.poll()

"""


def generate_header(model_name: str, use_async: bool) -> str:
    """Generates the header for a Python module.

    Args:
        model_name (str): The name of the system model the header is generated for.
        use_async (bool): True if asynchronous code should be generated, false otherwise.

    Returns:
        str: The Python code for the header.


    """
    return dedent("""\
        # Generated from '{model}' on {date}

        from typing import Tuple

        from toptica.lasersdk.{_async}client import UserLevel
        from toptica.lasersdk.{_async}client import Client

        from toptica.lasersdk.{_async}client import DecopBoolean
        from toptica.lasersdk.{_async}client import DecopInteger
        from toptica.lasersdk.{_async}client import DecopReal
        from toptica.lasersdk.{_async}client import DecopString
        from toptica.lasersdk.{_async}client import DecopBinary

        from toptica.lasersdk.{_async}client import MutableDecopBoolean
        from toptica.lasersdk.{_async}client import MutableDecopInteger
        from toptica.lasersdk.{_async}client import MutableDecopReal
        from toptica.lasersdk.{_async}client import MutableDecopString
        from toptica.lasersdk.{_async}client import MutableDecopBinary

        from toptica.lasersdk.{_async}client import Connection
        from toptica.lasersdk.{_async}client import NetworkConnection
        from toptica.lasersdk.{_async}client import SerialConnection

        from toptica.lasersdk.{_async}client import DecopError
        from toptica.lasersdk.{_async}client import DeviceNotFoundError


        """.format(model=model_name, date=str(datetime.now()), _async='asyncio.' if use_async else ''))


def generate_python_module(model_name: str, model_data: str, ul: UserLevel, use_async: bool) -> str:
    """Generates a Python module from a DeCoP system model.

    Args:
        model_name (str): The name of the system model.
        model_data (str): The XML data defining the system model.
        ul (UserLevel): The highest user level for which code will be generated.
        use_async (bool): True if asynchronous code should be generated, false otherwise

    Returns:
        str: The Python code for the module.

    """
    model = SystemModel()
    model.build_from_string(model_data)

    # Include all required types for the module
    result = generate_header(model_name, use_async)

    # Generate unique class names for the typedefs depending on the user level
    typenames = infer_type_names(model, ul)

    # Generate Python classes for all used types
    result += generate_typedefs(model, typenames, ul, use_async)

    # Generate the main class for the device
    result += generate_device_class(model, typenames, ul, use_async)

    return result


def process_command_line(commandline: List[str]):
    """Parse the command line and return a DeCoP model description.

    Args:
        commandline (List[str]): A list of commandline parameters.

    Returns:
        An object containing the parsed command line parameters.

    """
    parser = argparse.ArgumentParser(description='Generate Python code from a DeCoP system description.')

    # Allow naming the generated python module
    description = 'name the generated Python module'
    parser.add_argument('-m', '--module', metavar='name', dest='module_name', nargs=1, help=description)

    # Allow selecting the included elements based on a user level
    description = 'include properties up to this user level'
    parser.add_argument('-ul', '--userlevel', metavar='level', type=int, choices=range(0, 5), dest='ul', nargs=1, help=description)

    # Allow selecting between generating synchronous and asynchronous code
    description = 'generate asynchronous Python code'
    parser.add_argument('-a', '--async', dest='use_async', action='store_true', help=description)

    # Allow selecting between generating synchronous and asynchronous code
    description = 'download system model from a device'
    parser.add_argument('-d', '--download', dest='download', action='store_true', help=description)

    # At least one XML file is required
    parser.add_argument('model_xml', metavar='model_xml', nargs=1, help='DeCoP system description file or device IP address')

    if not commandline:
        # Show the command line help if there weren't any parameters provided
        parser.print_help()
        parser.exit()

    args = parser.parse_args(commandline)

    if args.model_xml:
        # ['model.xml'] -> 'model.xml'
        args.model_xml = args.model_xml[0]

    if args.module_name:
        # ['decop.py'] -> 'decop.py'
        args.module_name = args.module_name[0]

    if args.ul:
        # 3 -> UserLevel.NORMAL
        args.ul = UserLevel(args.ul[0])
    else:
        args.ul = UserLevel.NORMAL

    return args


def main() -> None:
    """Parses the command line and imports a system model if necessary."""

    # Get a list of files to convert or show the command line help
    args = process_command_line(sys.argv[1:])

    if args.module_name:
        # Use the provided module name
        module_name = args.module_name
    else:
        # Replace the model file extension with '.py'
        module_name = os.path.splitext(args.model_xml)[0] + '.py'

        # Replace reserved characters in the filename
        for c in '-<>:"/\\|?*':
            module_name = module_name.replace(c, '_')

    if args.download:
        # Try to download a system model from a device
        model_name, model_data = download_system_xml(args.model_xml)
    else:
        # Try to read a system model from a file
        with open(args.model_xml, 'r', encoding='utf-8') as xml_file:
            model_name = os.path.basename(args.model_xml)
            model_data = xml_file.read()

    if model_name:
        with open(module_name, 'w+') as file:
            file.write(generate_python_module(model_name, model_data, args.ul, args.use_async))


if __name__ == "__main__":
    main()
