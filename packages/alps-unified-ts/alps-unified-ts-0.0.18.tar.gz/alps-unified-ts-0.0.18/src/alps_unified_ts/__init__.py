"""
[![NPM version](https://badge.fury.io/js/alps-unified-ts.svg)](https://badge.fury.io/js/alps-unified-ts)
[![PyPI version](https://badge.fury.io/py/alps-unified-ts.svg)](https://badge.fury.io/py/alps-unified-ts)
[![Maven version](https://maven-badges.herokuapp.com/maven-central/com.github.mmuller88.alpsUnifiedTs/alps-unified-ts/badge.svg)](https://maven-badges.herokuapp.com/maven-central/com.github.mmuller88.alpsUnifiedTs/alps-unified-ts)
[![.NET version](https://img.shields.io/nuget/v/com.github.mmuller88.AlpsUnifiedTs.svg?style=flat-square)](https://www.nuget.org/packages/com.github.mmuller88.AlpsUnifiedTs/)
![Release](https://github.com/mmuller88/alps-unified-ts/workflows/Release/badge.svg)

# alps-unified-ts

That is an enhanced TypeScript library of [alps-unified](https://github.com/mamund/alps-unified). With it you can convert an ALPS API spec to other API spec like openApi, Graph QL Schema.

Very useful to understand the idea of ALPS API is this video on YT: https://www.youtube.com/watch?v=oG6-r3UdenE

Want to know more about ALPS? --> please visit:

* http://alps.io/
* https://github.com/alps-io/
* https://github.com/mamund/alps-unified

# Features

* generating and publishing alps unified libraries for JavaScript, TypeScript, Python, Java and .NET
* Type support for ALPS specs (see example 'Create from Spec' down below)

# Examples

## Load from YAML file

You can load the ALPS spec directly from a YAML file. JSON ist atm not supported.

### Convert to OpenApi

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Alps.unified(Alps.load_yaml("test/todo-alps.yaml"),
    format_type=FormatType.OPENAPI
)
```

### Convert to GraphQL Schema

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Alps.unified(Alps.load_yaml("test/todo-alps.yaml"),
    format_type=FormatType.SDL
)
```

## Create from Spec

Creating the API specification from the spec is very powerful. As it gives you much support in an idea like VS as it is typed and documented. So you alway produce valid API specs.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Alps.unified(
    Alps.spec(
        alps={
            "version": "1.0",
            "doc": {
                "value": "Simple Todo list example"
            },
            "ext": [{
                "type": "metadata",
                "name": "title",
                "value": "simpleTodo",
                "tags": "oas"
            }, {
                "type": "metadata",
                "name": "root",
                "value": "http://api.example.org/todo",
                "tags": "oas"
            }
            ],
            "descriptor": [{
                "id": "id",
                "type": "semantic",
                "text": "storage id of todo item"
            }
            ]
        }
    ))
```

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

    @jsii.member(jsii_name="loadYaml")
    @builtins.classmethod
    def load_yaml(cls, path: builtins.str) -> typing.Any:
        """loads the ALPS document.

        :param path: ALPS spec file path.
        """
        return jsii.sinvoke(cls, "loadYaml", [path])

    @jsii.member(jsii_name="spec")
    @builtins.classmethod
    def spec(cls, *, alps: "AlpsDef") -> "AlpsSpec":
        """
        :param alps: Indicates the root of the ALPS document. This property is REQUIRED, and it SHOULD have one or more 'descriptor' child properties.
        """
        spec = AlpsSpec(alps=alps)

        return jsii.sinvoke(cls, "spec", [spec])

    @jsii.member(jsii_name="unified")
    @builtins.classmethod
    def unified(
        cls,
        alps_document: typing.Any,
        *,
        format_type: "FormatType",
    ) -> builtins.str:
        """Converts an ALPS spec JSON object into a specified API like openApi or graph ql schema.

        :param alps_document: The ALPS document.
        :param format_type: 

        :return: the requested api in string format
        """
        options = ConvertOptions(format_type=format_type)

        return jsii.sinvoke(cls, "unified", [alps_document, options])


@jsii.data_type(
    jsii_type="alps-unified-ts.AlpsDef",
    jsii_struct_bases=[],
    name_mapping={
        "descriptor": "descriptor",
        "doc": "doc",
        "ext": "ext",
        "version": "version",
    },
)
class AlpsDef:
    def __init__(
        self,
        *,
        descriptor: typing.List["DescriptorDef"],
        doc: "DocDef",
        ext: typing.List["ExtDef"],
        version: builtins.str,
    ) -> None:
        """
        :param descriptor: 
        :param doc: 
        :param ext: 
        :param version: can be any string e.g.: 1.0.
        """
        if isinstance(doc, dict):
            doc = DocDef(**doc)
        self._values: typing.Dict[str, typing.Any] = {
            "descriptor": descriptor,
            "doc": doc,
            "ext": ext,
            "version": version,
        }

    @builtins.property
    def descriptor(self) -> typing.List["DescriptorDef"]:
        result = self._values.get("descriptor")
        assert result is not None, "Required property 'descriptor' is missing"
        return result

    @builtins.property
    def doc(self) -> "DocDef":
        result = self._values.get("doc")
        assert result is not None, "Required property 'doc' is missing"
        return result

    @builtins.property
    def ext(self) -> typing.List["ExtDef"]:
        result = self._values.get("ext")
        assert result is not None, "Required property 'ext' is missing"
        return result

    @builtins.property
    def version(self) -> builtins.str:
        """can be any string e.g.: 1.0."""
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlpsDef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="alps-unified-ts.AlpsSpec",
    jsii_struct_bases=[],
    name_mapping={"alps": "alps"},
)
class AlpsSpec:
    def __init__(self, *, alps: AlpsDef) -> None:
        """
        :param alps: Indicates the root of the ALPS document. This property is REQUIRED, and it SHOULD have one or more 'descriptor' child properties.
        """
        if isinstance(alps, dict):
            alps = AlpsDef(**alps)
        self._values: typing.Dict[str, typing.Any] = {
            "alps": alps,
        }

    @builtins.property
    def alps(self) -> AlpsDef:
        """Indicates the root of the ALPS document.

        This property is REQUIRED, and it SHOULD have one or more 'descriptor' child properties.
        """
        result = self._values.get("alps")
        assert result is not None, "Required property 'alps' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlpsSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


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


@jsii.data_type(
    jsii_type="alps-unified-ts.DescriptorDef",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "text": "text",
        "type": "type",
        "descriptor": "descriptor",
        "doc": "doc",
        "href": "href",
        "rt": "rt",
        "tags": "tags",
    },
)
class DescriptorDef:
    def __init__(
        self,
        *,
        id: builtins.str,
        text: builtins.str,
        type: builtins.str,
        descriptor: typing.Optional[typing.List["DescriptorDef"]] = None,
        doc: typing.Optional["DocDef"] = None,
        href: typing.Optional[builtins.str] = None,
        rt: typing.Optional[builtins.str] = None,
        tags: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param id: 
        :param text: 
        :param type: 
        :param descriptor: 
        :param doc: 
        :param href: 
        :param rt: 
        :param tags: 
        """
        if isinstance(doc, dict):
            doc = DocDef(**doc)
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
            "text": text,
            "type": type,
        }
        if descriptor is not None:
            self._values["descriptor"] = descriptor
        if doc is not None:
            self._values["doc"] = doc
        if href is not None:
            self._values["href"] = href
        if rt is not None:
            self._values["rt"] = rt
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return result

    @builtins.property
    def text(self) -> builtins.str:
        result = self._values.get("text")
        assert result is not None, "Required property 'text' is missing"
        return result

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def descriptor(self) -> typing.Optional[typing.List["DescriptorDef"]]:
        result = self._values.get("descriptor")
        return result

    @builtins.property
    def doc(self) -> typing.Optional["DocDef"]:
        result = self._values.get("doc")
        return result

    @builtins.property
    def href(self) -> typing.Optional[builtins.str]:
        result = self._values.get("href")
        return result

    @builtins.property
    def rt(self) -> typing.Optional[builtins.str]:
        result = self._values.get("rt")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[builtins.str]:
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DescriptorDef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="alps-unified-ts.DocDef",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "format": "format", "href": "href"},
)
class DocDef:
    def __init__(
        self,
        *,
        value: builtins.str,
        format: typing.Optional[builtins.str] = None,
        href: typing.Optional[builtins.str] = None,
    ) -> None:
        """A text field that contains free-form, usually human-readable, text.

        The 'doc' element MAY have two properties: 'href' and 'format'.  If
        the 'href' property appears it SHOULD contain a dereferencable URL
        that points to human-readable text.  If the 'format' property appears
        it SHOULD contain one of the following values: 'text', 'html',
        'asciidoc', or 'markdown'.  Any program processing 'doc' elements
        SHOULD honor the 'format' directive and parse/render the content
        appropriately.  If the value in the 'format' property is not
        recognized and/or supported, the processing program MUST treat the
        content as plain text.  If no 'format' property is present, the
        content SHOULD be treated as plain text.
        JSON:  { "doc" : { "format" : "text" , "value" : "Date of Birth ...""} }

        A 'doc' element SHOULD appear as a child of 'descriptor'.  When
        present, it describes the meaning and use of the related 'descriptor'.
        JSON:  { "descriptor" : [ { "doc" : { "value" : "..." } ...  ] }

        The 'doc' element MAY appear as a child of 'alps'.  When present, it
        describes the purpose of the ALPS document as a whole.
        JSON:  { "alps : { "doc" : { "value" : "..." } } ... }

        :param value: 
        :param format: 
        :param href: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "value": value,
        }
        if format is not None:
            self._values["format"] = format
        if href is not None:
            self._values["href"] = href

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return result

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        result = self._values.get("format")
        return result

    @builtins.property
    def href(self) -> typing.Optional[builtins.str]:
        result = self._values.get("href")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DocDef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="alps-unified-ts.ExtDef",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "tags": "tags",
        "type": "type",
        "value": "value",
        "href": "href",
        "id": "id",
    },
)
class ExtDef:
    def __init__(
        self,
        *,
        name: builtins.str,
        tags: builtins.str,
        type: builtins.str,
        value: builtins.str,
        href: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param name: 
        :param tags: 
        :param type: 
        :param value: 
        :param href: 
        :param id: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "tags": tags,
            "type": type,
            "value": value,
        }
        if href is not None:
            self._values["href"] = href
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def tags(self) -> builtins.str:
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return result

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return result

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return result

    @builtins.property
    def href(self) -> typing.Optional[builtins.str]:
        result = self._values.get("href")
        return result

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExtDef(%s)" % ", ".join(
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
    "AlpsDef",
    "AlpsSpec",
    "ConvertOptions",
    "DescriptorDef",
    "DocDef",
    "ExtDef",
    "FormatType",
]

publication.publish()
