import typing

import System
import System.CodeDom.Compiler
import System.IO
import System.Text


class GeneratedCodeAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Tool(self) -> str:
        ...

    @property
    def Version(self) -> str:
        ...

    def __init__(self, tool: str, version: str) -> None:
        ...


class IndentedTextWriter(System.IO.TextWriter):
    """This class has no documentation."""

    DefaultTabString: str = "    "

    @property
    def Encoding(self) -> System.Text.Encoding:
        ...

    @property
    def NewLine(self) -> str:
        ...

    @NewLine.setter
    def NewLine(self, value: str):
        ...

    @property
    def Indent(self) -> int:
        ...

    @Indent.setter
    def Indent(self, value: int):
        ...

    @property
    def InnerWriter(self) -> System.IO.TextWriter:
        ...

    @typing.overload
    def __init__(self, writer: System.IO.TextWriter) -> None:
        ...

    @typing.overload
    def __init__(self, writer: System.IO.TextWriter, tabString: str) -> None:
        ...

    def Close(self) -> None:
        ...

    def Flush(self) -> None:
        ...

    def OutputTabs(self) -> None:
        """This method is protected."""
        ...

    @typing.overload
    def Write(self, s: str) -> None:
        ...

    @typing.overload
    def Write(self, value: bool) -> None:
        ...

    @typing.overload
    def Write(self, value: str) -> None:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[str]) -> None:
        ...

    @typing.overload
    def Write(self, buffer: typing.List[str], index: int, count: int) -> None:
        ...

    @typing.overload
    def Write(self, value: float) -> None:
        ...

    @typing.overload
    def Write(self, value: float) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: int) -> None:
        ...

    @typing.overload
    def Write(self, value: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, arg0: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, arg0: typing.Any, arg1: typing.Any) -> None:
        ...

    @typing.overload
    def Write(self, format: str, *arg: typing.Any) -> None:
        ...

    def WriteLineNoTabs(self, s: str) -> None:
        ...

    @typing.overload
    def WriteLine(self, s: str) -> None:
        ...

    @typing.overload
    def WriteLine(self) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: bool) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: str) -> None:
        ...

    @typing.overload
    def WriteLine(self, buffer: typing.List[str]) -> None:
        ...

    @typing.overload
    def WriteLine(self, buffer: typing.List[str], index: int, count: int) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: float) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: float) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: int) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: int) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, format: str, arg0: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, format: str, arg0: typing.Any, arg1: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, format: str, *arg: typing.Any) -> None:
        ...

    @typing.overload
    def WriteLine(self, value: int) -> None:
        ...


