import abc
import datetime
import typing

import QuantConnect.Benchmarks
import QuantConnect.Securities
import System


class IBenchmark(metaclass=abc.ABCMeta):
    """Specifies how to compute a benchmark for an algorithm"""

    def Evaluate(self, time: datetime.datetime) -> float:
        """
        Evaluates this benchmark at the specified time
        
        :param time: The time to evaluate the benchmark at
        :returns: The value of the benchmark at the specified time.
        """
        ...


class FuncBenchmark(System.Object, QuantConnect.Benchmarks.IBenchmark):
    """Creates a benchmark defined by a function"""

    def __init__(self, benchmark: typing.Callable[[datetime.datetime], float]) -> None:
        """
        Initializes a new instance of the FuncBenchmark class
        
        :param benchmark: The functional benchmark implementation
        """
        ...

    def Evaluate(self, time: datetime.datetime) -> float:
        """
        Evaluates this benchmark at the specified time
        
        :param time: The time to evaluate the benchmark at
        :returns: The value of the benchmark at the specified time.
        """
        ...


class SecurityBenchmark(System.Object, QuantConnect.Benchmarks.IBenchmark):
    """Creates a benchmark defined by the closing price of a Security instance"""

    @property
    def Security(self) -> QuantConnect.Securities.Security:
        """The benchmark security"""
        ...

    def __init__(self, security: QuantConnect.Securities.Security) -> None:
        """Initializes a new instance of the SecurityBenchmark class"""
        ...

    def Evaluate(self, time: datetime.datetime) -> float:
        """
        Evaluates this benchmark at the specified time in units of the account's currency.
        
        :param time: The time to evaluate the benchmark at
        :returns: The value of the benchmark at the specified time in units of the account's currency.
        """
        ...


