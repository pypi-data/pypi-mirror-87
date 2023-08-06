"""
[![NPM version](https://badge.fury.io/js/alps-unified-ts.svg)](https://badge.fury.io/js/alps-unified-ts)
[![PyPI version](https://badge.fury.io/py/alps-unified-ts.svg)](https://badge.fury.io/py/alps-unified-ts)
![Release](https://github.com/mmuller88/alps-unified-ts/workflows/Release/badge.svg)

# alps-unified-ts

That is an enhanced TypeScript library of [alps-unified](https://github.com/mamund/alps-unified).

Very useful to understand the idea of ALPS API is this video on YouTube: https://www.youtube.com/watch?v=oG6-r3UdenE

Want to know more about ALPS? --> please visit:

* http://alps.io/
* https://github.com/alps-io/
* https://github.com/mamund/alps-unified

# Thanks to

* The AWS CDK Community for the repo tool [projen](https://github.com/projen/projen) which I use for this repo.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *


class Alps(metaclass=jsii.JSIIMeta, jsii_type="alps-unified-ts.Alps"):
    def __init__(self) -> None:
        jsii.create(Alps, self, [])

    @jsii.member(jsii_name="unified")
    @builtins.classmethod
    def unified(
        cls,
        alps_document: builtins.str,
        *,
        format_type: "FormatType",
    ) -> typing.Any:
        """Converts an ALPS spec JSON object into a specified API like openApi or graph ql schema.

        :param alps_document: The ALPS spec in json.
        :param format_type: 

        :return: the requested api
        """
        options = ConvertOptions(format_type=format_type)

        return jsii.sinvoke(cls, "unified", [alps_document, options])


@jsii.data_type(
    jsii_type="alps-unified-ts.ConvertOptions",
    jsii_struct_bases=[],
    name_mapping={"format_type": "formatType"},
)
class ConvertOptions:
    def __init__(self, *, format_type: "FormatType") -> None:
        """Convert option.

        So far only the format type

        :param format_type: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "format_type": format_type,
        }

    @builtins.property
    def format_type(self) -> "FormatType":
        result = self._values.get("format_type")
        assert result is not None, "Required property 'format_type' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConvertOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="alps-unified-ts.FormatType")
class FormatType(enum.Enum):
    """Format type to convert the ALPS spec into."""

    S = "S"
    SDL = "SDL"
    A = "A"
    ASYNC = "ASYNC"
    ASYNCAPI = "ASYNCAPI"
    O = "O"
    OAS = "OAS"
    OPEN = "OPEN"
    OPENAPI = "OPENAPI"
    P = "P"
    PROTO = "PROTO"
    J = "J"
    JSON = "JSON"
    W = "W"
    WSDL = "WSDL"
    SOAP = "SOAP"


__all__ = [
    "Alps",
    "ConvertOptions",
    "FormatType",
]

publication.publish()
