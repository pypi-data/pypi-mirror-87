import typing

import System
import System.Runtime.Versioning

System_Runtime_Versioning_FrameworkName = typing.Any


class ResourceScope(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    Machine = ...

    Process = ...

    AppDomain = ...

    Library = ...

    Private = ...

    Assembly = ...


class ResourceConsumptionAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def ResourceScope(self) -> System.Runtime.Versioning.ResourceScope:
        ...

    @property
    def ConsumptionScope(self) -> System.Runtime.Versioning.ResourceScope:
        ...

    @typing.overload
    def __init__(self, resourceScope: System.Runtime.Versioning.ResourceScope) -> None:
        ...

    @typing.overload
    def __init__(self, resourceScope: System.Runtime.Versioning.ResourceScope, consumptionScope: System.Runtime.Versioning.ResourceScope) -> None:
        ...


class FrameworkName(System.Object, System.IEquatable[System_Runtime_Versioning_FrameworkName]):
    """This class has no documentation."""

    @property
    def Identifier(self) -> str:
        ...

    @property
    def Version(self) -> System.Version:
        ...

    @property
    def Profile(self) -> str:
        ...

    @property
    def FullName(self) -> str:
        ...

    @typing.overload
    def Equals(self, obj: System.Object) -> bool:
        ...

    @typing.overload
    def Equals(self, other: System.Runtime.Versioning.FrameworkName) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...

    def ToString(self) -> str:
        ...

    @typing.overload
    def __init__(self, identifier: str, version: System.Version) -> None:
        ...

    @typing.overload
    def __init__(self, identifier: str, version: System.Version, profile: str) -> None:
        ...

    @typing.overload
    def __init__(self, frameworkName: str) -> None:
        ...


class TargetFrameworkAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def FrameworkName(self) -> str:
        ...

    @property
    def FrameworkDisplayName(self) -> str:
        ...

    @FrameworkDisplayName.setter
    def FrameworkDisplayName(self, value: str):
        ...

    def __init__(self, frameworkName: str) -> None:
        ...


class ComponentGuaranteesOptions(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    Exchange = ...

    Stable = ...

    SideBySide = ...


class ResourceExposureAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def ResourceExposureLevel(self) -> System.Runtime.Versioning.ResourceScope:
        ...

    def __init__(self, exposureLevel: System.Runtime.Versioning.ResourceScope) -> None:
        ...


class ComponentGuaranteesAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def Guarantees(self) -> System.Runtime.Versioning.ComponentGuaranteesOptions:
        ...

    def __init__(self, guarantees: System.Runtime.Versioning.ComponentGuaranteesOptions) -> None:
        ...


class VersioningHelper(System.Object):
    """This class has no documentation."""

    @staticmethod
    @typing.overload
    def MakeVersionSafeName(name: str, _from: System.Runtime.Versioning.ResourceScope, to: System.Runtime.Versioning.ResourceScope) -> str:
        ...

    @staticmethod
    @typing.overload
    def MakeVersionSafeName(name: str, _from: System.Runtime.Versioning.ResourceScope, to: System.Runtime.Versioning.ResourceScope, type: System.Type) -> str:
        ...


