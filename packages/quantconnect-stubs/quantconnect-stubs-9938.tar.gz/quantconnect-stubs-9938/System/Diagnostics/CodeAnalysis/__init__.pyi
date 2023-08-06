import System
import System.Diagnostics.CodeAnalysis


class SuppressMessageAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Category(self) -> str:
        ...

    @property
    def CheckId(self) -> str:
        ...

    @property
    def Scope(self) -> str:
        ...

    @Scope.setter
    def Scope(self, value: str):
        ...

    @property
    def Target(self) -> str:
        ...

    @Target.setter
    def Target(self, value: str):
        ...

    @property
    def MessageId(self) -> str:
        ...

    @MessageId.setter
    def MessageId(self, value: str):
        ...

    @property
    def Justification(self) -> str:
        ...

    @Justification.setter
    def Justification(self, value: str):
        ...

    def __init__(self, category: str, checkId: str) -> None:
        ...


class RequiresUnreferencedCodeAttribute(System.Attribute):
    """
    Indicates that the specified method requires dynamic access to code that is not referenced
    statically, for example through System.Reflection.
    """

    @property
    def Message(self) -> str:
        """Gets a message that contains information about the usage of unreferenced code."""
        ...

    @property
    def Url(self) -> str:
        """
        Gets or sets an optional URL that contains more information about the method,
        why it requries unreferenced code, and what options a consumer has to deal with it.
        """
        ...

    @Url.setter
    def Url(self, value: str):
        """
        Gets or sets an optional URL that contains more information about the method,
        why it requries unreferenced code, and what options a consumer has to deal with it.
        """
        ...

    def __init__(self, message: str) -> None:
        """
        Initializes a new instance of the RequiresUnreferencedCodeAttribute class
        with the specified message.
        
        :param message: A message that contains information about the usage of unreferenced code.
        """
        ...


