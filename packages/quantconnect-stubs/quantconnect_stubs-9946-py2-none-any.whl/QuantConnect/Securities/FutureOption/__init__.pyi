import datetime
import typing

import QuantConnect
import QuantConnect.Securities
import QuantConnect.Securities.FutureOption
import QuantConnect.Securities.Option
import System


class FutureOption(QuantConnect.Securities.Option.Option):
    """Futures Options security"""

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours, quoteCurrency: QuantConnect.Securities.Cash, symbolProperties: QuantConnect.Securities.Option.OptionSymbolProperties, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypes: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider, securityCache: QuantConnect.Securities.SecurityCache) -> None:
        """
        Constructor for the future option security
        
        :param symbol: Symbol of the future option
        :param exchangeHours: Exchange hours of the future option
        :param quoteCurrency: Quoted currency of the future option
        :param symbolProperties: Symbol properties of the future option
        :param currencyConverter: Currency converter
        :param registeredTypes: Provides all data types registered to the algorithm
        :param securityCache: Cache of security objects
        """
        ...


class FuturesOptionsExpiryFunctions(System.Object):
    """Futures options expiry lookup utility class"""

    @staticmethod
    def FuturesOptionExpiry(canonicalFutureOptionSymbol: typing.Union[QuantConnect.Symbol, str], futureContractMonth: datetime.datetime) -> datetime.datetime:
        """
        Gets the Futures Options' expiry for the given contract month.
        
        :param canonicalFutureOptionSymbol: Canonical Futures Options Symbol. Will be made canonical if not provided a canonical
        :param futureContractMonth: Contract month of the underlying Future
        :returns: Expiry date/time.
        """
        ...

    @staticmethod
    def GetFutureContractMonth(canonicalFutureSymbol: typing.Union[QuantConnect.Symbol, str], futureOptionExpirationDate: datetime.datetime) -> datetime.datetime:
        """
        Gets the Future's contract month from a futures options expiry date
        
        :param canonicalFutureSymbol: Canonical Future Symbol
        :param futureOptionExpirationDate: Expiration of the futures option contract
        :returns: Contract month of the future.
        """
        ...

    @staticmethod
    def GetFutureOptionExpiryFromFutureExpiry(futureSymbol: typing.Union[QuantConnect.Symbol, str], canonicalFutureOption: typing.Union[QuantConnect.Symbol, str] = None) -> datetime.datetime:
        """
        Gets the Future Option's expiry from the Future Symbol provided
        
        :param futureSymbol: Future (non-canonical) Symbol
        :returns: Future Option Expiry for the Future with the same contract month.
        """
        ...


class FutureOptionSymbol(System.Object):
    """Static helper methods to resolve Futures Options Symbol-related tasks."""

    @staticmethod
    def IsStandard(_: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Detects if the future option contract is standard, i.e. not weekly, not short-term, not mid-sized, etc.
        
        :param _: Symbol
        :returns: true.
        """
        ...

    @staticmethod
    def GetLastDayOfTrading(symbol: typing.Union[QuantConnect.Symbol, str]) -> datetime.datetime:
        """
        Gets the last day of trading, aliased to be the Futures options' expiry
        
        :param symbol: Futures Options Symbol
        :returns: Last day of trading date.
        """
        ...


class CMEStrikePriceScalingFactors(System.Object):
    """Provides a means to get the scaling factor for CME's quotes API"""

    @staticmethod
    def GetScaleFactor(underlyingFuture: typing.Union[QuantConnect.Symbol, str]) -> float:
        """
        Gets the option chain strike price scaling factor for the quote response from CME
        
        :param underlyingFuture: Underlying future Symbol to normalize
        :returns: Scaling factor for the strike price.
        """
        ...


