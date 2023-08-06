import abc
import datetime
import typing

import QuantConnect.Brokerages.Alpaca.Markets
import System
import System.Collections.Generic
import System.Threading
import System.Threading.Tasks

IWatchList = typing.Any
QuantConnect_Brokerages_Alpaca_Markets_AggregationPeriod = typing.Any
QuantConnect_Brokerages_Alpaca_Markets_HistoryPeriod = typing.Any

QuantConnect_Brokerages_Alpaca_Markets_IDayHistoricalItems_TItem = typing.TypeVar("QuantConnect_Brokerages_Alpaca_Markets_IDayHistoricalItems_TItem")
QuantConnect_Brokerages_Alpaca_Markets_IHistoricalItems_TItem = typing.TypeVar("QuantConnect_Brokerages_Alpaca_Markets_IHistoricalItems_TItem")
QuantConnect_Brokerages_Alpaca_Markets_IQuoteBase_TExchange = typing.TypeVar("QuantConnect_Brokerages_Alpaca_Markets_IQuoteBase_TExchange")
QuantConnect_Brokerages_Alpaca_Markets_IAggHistoricalItems_TItem = typing.TypeVar("QuantConnect_Brokerages_Alpaca_Markets_IAggHistoricalItems_TItem")


class ThrottleParameters(System.Object):
    """Helper class for storing parameters required for initializing rate throttler in RestClient class."""

    @property
    def Occurrences(self) -> int:
        """Gets or sets number of occurrences per unit time."""
        ...

    @Occurrences.setter
    def Occurrences(self, value: int):
        """Gets or sets number of occurrences per unit time."""
        ...

    @property
    def TimeUnit(self) -> datetime.timedelta:
        """Gets or sets throttling time interval."""
        ...

    @TimeUnit.setter
    def TimeUnit(self, value: datetime.timedelta):
        """Gets or sets throttling time interval."""
        ...

    @property
    def MaxRetryAttempts(self) -> int:
        """Gets or sets maximal number of retry attempts for single request."""
        ...

    @MaxRetryAttempts.setter
    def MaxRetryAttempts(self, value: int):
        """Gets or sets maximal number of retry attempts for single request."""
        ...

    @property
    def RetryHttpStatuses(self) -> System.Collections.Generic.IEnumerable[int]:
        """Gets or sets list of Http status codes which when received should initiate a retry of the affected request"""
        ...

    @RetryHttpStatuses.setter
    def RetryHttpStatuses(self, value: System.Collections.Generic.IEnumerable[int]):
        """Gets or sets list of Http status codes which when received should initiate a retry of the affected request"""
        ...

    Default: QuantConnect.Brokerages.Alpaca.Markets.ThrottleParameters
    """Gets throttle parameters initialized with default values or from configuration file."""

    def __init__(self, occurrences: typing.Optional[int] = None, timeUnit: typing.Optional[datetime.timedelta] = None, maxRetryAttempts: typing.Optional[int] = None, retryHttpStatuses: System.Collections.Generic.IEnumerable[int] = None) -> None:
        """Creates new instance of ThrottleParameters object."""
        ...


class IAccountConfiguration(metaclass=abc.ABCMeta):
    """Encapsulates account configuration settings from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def DayTradeMarginCallProtection(self) -> int:
        """
        Gets or sets day trade margin call protection mode for account.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.DayTradeMarginCallProtection enum.
        """
        ...

    @DayTradeMarginCallProtection.setter
    @abc.abstractmethod
    def DayTradeMarginCallProtection(self, value: int):
        """
        Gets or sets day trade margin call protection mode for account.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.DayTradeMarginCallProtection enum.
        """
        ...

    @property
    @abc.abstractmethod
    def TradeConfirmEmail(self) -> int:
        """
        Gets or sets notification level for order fill emails.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.TradeConfirmEmail enum.
        """
        ...

    @TradeConfirmEmail.setter
    @abc.abstractmethod
    def TradeConfirmEmail(self, value: int):
        """
        Gets or sets notification level for order fill emails.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.TradeConfirmEmail enum.
        """
        ...

    @property
    @abc.abstractmethod
    def IsSuspendTrade(self) -> bool:
        """Gets or sets control flag for blocking new orders placement."""
        ...

    @IsSuspendTrade.setter
    @abc.abstractmethod
    def IsSuspendTrade(self, value: bool):
        """Gets or sets control flag for blocking new orders placement."""
        ...

    @property
    @abc.abstractmethod
    def IsNoShorting(self) -> bool:
        """Gets or sets control flag for enabling long-only account mode."""
        ...

    @IsNoShorting.setter
    @abc.abstractmethod
    def IsNoShorting(self, value: bool):
        """Gets or sets control flag for enabling long-only account mode."""
        ...


class AccountActivityType(System.Enum):
    """Types of account activities"""

    Fill = 0
    """Order fills (both partial and full fills)"""

    Transaction = 1
    """Cash transactions (both CSD and CSR)"""

    Miscellaneous = 2
    """Miscellaneous or rarely used activity types (All types except those in TRANS, DIV, or FILL)"""

    ACATCash = 3
    """ACATS IN/OUT (Cash)"""

    ACATSecurities = 4
    """ACATS IN/OUT (Securities)"""

    CashDisbursement = 5
    """Cash disbursement(+)"""

    CashReceipt = 6
    """Cash receipt(-)"""

    Dividend = 7
    """Dividends"""

    DividendCapitalGainsLongTerm = 8
    """Dividend (capital gains long term)"""

    DividendCapitalGainsShortTerm = 9
    """Dividend (capital gain short term)"""

    DividendFee = 10
    """Dividend fee"""

    DividendForeignTaxWithheld = 11
    """Dividend adjusted (Foreign Tax Withheld)"""

    DividendNRAWithheld = 12
    """Dividend adjusted (NRA Withheld)"""

    DividendReturnOfCapital = 13
    """Dividend return of capital"""

    DividendTefraWithheld = 14
    """Dividend adjusted (Tefra Withheld)"""

    DividendTaxExempt = 15
    """Dividend (tax exempt)"""

    Interest = 16
    """Interest (credit/margin)"""

    InterestNRAWithheld = 17
    """Interest adjusted (NRA Withheld)"""

    InterestTefraWithheld = 18
    """Interest adjusted (Tefra Withheld)"""

    JournalEntry = 19
    """Journal entry"""

    JournalEntryCash = 20
    """Journal entry (cash)"""

    JournalEntryStock = 21
    """Journal entry (stock)"""

    MergerAcquisition = 22
    """Merger/Acquisition"""

    NameChange = 23
    """Name change"""

    PassThruCharge = 24
    """Pass Thru Charge"""

    PassThruRebate = 25
    """Pass Thru Rebate"""

    Reorg = 26
    """Reorganization"""

    SymbolChange = 27
    """Symbol change"""

    StockSpinoff = 28
    """Stock spinoff"""

    StockSplit = 29
    """Stock split"""


class SortDirection(System.Enum):
    """Supported sort directions in Alpaca REST API."""

    Descending = 0
    """Descending sort order"""

    Ascending = 1
    """Ascending sort order"""


class RequestValidationException(System.Exception):
    """Represents exception information for request input data validation errors."""

    @property
    def PropertyName(self) -> str:
        ...

    @typing.overload
    def __init__(self) -> None:
        """Creates new instance of RequestValidationException class."""
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        """
        Creates new instance of RequestValidationException class with specified error message.
        
        :param message: The message that describes the error.
        """
        ...

    @typing.overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        """
        Creates new instance of RequestValidationException class with
        specified error message and reference to the inner exception that is the cause of this exception.
        
        :param message: The message that describes the error.
        :param inner: The  exception that is the cause of this exception.
        """
        ...

    @typing.overload
    def __init__(self, message: str, propertyName: str) -> None:
        """
        Creates new instance of RequestValidationException class with specified error message.
        
        :param message: The message that describes the error.
        :param propertyName: The invalid property name.
        """
        ...


class AccountActivitiesRequest(System.Object, QuantConnect.Brokerages.Alpaca.Markets.Validation.IRequest):
    """Encapsulates request parameters for AlpacaTradingClient.ListAccountActivitiesAsync(AccountActivitiesRequest,System.Threading.CancellationToken) call."""

    @property
    def ActivityTypes(self) -> System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.AccountActivityType]:
        """Gets the activity types you want to view entries for. Empty list means 'all activity types'."""
        ...

    @property
    def Date(self) -> typing.Optional[datetime.datetime]:
        """Gets the date for which you want to see activities."""
        ...

    @Date.setter
    def Date(self, value: typing.Optional[datetime.datetime]):
        """Gets the date for which you want to see activities."""
        ...

    @property
    def Until(self) -> typing.Optional[datetime.datetime]:
        """Gets the upper date limit for requesting only activities submitted before this date."""
        ...

    @Until.setter
    def Until(self, value: typing.Optional[datetime.datetime]):
        """Gets the upper date limit for requesting only activities submitted before this date."""
        ...

    @property
    def After(self) -> typing.Optional[datetime.datetime]:
        """Gets the lover date limit for requesting only activities submitted after this date."""
        ...

    @After.setter
    def After(self, value: typing.Optional[datetime.datetime]):
        """Gets the lover date limit for requesting only activities submitted after this date."""
        ...

    @property
    def Direction(self) -> typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.SortDirection]:
        """Gets or sets the sorting direction for results."""
        ...

    @Direction.setter
    def Direction(self, value: typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.SortDirection]):
        """Gets or sets the sorting direction for results."""
        ...

    @property
    def PageSize(self) -> typing.Optional[int]:
        """Gets or sets the maximum number of entries to return in the response."""
        ...

    @PageSize.setter
    def PageSize(self, value: typing.Optional[int]):
        """Gets or sets the maximum number of entries to return in the response."""
        ...

    @property
    def PageToken(self) -> str:
        """Gets or sets the ID of the end of your current page of results."""
        ...

    @PageToken.setter
    def PageToken(self, value: str):
        """Gets or sets the ID of the end of your current page of results."""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Creates new instance of AccountActivitiesRequest object for all activity types."""
        ...

    @typing.overload
    def __init__(self, activityType: QuantConnect.Brokerages.Alpaca.Markets.AccountActivityType) -> None:
        """
        Creates new instance of AccountActivitiesRequest object for a single activity types.
        
        :param activityType: The activity type you want to view entries for.
        """
        ...

    @typing.overload
    def __init__(self, activityTypes: System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Alpaca.Markets.AccountActivityType]) -> None:
        """
        Creates new instance of BarSetRequest object for several activity types.
        
        :param activityTypes: The list of activity types you want to view entries for.
        """
        ...

    def SetSingleDate(self, date: datetime.datetime) -> QuantConnect.Brokerages.Alpaca.Markets.AccountActivitiesRequest:
        """"""
        ...

    def SetInclusiveTimeInterval(self, dateFrom: typing.Optional[datetime.datetime], dateInto: typing.Optional[datetime.datetime]) -> QuantConnect.Brokerages.Alpaca.Markets.AccountActivitiesRequest:
        """"""
        ...

    def GetExceptions(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Alpaca.Markets.RequestValidationException]:
        ...


class TimeFrame(System.Enum):
    """Supported bar duration for Alpaca REST API."""

    Minute = 0
    """One minute bars."""

    FiveMinutes = 1
    """Five minutes bars."""

    FifteenMinutes = 2
    """Fifteen minutes bars."""

    Day = 3
    """Daily bars."""


class HistoryPeriodUnit(System.Enum):
    """Period units for portfolio history in the Alpaca REST API."""

    Day = 0
    """Day"""

    Week = 1
    """Month"""

    Month = 2
    """Month"""

    Year = 3
    """3 month"""


class HistoryPeriod(System.IEquatable[QuantConnect_Brokerages_Alpaca_Markets_HistoryPeriod]):
    """Encapsulates account history period request duration - value and unit pair."""

    @property
    def Unit(self) -> int:
        """
        Gets specified duration units.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.HistoryPeriodUnit enum.
        """
        ...

    @property
    def Value(self) -> int:
        """Gets specified duration value."""
        ...

    def __init__(self, value: int, unit: QuantConnect.Brokerages.Alpaca.Markets.HistoryPeriodUnit) -> None:
        """
        Creates new instance of HistoryPeriod object.
        
        :param value: Duration value in units.
        :param unit: Duration units (days, weeks, etc.)
        """
        ...

    @typing.overload
    def Equals(self, other: QuantConnect.Brokerages.Alpaca.Markets.HistoryPeriod) -> bool:
        ...

    def ToString(self) -> str:
        ...

    @typing.overload
    def Equals(self, other: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class PortfolioHistoryRequest(System.Object, QuantConnect.Brokerages.Alpaca.Markets.Validation.IRequest):
    """Encapsulates request parameters for AlpacaTradingClient.GetPortfolioHistoryAsync(PortfolioHistoryRequest,System.Threading.CancellationToken) call."""

    @property
    def StartDate(self) -> typing.Optional[datetime.datetime]:
        """Gets or sets start date for desired history."""
        ...

    @StartDate.setter
    def StartDate(self, value: typing.Optional[datetime.datetime]):
        """Gets or sets start date for desired history."""
        ...

    @property
    def EndDate(self) -> typing.Optional[datetime.datetime]:
        """Gets or sets  the end date for desired history. Default value (if null) is today."""
        ...

    @EndDate.setter
    def EndDate(self, value: typing.Optional[datetime.datetime]):
        """Gets or sets  the end date for desired history. Default value (if null) is today."""
        ...

    @property
    def TimeFrame(self) -> typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.TimeFrame]:
        """
        Gets or sets the time frame value for desired history. Default value (if null) is 1 minute
        for a period shorter than 7 days, 15 minutes for a period less than 30 days, or 1 day for a longer period.
        """
        ...

    @TimeFrame.setter
    def TimeFrame(self, value: typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.TimeFrame]):
        """
        Gets or sets the time frame value for desired history. Default value (if null) is 1 minute
        for a period shorter than 7 days, 15 minutes for a period less than 30 days, or 1 day for a longer period.
        """
        ...

    @property
    def Period(self) -> typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.HistoryPeriod]:
        """Gets or sets period value for desired history. Default value (if null) is 1 month."""
        ...

    @Period.setter
    def Period(self, value: typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.HistoryPeriod]):
        """Gets or sets period value for desired history. Default value (if null) is 1 month."""
        ...

    @property
    def ExtendedHours(self) -> typing.Optional[bool]:
        """
        Gets or sets flags, indicating that include extended hours included in the result.
        This is effective only for time frame less than 1 day.
        """
        ...

    @ExtendedHours.setter
    def ExtendedHours(self, value: typing.Optional[bool]):
        """
        Gets or sets flags, indicating that include extended hours included in the result.
        This is effective only for time frame less than 1 day.
        """
        ...

    def GetExceptions(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Alpaca.Markets.RequestValidationException]:
        ...


class AssetStatus(System.Enum):
    """Single asset status in Alpaca REST API."""

    Active = 0
    """Active asset."""

    Inactive = 1
    """Inactive asset."""

    Delisted = 2
    """Delisted asset."""


class AssetClass(System.Enum):
    """Supported assed classes for Alpaca REST API."""

    UsEquity = 0
    """US equity asset class."""


class AssetsRequest(System.Object, QuantConnect.Brokerages.Alpaca.Markets.Validation.IRequest):
    """Encapsulates request parameters for AlpacaTradingClient.ListAssetsAsync(AssetsRequest,System.Threading.CancellationToken) call."""

    @property
    def AssetStatus(self) -> typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.AssetStatus]:
        """Gets or sets asset status for filtering."""
        ...

    @AssetStatus.setter
    def AssetStatus(self, value: typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.AssetStatus]):
        """Gets or sets asset status for filtering."""
        ...

    @property
    def AssetClass(self) -> typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.AssetClass]:
        """Gets or sets asset class for filtering."""
        ...

    @AssetClass.setter
    def AssetClass(self, value: typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.AssetClass]):
        """Gets or sets asset class for filtering."""
        ...

    def GetExceptions(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Alpaca.Markets.RequestValidationException]:
        ...


class CalendarRequest(System.Object, QuantConnect.Brokerages.Alpaca.Markets.Validation.IRequest):
    """Encapsulates request parameters for AlpacaTradingClient.ListCalendarAsync(CalendarRequest,System.Threading.CancellationToken) call."""

    @property
    def StartDateInclusive(self) -> typing.Optional[datetime.datetime]:
        """Gets start time for filtering (inclusive)."""
        ...

    @StartDateInclusive.setter
    def StartDateInclusive(self, value: typing.Optional[datetime.datetime]):
        """Gets start time for filtering (inclusive)."""
        ...

    @property
    def EndDateInclusive(self) -> typing.Optional[datetime.datetime]:
        """Gets end time for filtering (inclusive)."""
        ...

    @EndDateInclusive.setter
    def EndDateInclusive(self, value: typing.Optional[datetime.datetime]):
        """Gets end time for filtering (inclusive)."""
        ...

    def SetInclusiveTimeInterval(self, start: typing.Optional[datetime.datetime], end: typing.Optional[datetime.datetime]) -> QuantConnect.Brokerages.Alpaca.Markets.CalendarRequest:
        """
        Sets exclusive time interval for request (start/end time included into interval if specified).
        
        :param start: Filtering interval start time.
        :param end: Filtering interval end time.
        :returns: Fluent interface method return same CalendarRequest instance.
        """
        ...

    def GetExceptions(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Alpaca.Markets.RequestValidationException]:
        ...


class ApiVersion(System.Enum):
    """REST API version number."""

    V1 = 1
    """First version number."""

    V2 = 2
    """Second version number."""


class SecurityKey(System.Object, metaclass=abc.ABCMeta):
    """Base class for 'security key' abstraction."""

    @property
    def Value(self) -> str:
        ...

    def __init__(self, value: str) -> None:
        """
        Creates new instance of SecurityKey object.
        
        This method is protected.
        
        :param value: Security key value.
        """
        ...


class AlpacaTradingClientConfiguration(System.Object):
    """Configuration parameters object for AlpacaTradingClient class."""

    DefaultApiVersion: QuantConnect.Brokerages.Alpaca.Markets.ApiVersion = ...

    @property
    def SecurityId(self) -> QuantConnect.Brokerages.Alpaca.Markets.SecurityKey:
        """Security identifier for API authentication."""
        ...

    @SecurityId.setter
    def SecurityId(self, value: QuantConnect.Brokerages.Alpaca.Markets.SecurityKey):
        """Security identifier for API authentication."""
        ...

    @property
    def ApiEndpoint(self) -> System.Uri:
        """Gets or sets Alpaca Trading API base URL."""
        ...

    @ApiEndpoint.setter
    def ApiEndpoint(self, value: System.Uri):
        """Gets or sets Alpaca Trading API base URL."""
        ...

    @property
    def ApiVersion(self) -> int:
        """
        Gets or sets Alpaca Trading API version.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.ApiVersion enum.
        """
        ...

    @ApiVersion.setter
    def ApiVersion(self, value: int):
        """
        Gets or sets Alpaca Trading API version.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.ApiVersion enum.
        """
        ...

    @property
    def ThrottleParameters(self) -> QuantConnect.Brokerages.Alpaca.Markets.ThrottleParameters:
        """Gets or sets REST API throttling parameters."""
        ...

    @ThrottleParameters.setter
    def ThrottleParameters(self, value: QuantConnect.Brokerages.Alpaca.Markets.ThrottleParameters):
        """Gets or sets REST API throttling parameters."""
        ...

    def __init__(self) -> None:
        """Creates new instance of AlpacaTradingClientConfiguration class."""
        ...


class OrderStatusFilter(System.Enum):
    """Order statuses filter for RestClient.ListOrdersAsync call from Alpaca REST API."""

    Open = 0
    """Returns only open orders."""

    Closed = 1
    """Returns only closed orders."""

    All = 2
    """Returns all orders."""


class ListOrdersRequest(System.Object, QuantConnect.Brokerages.Alpaca.Markets.Validation.IRequest):
    """Encapsulates request parameters for AlpacaTradingClient.ListOrdersAsync(ListOrdersRequest,System.Threading.CancellationToken) call."""

    @property
    def OrderStatusFilter(self) -> typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.OrderStatusFilter]:
        """Gets or sets order status for filtering."""
        ...

    @OrderStatusFilter.setter
    def OrderStatusFilter(self, value: typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.OrderStatusFilter]):
        """Gets or sets order status for filtering."""
        ...

    @property
    def OrderListSorting(self) -> typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.SortDirection]:
        """Gets or sets the chronological order of response based on the submission time."""
        ...

    @OrderListSorting.setter
    def OrderListSorting(self, value: typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.SortDirection]):
        """Gets or sets the chronological order of response based on the submission time."""
        ...

    @property
    def UntilDateTimeExclusive(self) -> typing.Optional[datetime.datetime]:
        """Gets upper bound date time for filtering orders until specified timestamp (exclusive)."""
        ...

    @UntilDateTimeExclusive.setter
    def UntilDateTimeExclusive(self, value: typing.Optional[datetime.datetime]):
        """Gets upper bound date time for filtering orders until specified timestamp (exclusive)."""
        ...

    @property
    def AfterDateTimeExclusive(self) -> typing.Optional[datetime.datetime]:
        """Gets lower bound date time for filtering orders until specified timestamp (exclusive)."""
        ...

    @AfterDateTimeExclusive.setter
    def AfterDateTimeExclusive(self, value: typing.Optional[datetime.datetime]):
        """Gets lower bound date time for filtering orders until specified timestamp (exclusive)."""
        ...

    @property
    def LimitOrderNumber(self) -> typing.Optional[int]:
        """Gets or sets maximal number of orders in response."""
        ...

    @LimitOrderNumber.setter
    def LimitOrderNumber(self, value: typing.Optional[int]):
        """Gets or sets maximal number of orders in response."""
        ...

    def SetExclusiveTimeInterval(self, after: typing.Optional[datetime.datetime], until: typing.Optional[datetime.datetime]) -> QuantConnect.Brokerages.Alpaca.Markets.ListOrdersRequest:
        """
        Sets exclusive time interval for request (start/end time not included into interval if specified).
        
        :param after: Filtering interval start time.
        :param until: Filtering interval end time.
        :returns: Fluent interface method return same ListOrdersRequest instance.
        """
        ...

    def GetExceptions(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Alpaca.Markets.RequestValidationException]:
        ...


class OrderSide(System.Enum):
    """Order side in Alpaca REST API."""

    Buy = 0
    """Buy order."""

    Sell = 1
    """Sell order."""


class OrderType(System.Enum):
    """Supported order types in Alpaca REST API."""

    Market = 0
    """Market order (no prices required)."""

    Stop = 1
    """Stop order (stop price required)."""

    Limit = 2
    """Limit order (limit price required)."""

    StopLimit = 3
    """Stop limit order (both stop and limit prices required)."""


class TimeInForce(System.Enum):
    """Supported order durations in Alpaca REST API."""

    Day = 0
    """The order is good for the day, and it will be canceled automatically at the end of market hours."""

    Gtc = 1
    """The order is good until canceled."""

    Opg = 2
    """The order is placed at the time the market opens."""

    Ioc = 3
    """The order is immediately filled or canceled after being placed (may partial fill)."""

    Fok = 4
    """The order is immediately filled or canceled after being placed (may not partial fill)."""


class OrderClass(System.Enum):
    """Order class for advanced orders in the Alpaca REST API."""

    Bracket = 0
    """Bracket order"""

    OneCancelsOther = 1
    """One Cancels Other order"""

    OneTriggersOther = 2
    """One Triggers Other order"""


class NewOrderRequest(System.Object, QuantConnect.Brokerages.Alpaca.Markets.Validation.IRequest):
    """Encapsulates request parameters for AlpacaTradingClient.PostOrderAsync(NewOrderRequest,System.Threading.CancellationToken) call."""

    @property
    def Symbol(self) -> str:
        """Gets the new order asset name."""
        ...

    @property
    def Quantity(self) -> int:
        """Gets the new order quantity."""
        ...

    @property
    def Side(self) -> int:
        """
        Gets the new order side (buy or sell).
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.OrderSide enum.
        """
        ...

    @property
    def Type(self) -> int:
        """
        Gets the new order type.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.OrderType enum.
        """
        ...

    @property
    def Duration(self) -> int:
        """
        Gets the new order duration.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.TimeInForce enum.
        """
        ...

    @property
    def LimitPrice(self) -> typing.Optional[float]:
        """Gets or sets the new order limit price."""
        ...

    @LimitPrice.setter
    def LimitPrice(self, value: typing.Optional[float]):
        """Gets or sets the new order limit price."""
        ...

    @property
    def StopPrice(self) -> typing.Optional[float]:
        """Gets or sets the new order stop price."""
        ...

    @StopPrice.setter
    def StopPrice(self, value: typing.Optional[float]):
        """Gets or sets the new order stop price."""
        ...

    @property
    def ClientOrderId(self) -> str:
        """Gets or sets the client order ID."""
        ...

    @ClientOrderId.setter
    def ClientOrderId(self, value: str):
        """Gets or sets the client order ID."""
        ...

    @property
    def ExtendedHours(self) -> typing.Optional[bool]:
        """Gets or sets flag indicating that order should be allowed to execute during extended hours trading."""
        ...

    @ExtendedHours.setter
    def ExtendedHours(self, value: typing.Optional[bool]):
        """Gets or sets flag indicating that order should be allowed to execute during extended hours trading."""
        ...

    @property
    def OrderClass(self) -> typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.OrderClass]:
        """Gets or sets the order class for advanced order types."""
        ...

    @OrderClass.setter
    def OrderClass(self, value: typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.OrderClass]):
        """Gets or sets the order class for advanced order types."""
        ...

    @property
    def TakeProfitLimitPrice(self) -> typing.Optional[float]:
        """Gets or sets the profit taking limit price for advanced order types."""
        ...

    @TakeProfitLimitPrice.setter
    def TakeProfitLimitPrice(self, value: typing.Optional[float]):
        """Gets or sets the profit taking limit price for advanced order types."""
        ...

    @property
    def StopLossStopPrice(self) -> typing.Optional[float]:
        """Gets or sets the stop loss stop price for advanced order types."""
        ...

    @StopLossStopPrice.setter
    def StopLossStopPrice(self, value: typing.Optional[float]):
        """Gets or sets the stop loss stop price for advanced order types."""
        ...

    @property
    def StopLossLimitPrice(self) -> typing.Optional[float]:
        """Gets or sets the stop loss limit price for advanced order types."""
        ...

    @StopLossLimitPrice.setter
    def StopLossLimitPrice(self, value: typing.Optional[float]):
        """Gets or sets the stop loss limit price for advanced order types."""
        ...

    @property
    def Nested(self) -> typing.Optional[bool]:
        """Gets or sets flag indicated that child orders should be listed as 'legs' of parent orders."""
        ...

    @Nested.setter
    def Nested(self, value: typing.Optional[bool]):
        """Gets or sets flag indicated that child orders should be listed as 'legs' of parent orders."""
        ...

    def __init__(self, symbol: str, quantity: int, side: QuantConnect.Brokerages.Alpaca.Markets.OrderSide, type: QuantConnect.Brokerages.Alpaca.Markets.OrderType, duration: QuantConnect.Brokerages.Alpaca.Markets.TimeInForce) -> None:
        """
        Creates new instance of NewOrderRequest object.
        
        :param symbol: Order asset name.
        :param quantity: Order quantity.
        :param side: Order side (buy or sell).
        :param type: Order type.
        :param duration: Order duration.
        """
        ...

    def GetExceptions(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Alpaca.Markets.RequestValidationException]:
        ...


class ChangeOrderRequest(System.Object, QuantConnect.Brokerages.Alpaca.Markets.Validation.IRequest):
    """Encapsulates request parameters for AlpacaTradingClient.PatchOrderAsync(ChangeOrderRequest,System.Threading.CancellationToken) call."""

    @property
    def OrderId(self) -> System.Guid:
        """Gets server side order identifier."""
        ...

    @property
    def Quantity(self) -> typing.Optional[int]:
        """Gets or sets updated order quantity or null if quantity is not changed."""
        ...

    @Quantity.setter
    def Quantity(self, value: typing.Optional[int]):
        """Gets or sets updated order quantity or null if quantity is not changed."""
        ...

    @property
    def Duration(self) -> typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.TimeInForce]:
        """Gets or sets updated order duration or null if duration is not changed."""
        ...

    @Duration.setter
    def Duration(self, value: typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.TimeInForce]):
        """Gets or sets updated order duration or null if duration is not changed."""
        ...

    @property
    def LimitPrice(self) -> typing.Optional[float]:
        """Gets or sets updated order limit price or null if limit price is not changed."""
        ...

    @LimitPrice.setter
    def LimitPrice(self, value: typing.Optional[float]):
        """Gets or sets updated order limit price or null if limit price is not changed."""
        ...

    @property
    def StopPrice(self) -> typing.Optional[float]:
        """Gets or sets updated order stop price or null if stop price is not changed."""
        ...

    @StopPrice.setter
    def StopPrice(self, value: typing.Optional[float]):
        """Gets or sets updated order stop price or null if stop price is not changed."""
        ...

    @property
    def ClientOrderId(self) -> str:
        """Gets or sets updated client order ID or null if client order ID is not changed."""
        ...

    @ClientOrderId.setter
    def ClientOrderId(self, value: str):
        """Gets or sets updated client order ID or null if client order ID is not changed."""
        ...

    def __init__(self, orderId: System.Guid) -> None:
        """
        Creates new instance of ChangeOrderRequest object.
        
        :param orderId: Server side order identifier.
        """
        ...

    def GetExceptions(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Alpaca.Markets.RequestValidationException]:
        ...


class IAccountBase(metaclass=abc.ABCMeta):
    """Encapsulates basic account information from Alpaca streaming API."""

    @property
    @abc.abstractmethod
    def AccountId(self) -> System.Guid:
        """Gets unique account identifier."""
        ...

    @property
    @abc.abstractmethod
    def Status(self) -> int:
        """
        Gets updated account status.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.AccountStatus enum.
        """
        ...

    @property
    @abc.abstractmethod
    def Currency(self) -> str:
        """Gets main account currency."""
        ...

    @property
    @abc.abstractmethod
    def TradableCash(self) -> float:
        """Gets amount of money available for trading."""
        ...

    @property
    @abc.abstractmethod
    def WithdrawableCash(self) -> float:
        """Gets amount of money available for withdraw."""
        ...

    @property
    @abc.abstractmethod
    def CreatedAt(self) -> datetime.datetime:
        """Gets timestamp of account creation event."""
        ...


class IAccount(QuantConnect.Brokerages.Alpaca.Markets.IAccountBase, metaclass=abc.ABCMeta):
    """Encapsulates full account information from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def AccountNumber(self) -> str:
        """Gets account number (string identifier)."""
        ...

    @property
    @abc.abstractmethod
    def IsDayPatternTrader(self) -> bool:
        """Gets returns true if account is linked to day pattern trader."""
        ...

    @property
    @abc.abstractmethod
    def IsTradingBlocked(self) -> bool:
        """Gets returns true if account trading functions are blocked."""
        ...

    @property
    @abc.abstractmethod
    def IsTransfersBlocked(self) -> bool:
        """Gets returns true if account transfer functions are blocked."""
        ...

    @property
    @abc.abstractmethod
    def TradeSuspendedByUser(self) -> bool:
        """User setting. If true, the account is not allowed to place orders."""
        ...

    @property
    @abc.abstractmethod
    def ShortingEnabled(self) -> bool:
        """Flag to denote whether or not the account is permitted to short."""
        ...

    @property
    @abc.abstractmethod
    def Multiplier(self) -> int:
        """Buying power multiplier that represents account margin classification."""
        ...

    @property
    @abc.abstractmethod
    def BuyingPower(self) -> float:
        """Current available buying power."""
        ...

    @property
    @abc.abstractmethod
    def DayTradingBuyingPower(self) -> float:
        """Your buying power for day trades (continuously updated value)."""
        ...

    @property
    @abc.abstractmethod
    def RegulationBuyingPower(self) -> float:
        """Your buying power under Regulation T (your excess equity - equity minus margin value - times your margin multiplier)."""
        ...

    @property
    @abc.abstractmethod
    def LongMarketValue(self) -> float:
        """Real-time MtM value of all long positions held in the account."""
        ...

    @property
    @abc.abstractmethod
    def ShortMarketValue(self) -> float:
        """Real-time MtM value of all short positions held in the account."""
        ...

    @property
    @abc.abstractmethod
    def Equity(self) -> float:
        """Cash + LongMarketValue + ShortMarketValue."""
        ...

    @property
    @abc.abstractmethod
    def LastEquity(self) -> float:
        """Equity as of previous trading day at 16:00:00 ET."""
        ...

    @property
    @abc.abstractmethod
    def InitialMargin(self) -> float:
        """Reg T initial margin requirement (continuously updated value)."""
        ...

    @property
    @abc.abstractmethod
    def MaintenanceMargin(self) -> float:
        """Maintenance margin requirement (continuously updated value)."""
        ...

    @property
    @abc.abstractmethod
    def LastMaintenanceMargin(self) -> float:
        """Your maintenance margin requirement on the previous trading day"""
        ...

    @property
    @abc.abstractmethod
    def DayTradeCount(self) -> int:
        """the current number of day trades that have been made in the last 5 trading days (inclusive of today)."""
        ...

    @property
    @abc.abstractmethod
    def Sma(self) -> float:
        """value of special memorandum account."""
        ...

    @property
    @abc.abstractmethod
    def IsAccountBlocked(self) -> bool:
        """Gets returns true if account is completely blocked."""
        ...


class IPortfolioHistoryItem(metaclass=abc.ABCMeta):
    """Encapsulates portfolio history information item from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def Equity(self) -> typing.Optional[float]:
        """Gets historical equity value."""
        ...

    @property
    @abc.abstractmethod
    def ProfitLoss(self) -> typing.Optional[float]:
        """Gets historical profit/loss value."""
        ...

    @property
    @abc.abstractmethod
    def ProfitLossPercentage(self) -> typing.Optional[float]:
        """Gets historical profit/loss value as percentages."""
        ...

    @property
    @abc.abstractmethod
    def Timestamp(self) -> datetime.datetime:
        """Gets historical timestamp value."""
        ...


class IPortfolioHistory(metaclass=abc.ABCMeta):
    """Encapsulates portfolio history information from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def Items(self) -> System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.IPortfolioHistoryItem]:
        """Gets historical information items list with timestamps."""
        ...

    @property
    @abc.abstractmethod
    def TimeFrame(self) -> int:
        """
        Gets time frame value for this historical view.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.TimeFrame enum.
        """
        ...

    @property
    @abc.abstractmethod
    def BaseValue(self) -> float:
        """Gets base value for this historical view."""
        ...


class IAsset(metaclass=abc.ABCMeta):
    """Encapsulates asset information from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def AssetId(self) -> System.Guid:
        """Gets unique asset identifier."""
        ...

    @property
    @abc.abstractmethod
    def Class(self) -> int:
        """
        Gets asset class.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.AssetClass enum.
        """
        ...

    @property
    @abc.abstractmethod
    def Exchange(self) -> int:
        """
        Gets asset source exchange.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.Exchange enum.
        """
        ...

    @property
    @abc.abstractmethod
    def Symbol(self) -> str:
        """Gest asset name."""
        ...

    @property
    @abc.abstractmethod
    def Status(self) -> int:
        """
        Get asset status in API.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.AssetStatus enum.
        """
        ...

    @property
    @abc.abstractmethod
    def IsTradable(self) -> bool:
        """Returns true if asset is tradable."""
        ...

    @property
    @abc.abstractmethod
    def Marginable(self) -> bool:
        """Asset is marginable or not"""
        ...

    @property
    @abc.abstractmethod
    def Shortable(self) -> bool:
        """Asset is shortable or not"""
        ...

    @property
    @abc.abstractmethod
    def EasyToBorrow(self) -> bool:
        """Asset is easy-to-borrow or not"""
        ...


class IPosition(metaclass=abc.ABCMeta):
    """Encapsulates position information from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def AccountId(self) -> System.Guid:
        """Gets unique account identifier."""
        ...

    @property
    @abc.abstractmethod
    def AssetId(self) -> System.Guid:
        """Gets unique asset identifier."""
        ...

    @property
    @abc.abstractmethod
    def Symbol(self) -> str:
        """Gets asset name."""
        ...

    @property
    @abc.abstractmethod
    def Exchange(self) -> int:
        """
        Gets asset exchange.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.Exchange enum.
        """
        ...

    @property
    @abc.abstractmethod
    def AssetClass(self) -> int:
        """
        Gets asset class.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.AssetClass enum.
        """
        ...

    @property
    @abc.abstractmethod
    def AverageEntryPrice(self) -> float:
        """Gets average entry price for position."""
        ...

    @property
    @abc.abstractmethod
    def Quantity(self) -> int:
        """Get position quantity (size)."""
        ...

    @property
    @abc.abstractmethod
    def Side(self) -> int:
        """
        Get position side (short or long).
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.PositionSide enum.
        """
        ...

    @property
    @abc.abstractmethod
    def MarketValue(self) -> float:
        """Get current position market value."""
        ...

    @property
    @abc.abstractmethod
    def CostBasis(self) -> float:
        """Get postion cost basis."""
        ...

    @property
    @abc.abstractmethod
    def UnrealizedProfitLoss(self) -> float:
        """Get position unrealized profit loss."""
        ...

    @property
    @abc.abstractmethod
    def UnrealizedProfitLossPercent(self) -> float:
        """Get position unrealized profit loss in percent."""
        ...

    @property
    @abc.abstractmethod
    def IntradayUnrealizedProfitLoss(self) -> float:
        """Get position intraday unrealized profit loss."""
        ...

    @property
    @abc.abstractmethod
    def IntradayUnrealizedProfitLossPercent(self) -> float:
        """Get position intraday unrealized profit loss in percent."""
        ...

    @property
    @abc.abstractmethod
    def AssetCurrentPrice(self) -> float:
        """Gets position's asset current price."""
        ...

    @property
    @abc.abstractmethod
    def AssetLastPrice(self) -> float:
        """Gets position's asset last trade price."""
        ...

    @property
    @abc.abstractmethod
    def AssetChangePercent(self) -> float:
        """Gets position's asset price change in percent."""
        ...


class IClock(metaclass=abc.ABCMeta):
    """Encapsulates current trading date information from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def Timestamp(self) -> datetime.datetime:
        """Gets current timestamp (in UTC time zone)."""
        ...

    @property
    @abc.abstractmethod
    def IsOpen(self) -> bool:
        """Returns true if trading day is open now."""
        ...

    @property
    @abc.abstractmethod
    def NextOpen(self) -> datetime.datetime:
        """Gets nearest trading day open time (in UTC time zone)."""
        ...

    @property
    @abc.abstractmethod
    def NextClose(self) -> datetime.datetime:
        """Gets nearest trading day close time (in UTC time zone)."""
        ...


class IOrder(metaclass=abc.ABCMeta):
    """Encapsulates order information from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def OrderId(self) -> System.Guid:
        """Gests unique server-side order identifier."""
        ...

    @property
    @abc.abstractmethod
    def ClientOrderId(self) -> str:
        """Gets client-side order identifier."""
        ...

    @property
    @abc.abstractmethod
    def CreatedAt(self) -> typing.Optional[datetime.datetime]:
        """Gets order creation timestamp."""
        ...

    @property
    @abc.abstractmethod
    def UpdatedAt(self) -> typing.Optional[datetime.datetime]:
        """Gets last order update timestamp."""
        ...

    @property
    @abc.abstractmethod
    def SubmittedAt(self) -> typing.Optional[datetime.datetime]:
        """Gets order submission timestamp."""
        ...

    @property
    @abc.abstractmethod
    def FilledAt(self) -> typing.Optional[datetime.datetime]:
        """Gets order fill timestamp."""
        ...

    @property
    @abc.abstractmethod
    def ExpiredAt(self) -> typing.Optional[datetime.datetime]:
        """Gets order expiration timestamp."""
        ...

    @property
    @abc.abstractmethod
    def CancelledAt(self) -> typing.Optional[datetime.datetime]:
        """Gets order cancellation timestamp."""
        ...

    @property
    @abc.abstractmethod
    def FailedAt(self) -> typing.Optional[datetime.datetime]:
        """Gets order rejection timestamp."""
        ...

    @property
    @abc.abstractmethod
    def AssetId(self) -> System.Guid:
        """Gets unique asset identifier."""
        ...

    @property
    @abc.abstractmethod
    def Symbol(self) -> str:
        """Gets asset name."""
        ...

    @property
    @abc.abstractmethod
    def AssetClass(self) -> int:
        """
        Gets asset class.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.AssetClass enum.
        """
        ...

    @property
    @abc.abstractmethod
    def Quantity(self) -> int:
        """Gets original order quantity."""
        ...

    @property
    @abc.abstractmethod
    def FilledQuantity(self) -> int:
        """Gets filled order quantity."""
        ...

    @property
    @abc.abstractmethod
    def OrderType(self) -> int:
        """
        Gets order type.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.OrderType enum.
        """
        ...

    @property
    @abc.abstractmethod
    def OrderSide(self) -> int:
        """
        Gets order side (buy or sell).
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.OrderSide enum.
        """
        ...

    @property
    @abc.abstractmethod
    def TimeInForce(self) -> int:
        """
        Gets order duration.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.TimeInForce enum.
        """
        ...

    @property
    @abc.abstractmethod
    def LimitPrice(self) -> typing.Optional[float]:
        """Gets order limit price for limit and stop-limit orders."""
        ...

    @property
    @abc.abstractmethod
    def StopPrice(self) -> typing.Optional[float]:
        """Gets order stop price for stop and stop-limit orders."""
        ...

    @property
    @abc.abstractmethod
    def AverageFillPrice(self) -> typing.Optional[float]:
        """Gets order average fill price."""
        ...

    @property
    @abc.abstractmethod
    def OrderStatus(self) -> int:
        """
        Gets current order status.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.OrderStatus enum.
        """
        ...

    @property
    @abc.abstractmethod
    def Legs(self) -> System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.IOrder]:
        """Gets legs for this order."""
        ...


class TradeEvent(System.Enum):
    """Trade event in Alpaca trade update stream"""

    New = 0
    """New working order."""

    PartialFill = 1
    """Order partially filled."""

    Fill = 2
    """Order completely filled."""

    DoneForDay = 3
    """Order processing done."""

    Canceled = 4
    """Order cancelled."""

    PendingCancel = 5
    """Order cancellation request pending."""

    Stopped = 6
    """Order processing stopped by server."""

    Rejected = 7
    """Order rejected by server side."""

    Suspended = 8
    """Order processing suspended by server."""

    PendingNew = 9
    """Initial new order request pending."""

    Calculated = 10
    """Order information calculated by server."""

    Expired = 11
    """Order expired."""

    OrderCancelRejected = 12
    """Order cancellation was rejected."""

    Replaced = 13
    """Requested replacement of an order was processed."""

    PendingReplace = 14
    """The order is awaiting replacement."""

    ReplaceRejected = 15
    """The order replace has been rejected."""


class IAccountActivity(metaclass=abc.ABCMeta):
    """Encapsulates account activity information from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def ActivityType(self) -> int:
        """
        Activity type.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.AccountActivityType enum.
        """
        ...

    @property
    @abc.abstractmethod
    def ActivityId(self) -> str:
        """An ID for the activity, always in "{date}::{uuid}" format. Can be sent as page_token in requests to facilitate the paging of results."""
        ...

    @property
    @abc.abstractmethod
    def ActivityDateTime(self) -> datetime.datetime:
        """An activity timestamp (date and time) from ActivityId."""
        ...

    @property
    @abc.abstractmethod
    def ActivityGuid(self) -> System.Guid:
        """An activity unique identifier from ActivityId."""
        ...

    @property
    @abc.abstractmethod
    def Symbol(self) -> str:
        """The symbol of the security involved with the activity. Not present for all activity types."""
        ...

    @property
    @abc.abstractmethod
    def ActivityDate(self) -> typing.Optional[datetime.datetime]:
        """The date on which the activity occurred or on which the transaction associated with the activity settled."""
        ...

    @property
    @abc.abstractmethod
    def NetAmount(self) -> typing.Optional[float]:
        """The net amount of money (positive or negative) associated with the activity."""
        ...

    @property
    @abc.abstractmethod
    def Quantity(self) -> typing.Optional[int]:
        """The number of shares that contributed to the transaction. Not present for all activity types."""
        ...

    @property
    @abc.abstractmethod
    def PerShareAmount(self) -> typing.Optional[float]:
        """For dividend activities, the average amount paid per share. Not present for other activity types."""
        ...

    @property
    @abc.abstractmethod
    def CumulativeQuantity(self) -> typing.Optional[int]:
        """The cumulative quantity of shares involved in the execution."""
        ...

    @property
    @abc.abstractmethod
    def LeavesQuantity(self) -> typing.Optional[int]:
        """For partially_filled orders, the quantity of shares that are left to be filled."""
        ...

    @property
    @abc.abstractmethod
    def Price(self) -> typing.Optional[float]:
        """The per-share price that a trade was executed at."""
        ...

    @property
    @abc.abstractmethod
    def Side(self) -> typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.OrderSide]:
        """The order side of a trade execution."""
        ...

    @property
    @abc.abstractmethod
    def TransactionTime(self) -> typing.Optional[datetime.datetime]:
        """The time at which an execution occurred."""
        ...

    @property
    @abc.abstractmethod
    def Type(self) -> typing.Optional[QuantConnect.Brokerages.Alpaca.Markets.TradeEvent]:
        """The type of trade event associated with an execution."""
        ...


class IPositionActionStatus(metaclass=abc.ABCMeta):
    """Encapsulates position action status information from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def Symbol(self) -> str:
        """Gets processed position asset name."""
        ...

    @property
    @abc.abstractmethod
    def IsSuccess(self) -> bool:
        """Returns true if requested action completed successfully."""
        ...


class ICalendar(metaclass=abc.ABCMeta):
    """Encapsulates single trading day information from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def TradingDate(self) -> datetime.datetime:
        """Gets trading date (in UTC time zone)."""
        ...

    @property
    @abc.abstractmethod
    def TradingOpenTime(self) -> datetime.datetime:
        """Gets trading date open time (in UTC time zone)."""
        ...

    @property
    @abc.abstractmethod
    def TradingCloseTime(self) -> datetime.datetime:
        """Gets trading date close time (in UTC time zone)."""
        ...


class IOrderActionStatus(metaclass=abc.ABCMeta):
    """Encapsulates order action status information from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def OrderId(self) -> System.Guid:
        """Gets unique server-side order identifier."""
        ...

    @property
    @abc.abstractmethod
    def IsSuccess(self) -> bool:
        """Returns true if requested action completed successfully."""
        ...


class AlpacaTradingClient(System.Object, System.IDisposable):
    """Provides unified type-safe access for Alpaca Trading API via HTTP/REST."""

    def GetAccountAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IAccount]:
        """
        Gets account information from Alpaca REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only account information.
        """
        ...

    def GetAccountConfigurationAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IAccountConfiguration]:
        """
        Gets account configuration settings from Alpaca REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Mutable version of account configuration object.
        """
        ...

    def PatchAccountConfigurationAsync(self, accountConfiguration: QuantConnect.Brokerages.Alpaca.Markets.IAccountConfiguration, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IAccountConfiguration]:
        """
        Updates account configuration settings using Alpaca REST API endpoint.
        
        :param accountConfiguration: New account configuration object for updating.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Mutable version of updated account configuration object.
        """
        ...

    def ListAccountActivitiesAsync(self, request: QuantConnect.Brokerages.Alpaca.Markets.AccountActivitiesRequest, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.IAccountActivity]]:
        """
        Gets list of account activities from Alpaca REST API endpoint by specific activity.
        
        :param request: Account activities request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of account activity record objects.
        """
        ...

    def GetPortfolioHistoryAsync(self, request: QuantConnect.Brokerages.Alpaca.Markets.PortfolioHistoryRequest, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IPortfolioHistory]:
        """
        Gets portfolio equity history from Alpaca REST API endpoint.
        
        :param request: Portfolio history request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only portfolio history information object.
        """
        ...

    def ListAllAssetsAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.IAsset]]:
        """
        Gets list of all available assets from Alpaca REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of asset information objects.
        """
        ...

    def ListAssetsAsync(self, request: QuantConnect.Brokerages.Alpaca.Markets.AssetsRequest, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.IAsset]]:
        """
        Gets list of available assets from Alpaca REST API endpoint.
        
        :param request: Asset list request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of asset information objects.
        """
        ...

    def GetAssetAsync(self, symbol: str, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IAsset]:
        """
        Get single asset information by asset name from Alpaca REST API endpoint.
        
        :param symbol: Asset name for searching.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only asset information.
        """
        ...

    def ListPositionsAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.IPosition]]:
        """
        Gets list of available positions from Alpaca REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of position information objects.
        """
        ...

    def GetPositionAsync(self, symbol: str, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IPosition]:
        """
        Gets position information by asset name from Alpaca REST API endpoint.
        
        :param symbol: Position asset name.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only position information object.
        """
        ...

    def DeleteAllPositionsAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.IPositionActionStatus]]:
        """
        Liquidates all open positions at market price using Alpaca REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: List of position cancellation status objects.
        """
        ...

    def DeletePositionAsync(self, symbol: str, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[bool]:
        """
        Liquidate an open position at market price using Alpaca REST API endpoint.
        
        :param symbol: Symbol for liquidation.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: True if position liquidation was accepted.
        """
        ...

    def GetClockAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IClock]:
        """
        Get current time information from Alpaca REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only clock information object.
        """
        ...

    def ListAllCalendarAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.ICalendar]]:
        """
        Gets list of all trading days from Alpaca REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of trading date information object.
        """
        ...

    def ListCalendarAsync(self, request: QuantConnect.Brokerages.Alpaca.Markets.CalendarRequest, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.ICalendar]]:
        """
        Gets list of trading days from Alpaca REST API endpoint.
        
        :param request: Calendar items request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of trading date information object.
        """
        ...

    def __init__(self, configuration: QuantConnect.Brokerages.Alpaca.Markets.AlpacaTradingClientConfiguration) -> None:
        """
        Creates new instance of AlpacaTradingClient object.
        
        :param configuration: Configuration parameters object.
        """
        ...

    def Dispose(self) -> None:
        ...

    def ListAllOrdersAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.IOrder]]:
        """
        Gets list of available orders from Alpaca REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of order information objects.
        """
        ...

    def ListOrdersAsync(self, request: QuantConnect.Brokerages.Alpaca.Markets.ListOrdersRequest, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.IOrder]]:
        """
        Gets list of available orders from Alpaca REST API endpoint.
        
        :param request: List orders request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of order information objects.
        """
        ...

    def PostOrderAsync(self, request: QuantConnect.Brokerages.Alpaca.Markets.NewOrderRequest, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IOrder]:
        """
        Creates new order for execution using Alpaca REST API endpoint.
        
        :param request: New order placement request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only order information object for newly created order.
        """
        ...

    def PatchOrderAsync(self, request: QuantConnect.Brokerages.Alpaca.Markets.ChangeOrderRequest, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IOrder]:
        """
        Updates existing order using Alpaca REST API endpoint.
        
        :param request: Patch order request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only order information object for updated order.
        """
        ...

    @typing.overload
    def GetOrderAsync(self, clientOrderId: str, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IOrder]:
        """
        Get single order information by client order ID from Alpaca REST API endpoint.
        
        :param clientOrderId: Client order ID for searching.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only order information object.
        """
        ...

    @typing.overload
    def GetOrderAsync(self, orderId: System.Guid, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IOrder]:
        """
        Get single order information by server order ID from Alpaca REST API endpoint.
        
        :param orderId: Server order ID for searching.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only order information object.
        """
        ...

    def DeleteOrderAsync(self, orderId: System.Guid, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[bool]:
        """
        Deletes/cancel order on server by server order ID using Alpaca REST API endpoint.
        
        :param orderId: Server order ID for cancelling.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: True if order cancellation was accepted.
        """
        ...

    def DeleteAllOrdersAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.IOrderActionStatus]]:
        """
        Deletes/cancel all open orders using Alpaca REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: List of order cancellation status objects.
        """
        ...

    def ListWatchListsAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[IWatchList]]:
        """
        Gets list of watch list objects from Alpaca REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of watch list objects.
        """
        ...

    def CreateWatchListAsync(self, request: typing.Any, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[IWatchList]:
        """
        Add new watch list object into Alpaca REST API endpoint.
        
        :param request: New watch list request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Newly created watch list object.
        """
        ...

    def GetWatchListByIdAsync(self, watchListId: System.Guid, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[IWatchList]:
        """
        Get watch list object from Alpaca REST API endpoint by watch list identifier.
        
        :param watchListId: Unique watch list identifier.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Watch list object with proper  value.
        """
        ...

    def GetWatchListByNameAsync(self, name: str, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[IWatchList]:
        """
        Get watch list object from Alpaca REST API endpoint by watch list user-defined name.
        
        :param name: User defined watch list name.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Watch list object with proper  value.
        """
        ...

    def UpdateWatchListByIdAsync(self, request: typing.Any, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[IWatchList]:
        """
        Updates watch list object from Alpaca REST API endpoint by watch list identifier.
        
        :param request: Update watch list request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Updated watch list object with proper  value.
        """
        ...

    def AddAssetIntoWatchListByIdAsync(self, request: typing.Any, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[IWatchList]:
        """
        Adds asset into watch list using Alpaca REST API endpoint by watch list identifier.
        
        :param request: Asset adding request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Updated watch list object with proper  value.
        """
        ...

    def AddAssetIntoWatchListByNameAsync(self, request: typing.Any, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[IWatchList]:
        """
        Adds asset into watch list using Alpaca REST API endpoint by watch list name.
        
        :param request: Asset adding request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Updated watch list object with proper  value.
        """
        ...

    def DeleteAssetFromWatchListByIdAsync(self, request: typing.Any, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[IWatchList]:
        """
        Deletes asset from watch list using Alpaca REST API endpoint by watch list identifier.
        
        :param request: Asset deleting request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Updated watch list object with proper  value.
        """
        ...

    def DeleteAssetFromWatchListByNameAsync(self, request: typing.Any, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[IWatchList]:
        """
        Deletes asset from watch list using Alpaca REST API endpoint by watch list name.
        
        :param request: Asset deleting request parameters.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Updated watch list object with proper  value.
        """
        ...

    def DeleteWatchListByIdAsync(self, watchListId: System.Guid, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[bool]:
        """
        Deletes watch list from Alpaca REST API endpoint by watch list identifier.
        
        :param watchListId: Unique watch list identifier.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Returns true if operation completed successfully.
        """
        ...

    def DeleteWatchListByNameAsync(self, name: str, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[bool]:
        """
        Deletes watch list from Alpaca REST API endpoint by watch list name.
        
        :param name: User defined watch list name.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Returns true if operation completed successfully.
        """
        ...


class PolygonDataClientConfiguration(System.Object):
    """Configuration parameters object for PolygonDataClient class."""

    @property
    def KeyId(self) -> str:
        """Gets or sets Alpaca application key identifier."""
        ...

    @KeyId.setter
    def KeyId(self, value: str):
        """Gets or sets Alpaca application key identifier."""
        ...

    @property
    def ApiEndpoint(self) -> System.Uri:
        """Gets or sets Polygon Data API base URL."""
        ...

    @ApiEndpoint.setter
    def ApiEndpoint(self, value: System.Uri):
        """Gets or sets Polygon Data API base URL."""
        ...

    def __init__(self) -> None:
        """Creates new instance of PolygonDataClientConfiguration class."""
        ...


class HistoricalRequest(System.Object, QuantConnect.Brokerages.Alpaca.Markets.Validation.IRequest):
    """
    Encapsulates request parameters for PolygonDataClient.ListHistoricalTradesAsync(HistoricalRequest,System.Threading.CancellationToken)
    and PolygonDataClient.ListHistoricalQuotesAsync(HistoricalRequest,System.Threading.CancellationToken) method calls.
    """

    @property
    def Symbol(self) -> str:
        """Gets asset name for data retrieval."""
        ...

    @property
    def Date(self) -> datetime.datetime:
        """Gets single date for data retrieval."""
        ...

    @property
    def Timestamp(self) -> typing.Optional[int]:
        """Gets or sets initial timestamp for request. Using the timestamp of the last result will give you the next page of results."""
        ...

    @Timestamp.setter
    def Timestamp(self, value: typing.Optional[int]):
        """Gets or sets initial timestamp for request. Using the timestamp of the last result will give you the next page of results."""
        ...

    @property
    def TimestampLimit(self) -> typing.Optional[int]:
        """Gets or sets maximum timestamp allowed in the results."""
        ...

    @TimestampLimit.setter
    def TimestampLimit(self, value: typing.Optional[int]):
        """Gets or sets maximum timestamp allowed in the results."""
        ...

    @property
    def Limit(self) -> typing.Optional[int]:
        """Gets or sets size (number of items) limits fore the response."""
        ...

    @Limit.setter
    def Limit(self, value: typing.Optional[int]):
        """Gets or sets size (number of items) limits fore the response."""
        ...

    @property
    def Reverse(self) -> typing.Optional[bool]:
        """Gets or sets flag that indicates reversed order of the results."""
        ...

    @Reverse.setter
    def Reverse(self, value: typing.Optional[bool]):
        """Gets or sets flag that indicates reversed order of the results."""
        ...

    def __init__(self, symbol: str, date: datetime.datetime) -> None:
        """
        Creates new instance of HistoricalRequest object.
        
        :param symbol: Asset name for data retrieval.
        :param date: Single date for data retrieval.
        """
        ...

    def GetExceptions(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Alpaca.Markets.RequestValidationException]:
        ...


class AggregationPeriodUnit(System.Enum):
    """Supported aggregation time windows for Alpaca REST API."""

    Minute = 0
    """One minute window"""

    Hour = 1
    """One hour window"""

    Day = 2
    """One day window"""

    Week = 3
    """One week window"""

    Month = 4
    """One month window"""

    Quarter = 5
    """One quarter window"""

    Year = 6
    """One year window"""


class AggregationPeriod(System.IEquatable[QuantConnect_Brokerages_Alpaca_Markets_AggregationPeriod]):
    """Encapsulates account history period request duration - value and unit pair."""

    @property
    def Unit(self) -> int:
        """
        Gets specified duration units.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.AggregationPeriodUnit enum.
        """
        ...

    @property
    def Value(self) -> int:
        """Gets specified duration value."""
        ...

    def __init__(self, value: int, unit: QuantConnect.Brokerages.Alpaca.Markets.AggregationPeriodUnit) -> None:
        """
        Creates new instance of AggregationPeriod object.
        
        :param value: Duration value in units.
        :param unit: Duration units (days, weeks, etc.)
        """
        ...

    @typing.overload
    def Equals(self, other: QuantConnect.Brokerages.Alpaca.Markets.AggregationPeriod) -> bool:
        ...

    def ToString(self) -> str:
        ...

    @typing.overload
    def Equals(self, other: typing.Any) -> bool:
        ...

    def GetHashCode(self) -> int:
        ...


class AggregatesRequest(System.Object, QuantConnect.Brokerages.Alpaca.Markets.Validation.IRequest):
    """Encapsulates request parameters for PolygonDataClient.ListAggregatesAsync(AggregatesRequest,System.Threading.CancellationToken) call."""

    @property
    def Symbol(self) -> str:
        """Gets asset name for data retrieval."""
        ...

    @property
    def Period(self) -> QuantConnect.Brokerages.Alpaca.Markets.AggregationPeriod:
        """Gets aggregation time span (number or bars and base bar size)."""
        ...

    @property
    def DateFrom(self) -> datetime.datetime:
        """Gets start time for filtering (inclusive)."""
        ...

    @DateFrom.setter
    def DateFrom(self, value: datetime.datetime):
        """Gets start time for filtering (inclusive)."""
        ...

    @property
    def DateInto(self) -> datetime.datetime:
        """Gets end time for filtering (inclusive)."""
        ...

    @DateInto.setter
    def DateInto(self, value: datetime.datetime):
        """Gets end time for filtering (inclusive)."""
        ...

    @property
    def Unadjusted(self) -> bool:
        """Gets or sets flag indicated that the results should not be adjusted for splits."""
        ...

    @Unadjusted.setter
    def Unadjusted(self, value: bool):
        """Gets or sets flag indicated that the results should not be adjusted for splits."""
        ...

    def __init__(self, symbol: str, period: QuantConnect.Brokerages.Alpaca.Markets.AggregationPeriod) -> None:
        """
        Creates new instance of AggregatesRequest object.
        
        :param symbol: Asset name for data retrieval.
        :param period: Aggregation time span (number or bars and base bar size).
        """
        ...

    def SetInclusiveTimeInterval(self, dateFrom: datetime.datetime, dateInto: datetime.datetime) -> QuantConnect.Brokerages.Alpaca.Markets.AggregatesRequest:
        """
        Sets inclusive time interval for request.
        
        :param dateFrom: Filtering interval start time.
        :param dateInto: Filtering interval end time.
        :returns: Fluent interface method return same AggregatesRequest instance.
        """
        ...

    def GetExceptions(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Brokerages.Alpaca.Markets.RequestValidationException]:
        ...


class TickType(System.Enum):
    """Conditions map type for RestClient.GetConditionMapAsync call form Polygon REST API."""

    Trades = 0
    """Method RestClient.GetConditionMapAsync returns trades conditions."""

    Quotes = 1
    """Method RestClient.GetConditionMapAsync returns quotes conditions."""


class IHistoricalItems(typing.Generic[QuantConnect_Brokerages_Alpaca_Markets_IHistoricalItems_TItem], metaclass=abc.ABCMeta):
    """Encapsulates read-only access for historical items in Polygon REST API."""

    @property
    @abc.abstractmethod
    def Status(self) -> str:
        """Gets resulting status of historical data request."""
        ...

    @property
    @abc.abstractmethod
    def Symbol(self) -> str:
        """Gets asset name for all historical items in container."""
        ...

    @property
    @abc.abstractmethod
    def Items(self) -> System.Collections.Generic.IReadOnlyList[QuantConnect_Brokerages_Alpaca_Markets_IHistoricalItems_TItem]:
        """Gets read-only collection of historical items."""
        ...

    @property
    @abc.abstractmethod
    def Adjusted(self) -> bool:
        """
        Indicates if this response was adjusted for splits.
        Polygon v2 API only.
        """
        ...

    @property
    @abc.abstractmethod
    def QueryCount(self) -> int:
        """
        Number of aggregates (minutes or days) used to generate the response.
        Polygon v2 API only.
        """
        ...

    @property
    @abc.abstractmethod
    def ResultsCount(self) -> int:
        """
        Total number of results generated.
        Polygon v2 API only.
        """
        ...

    @property
    @abc.abstractmethod
    def DatabaseLatency(self) -> datetime.timedelta:
        """Query execution database latency reported by Polygon."""
        ...


class ILastTrade(metaclass=abc.ABCMeta):
    """Encapsulates last trade information from Polygon REST API."""

    @property
    @abc.abstractmethod
    def Status(self) -> str:
        """Gets request status."""
        ...

    @property
    @abc.abstractmethod
    def Symbol(self) -> str:
        """Gets asset name."""
        ...

    @property
    @abc.abstractmethod
    def Exchange(self) -> int:
        """Gets asset's exchange identifier."""
        ...

    @property
    @abc.abstractmethod
    def Price(self) -> float:
        """Gets trade price level."""
        ...

    @property
    @abc.abstractmethod
    def Size(self) -> int:
        """Gets trade quantity."""
        ...

    @property
    @abc.abstractmethod
    def Time(self) -> datetime.datetime:
        """Gets trade timestamp."""
        ...


class IQuoteBase(typing.Generic[QuantConnect_Brokerages_Alpaca_Markets_IQuoteBase_TExchange], metaclass=abc.ABCMeta):
    """Encapsulates basic quote information any REST API."""

    @property
    @abc.abstractmethod
    def BidExchange(self) -> QuantConnect_Brokerages_Alpaca_Markets_IQuoteBase_TExchange:
        """Gets identifier of bid source exchange."""
        ...

    @property
    @abc.abstractmethod
    def AskExchange(self) -> QuantConnect_Brokerages_Alpaca_Markets_IQuoteBase_TExchange:
        """Gets identifier of ask source exchange."""
        ...

    @property
    @abc.abstractmethod
    def BidPrice(self) -> float:
        """Gets bid price level."""
        ...

    @property
    @abc.abstractmethod
    def AskPrice(self) -> float:
        """Gets ask price level."""
        ...

    @property
    @abc.abstractmethod
    def BidSize(self) -> int:
        """Gets bid quantity."""
        ...

    @property
    @abc.abstractmethod
    def AskSize(self) -> int:
        """Gets ask quantity."""
        ...


class IStreamQuote(QuantConnect.Brokerages.Alpaca.Markets.IQuoteBase[int], metaclass=abc.ABCMeta):
    """Encapsulates quote information from Polygon streaming API."""

    @property
    @abc.abstractmethod
    def Symbol(self) -> str:
        """Gets asset name."""
        ...

    @property
    @abc.abstractmethod
    def Time(self) -> datetime.datetime:
        """Gets quote timestamp."""
        ...


class ILastQuote(QuantConnect.Brokerages.Alpaca.Markets.IStreamQuote, metaclass=abc.ABCMeta):
    """Encapsulates last quote information from Alpaca REST API."""

    @property
    @abc.abstractmethod
    def Status(self) -> str:
        """Gets quote response status."""
        ...


class IExchange(metaclass=abc.ABCMeta):
    """Encapsulates exchange information from Ploygon REST API."""

    @property
    @abc.abstractmethod
    def ExchangeId(self) -> int:
        """Gets exchange unique identifier."""
        ...

    @property
    @abc.abstractmethod
    def ExchangeType(self) -> int:
        """
        Gets exchange type.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.ExchangeType enum.
        """
        ...

    @property
    @abc.abstractmethod
    def MarketDataType(self) -> int:
        """
        Gets market data type.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.MarketDataType enum.
        """
        ...

    @property
    @abc.abstractmethod
    def MarketIdentificationCode(self) -> str:
        """Gets exchange market identification code."""
        ...

    @property
    @abc.abstractmethod
    def Name(self) -> str:
        """Gets exchange name."""
        ...

    @property
    @abc.abstractmethod
    def TapeId(self) -> str:
        """Gets exchange tape ID."""
        ...


class ITimestamps(metaclass=abc.ABCMeta):
    """Encapsulates timestamps information from Polygon REST API."""

    @property
    @abc.abstractmethod
    def Timestamp(self) -> datetime.datetime:
        """Gets SIP timestamp."""
        ...

    @property
    @abc.abstractmethod
    def ParticipantTimestamp(self) -> datetime.datetime:
        """Gets participant/exchange timestamp."""
        ...

    @property
    @abc.abstractmethod
    def TradeReportingFacilityTimestamp(self) -> datetime.datetime:
        """Gets trade reporting facility timestamp."""
        ...


class IHistoricalBase(metaclass=abc.ABCMeta):
    """Encapsulates base historical information from Polygon REST API."""

    @property
    @abc.abstractmethod
    def Tape(self) -> int:
        """Gets tape where trade occured."""
        ...

    @property
    @abc.abstractmethod
    def SequenceNumber(self) -> int:
        """Gets sequence number of trade."""
        ...

    @property
    @abc.abstractmethod
    def Conditions(self) -> System.Collections.Generic.IReadOnlyList[int]:
        """Gets quote conditions."""
        ...


class IHistoricalTrade(QuantConnect.Brokerages.Alpaca.Markets.ITimestamps, QuantConnect.Brokerages.Alpaca.Markets.IHistoricalBase, metaclass=abc.ABCMeta):
    """Encapsulates historical trade information from Polygon REST API."""

    @property
    @abc.abstractmethod
    def Exchange(self) -> str:
        """Gets trade source exchange."""
        ...

    @property
    @abc.abstractmethod
    def ExchangeId(self) -> int:
        """Gets trade source exchange identifier."""
        ...

    @property
    @abc.abstractmethod
    def TimeOffset(self) -> int:
        """Gets trade timestamp."""
        ...

    @property
    @abc.abstractmethod
    def Price(self) -> float:
        """Gets trade price."""
        ...

    @property
    @abc.abstractmethod
    def Size(self) -> int:
        """Gets trade quantity."""
        ...

    @property
    @abc.abstractmethod
    def TradeReportingFacilityId(self) -> int:
        """Gets trade reporting facility ID."""
        ...

    @property
    @abc.abstractmethod
    def TradeId(self) -> str:
        """Gets trade ID."""
        ...

    @property
    @abc.abstractmethod
    def OriginalTradeId(self) -> str:
        """Gets original trade ID."""
        ...


class IHistoricalQuote(QuantConnect.Brokerages.Alpaca.Markets.IQuoteBase[str], QuantConnect.Brokerages.Alpaca.Markets.ITimestamps, QuantConnect.Brokerages.Alpaca.Markets.IHistoricalBase, metaclass=abc.ABCMeta):
    """Encapsulates historical quote information from Polygon REST API."""

    @property
    @abc.abstractmethod
    def TimeOffset(self) -> int:
        """Gets time offset of quote."""
        ...

    @property
    @abc.abstractmethod
    def Indicators(self) -> System.Collections.Generic.IReadOnlyList[int]:
        """Gets indicators."""
        ...


class IAggBase(metaclass=abc.ABCMeta):
    """Encapsulates basic bar information for Polygon APIs."""

    @property
    @abc.abstractmethod
    def Open(self) -> float:
        """Gets bar open price."""
        ...

    @property
    @abc.abstractmethod
    def High(self) -> float:
        """Gets bar high price."""
        ...

    @property
    @abc.abstractmethod
    def Low(self) -> float:
        """Gets bar low price."""
        ...

    @property
    @abc.abstractmethod
    def Close(self) -> float:
        """Gets bar close price."""
        ...

    @property
    @abc.abstractmethod
    def Volume(self) -> int:
        """Gets bar trading volume."""
        ...

    @property
    @abc.abstractmethod
    def ItemsInWindow(self) -> int:
        """
        Number of items in aggregate window.
        Polygon v2 API only.
        """
        ...


class IAgg(QuantConnect.Brokerages.Alpaca.Markets.IAggBase, metaclass=abc.ABCMeta):
    """Encapsulates bar information from Polygon REST API."""

    @property
    @abc.abstractmethod
    def Time(self) -> datetime.datetime:
        """Gets bar timestamp."""
        ...


class PolygonDataClient(System.Object, System.IDisposable):
    """Provides unified type-safe access for Polygon Data API via HTTP/REST."""

    def __init__(self, configuration: QuantConnect.Brokerages.Alpaca.Markets.PolygonDataClientConfiguration) -> None:
        """
        Creates new instance of PolygonDataClient object.
        
        :param configuration: Configuration parameters object.
        """
        ...

    def Dispose(self) -> None:
        ...

    def ListExchangesAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyList[QuantConnect.Brokerages.Alpaca.Markets.IExchange]]:
        """
        Gets list of available exchanges from Polygon REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of exchange information objects.
        """
        ...

    def GetSymbolTypeMapAsync(self, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyDictionary[str, str]]:
        """
        Gets mapping dictionary for symbol types from Polygon REST API endpoint.
        
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only dictionary with keys equal to symbol type abbreviation and values equal to full symbol type names descriptions for each supported symbol type.
        """
        ...

    def ListHistoricalTradesAsync(self, request: QuantConnect.Brokerages.Alpaca.Markets.HistoricalRequest, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IHistoricalItems[QuantConnect.Brokerages.Alpaca.Markets.IHistoricalTrade]]:
        """
        Gets list of historical trades for a single asset from Polygon's REST API endpoint.
        
        :param request: Historical trades request parameter.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of historical trade information.
        """
        ...

    def ListHistoricalQuotesAsync(self, request: QuantConnect.Brokerages.Alpaca.Markets.HistoricalRequest, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IHistoricalItems[QuantConnect.Brokerages.Alpaca.Markets.IHistoricalQuote]]:
        """
        Gets list of historical trades for a single asset from Polygon's REST API endpoint.
        
        :param request: Historical quotes request parameter.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of historical trade information.
        """
        ...

    def ListAggregatesAsync(self, request: QuantConnect.Brokerages.Alpaca.Markets.AggregatesRequest, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.IHistoricalItems[QuantConnect.Brokerages.Alpaca.Markets.IAgg]]:
        """
        Gets list of historical minute bars for single asset from Polygon's v2 REST API endpoint.
        
        :param request: Day aggregates request parameter.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only list of day bars for specified asset.
        """
        ...

    def GetLastTradeAsync(self, symbol: str, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.ILastTrade]:
        """
        Gets last trade for singe asset from Polygon REST API endpoint.
        
        :param symbol: Asset name for data retrieval.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only last trade information.
        """
        ...

    def GetLastQuoteAsync(self, symbol: str, cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[QuantConnect.Brokerages.Alpaca.Markets.ILastQuote]:
        """
        Gets current quote for singe asset from Polygon REST API endpoint.
        
        :param symbol: Asset name for data retrieval.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only current quote information.
        """
        ...

    def GetConditionMapAsync(self, tickType: QuantConnect.Brokerages.Alpaca.Markets.TickType = ..., cancellationToken: System.Threading.CancellationToken = ...) -> System.Threading.Tasks.Task[System.Collections.Generic.IReadOnlyDictionary[int, str]]:
        """
        Gets mapping dictionary for specific tick type from Polygon REST API endpoint.
        
        :param tickType: Tick type for conditions map.
        :param cancellationToken: A cancellation token that can be used by other objects or threads to receive notice of cancellation.
        :returns: Read-only dictionary with keys equal to condition integer values and values equal to full tick condition descriptions for each supported tick type.
        """
        ...


class SecretKey(QuantConnect.Brokerages.Alpaca.Markets.SecurityKey):
    """Secret API key for Alpaca/Polygon APIs authentication."""

    @property
    def KeyId(self) -> str:
        ...

    def __init__(self, keyId: str, value: str) -> None:
        """
        Creates new instance of SecretKey object.
        
        :param keyId: Secret API key identifier.
        :param value: Secret API key value.
        """
        ...


class IStreamAgg(QuantConnect.Brokerages.Alpaca.Markets.IAggBase, metaclass=abc.ABCMeta):
    """Encapsulates bar information from Polygon streaming API."""

    @property
    @abc.abstractmethod
    def Symbol(self) -> str:
        """Gets asset name."""
        ...

    @property
    @abc.abstractmethod
    def Average(self) -> float:
        """Gets bar average price."""
        ...

    @property
    @abc.abstractmethod
    def StartTime(self) -> datetime.datetime:
        """Gets bar opening timestamp."""
        ...

    @property
    @abc.abstractmethod
    def EndTime(self) -> datetime.datetime:
        """Gets bar closing timestamp."""
        ...


class ITradeUpdate(metaclass=abc.ABCMeta):
    """Encapsulates trade update information from Alpaca streaming API."""

    @property
    @abc.abstractmethod
    def Event(self) -> int:
        """
        Gets trade update reason.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.TradeEvent enum.
        """
        ...

    @property
    @abc.abstractmethod
    def Price(self) -> typing.Optional[float]:
        """Gets updated trade price level."""
        ...

    @property
    @abc.abstractmethod
    def Quantity(self) -> typing.Optional[int]:
        """Gets updated trade quantity."""
        ...

    @property
    @abc.abstractmethod
    def Timestamp(self) -> datetime.datetime:
        """Gets update timestamp."""
        ...

    @property
    @abc.abstractmethod
    def Order(self) -> QuantConnect.Brokerages.Alpaca.Markets.IOrder:
        """Gets related order object."""
        ...


class IStreamTrade(metaclass=abc.ABCMeta):
    """Encapsulates trade information from Polygon streaming API."""

    @property
    @abc.abstractmethod
    def Symbol(self) -> str:
        """Gets asset name."""
        ...

    @property
    @abc.abstractmethod
    def Exchange(self) -> int:
        """Gets asset's exchange identifier."""
        ...

    @property
    @abc.abstractmethod
    def Price(self) -> float:
        """Gets trade price level."""
        ...

    @property
    @abc.abstractmethod
    def Size(self) -> int:
        """Gets trade quantity."""
        ...

    @property
    @abc.abstractmethod
    def Time(self) -> datetime.datetime:
        """Gets trade timestamp."""
        ...


class IDayHistoricalItems(typing.Generic[QuantConnect_Brokerages_Alpaca_Markets_IDayHistoricalItems_TItem], QuantConnect.Brokerages.Alpaca.Markets.IHistoricalItems[QuantConnect_Brokerages_Alpaca_Markets_IDayHistoricalItems_TItem], metaclass=abc.ABCMeta):
    """Encapsulates list of single day historical itmes from Polygon REST API."""

    @property
    @abc.abstractmethod
    def ItemsDay(self) -> datetime.datetime:
        """Gets historical items day."""
        ...

    @property
    @abc.abstractmethod
    def LatencyInMs(self) -> int:
        """Gets data latency in milliseconds."""
        ...


class IAggHistoricalItems(typing.Generic[QuantConnect_Brokerages_Alpaca_Markets_IAggHistoricalItems_TItem], QuantConnect.Brokerages.Alpaca.Markets.IHistoricalItems[QuantConnect_Brokerages_Alpaca_Markets_IAggHistoricalItems_TItem], metaclass=abc.ABCMeta):
    """Encapsulates list of historical aggregates (bars) from Polygon REST API."""

    @property
    @abc.abstractmethod
    def AggregationType(self) -> int:
        """
        Gets type of historical aggregates (bars) in this container.
        
        This property contains the int value of a member of the QuantConnect.Brokerages.Alpaca.Markets.AggregationType enum.
        """
        ...


class IAccountUpdate(QuantConnect.Brokerages.Alpaca.Markets.IAccountBase, metaclass=abc.ABCMeta):
    """Encapsulates account update information from Alpaca streaming API."""

    @property
    @abc.abstractmethod
    def UpdatedAt(self) -> datetime.datetime:
        """Gets timestamp of last account update event."""
        ...

    @property
    @abc.abstractmethod
    def DeletedAt(self) -> typing.Optional[datetime.datetime]:
        """Gets timestamp of account deletion event."""
        ...


class RestClientErrorException(System.Exception):
    """Represents Alpaca/Polygon REST API specific error information."""

    @property
    def ErrorCode(self) -> int:
        """Original error code returned by REST API endpoint."""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Creates new instance of RestClientErrorException class."""
        ...

    @typing.overload
    def __init__(self, message: str) -> None:
        """
        Creates new instance of RestClientErrorException class with specified error message.
        
        :param message: The message that describes the error.
        """
        ...

    @typing.overload
    def __init__(self, message: str, inner: System.Exception) -> None:
        """
        Creates new instance of RestClientErrorException class with
        specified error message and reference to the inner exception that is the cause of this exception.
        
        :param message: The message that describes the error.
        :param inner: The  exception that is the cause of this exception.
        """
        ...


class Exchange(System.Enum):
    """Exchanges supported by Alpaca REST API."""

    Unknown = 0
    """Unknown exchange (not supported by this version of SDK)."""

    NyseMkt = 1
    """NYSE American Stock Exchange."""

    NyseArca = 2
    """NYSE Arca Stock Exchange."""

    Nyse = 3
    """New York Stock Exchange (NYSE)"""

    Nasdaq = 4
    """Nasdaq Stock Market."""

    Bats = 5
    """BATS Global Market."""

    Amex = 6
    """American Stock Exchange (AMEX)"""

    Arca = 7
    """Archipelago Stock Exchange (ARCA)."""

    Iex = 8
    """International Exchange (IEX)."""


class AccountStatus(System.Enum):
    """User account status in Alpaca REST API."""

    Onboarding = 0
    """Account opened but not verified."""

    SubmissionFailed = 1
    """Missed important information."""

    Submitted = 2
    """Additional information added."""

    AccountUpdated = 3
    """Accouunt data updated."""

    ApprovalPending = 4
    """Approval request sent."""

    Active = 5
    """Account approved and working."""

    Rejected = 6
    """Account approval rejected."""


class AuthStatus(System.Enum):
    """Authorization status for Alpaca streaming API."""

    Authorized = 0
    """Client successfully authorized."""

    Unauthorized = 1
    """Client does not authorized."""


class PositionSide(System.Enum):
    """Position side in Alpaca REST API."""

    Long = 0
    """Long position."""

    Short = 1
    """Short position."""


class AggregationType(System.Enum):
    """Historical data aggregation type in Alpaca REST API."""

    Day = 0
    """Aggreagated data for single trading day."""

    Minute = 1
    """Aggregated data for single minute."""


class DayTradeMarginCallProtection(System.Enum):
    """
    Day trade margin call protection mode for account. See more information here:
    https://docs.alpaca.markets/user-protections/#day-trade-margin-call-dtmc-protection-at-alpaca
    """

    Entry = 0
    """Check rules on position entry."""

    Exit = 1
    """Check rules on position exit."""

    Both = 2
    """Check rules on position entry and exit."""


class ExchangeType(System.Enum):
    """Supported exchange types in Polygon REST API."""

    Exchange = 0
    """Ordinal exchange."""

    Banking = 1
    """Banking organization."""

    TradeReportingFacility = 2
    """Trade reporting facility."""


class OrderStatus(System.Enum):
    """Order status in Alpaca REST API."""

    Accepted = 0
    """Order accepted by server."""

    New = 1
    """New working order."""

    PartiallyFilled = 2
    """Order partially filled."""

    Filled = 3
    """Order completely filled."""

    DoneForDay = 4
    """Order processing done."""

    Canceled = 5
    """Order cancelled."""

    Replaced = 6
    """Order replaced (modified)."""

    PendingCancel = 7
    """Order cancellation request pending."""

    Stopped = 8
    """Order processing stopped by server."""

    Rejected = 9
    """Order rejected by server side."""

    Suspended = 10
    """Order processing suspended by server."""

    PendingNew = 11
    """Initial new order request pending."""

    Calculated = 12
    """Order information calculated by server."""

    Expired = 13
    """Order expired."""

    AcceptedForBidding = 14
    """Order accepted for bidding by server."""

    PendingReplace = 15
    """Order replacement request pending."""

    Fill = 16
    """Order completely filled."""


class TradeConfirmEmail(System.Enum):
    """Notification level for order fill emails."""

    # Cannot convert to Python: None = 0
    """Never send email notification for order fills."""

    All = 1
    """Send email notification for all order fills."""


class MarketDataType(System.Enum):
    """Supported asset types in Polygon REST API."""

    Equities = 0
    """Equities."""

    Indexes = 1
    """Indexes."""

    Currencies = 2
    """Currencies."""


class IEnvironment(metaclass=abc.ABCMeta):
    """Provides URLs for different APIs available for this SDK on specific environment."""

    @property
    @abc.abstractmethod
    def AlpacaTradingApi(self) -> System.Uri:
        """Gets Alpaca trading REST API base URL for this environment."""
        ...

    @property
    @abc.abstractmethod
    def AlpacaDataApi(self) -> System.Uri:
        """Gets Alpaca data REST API base URL for this environment."""
        ...

    @property
    @abc.abstractmethod
    def PolygonDataApi(self) -> System.Uri:
        """Gets Polygon.io data REST API base URL for this environment."""
        ...

    @property
    @abc.abstractmethod
    def AlpacaStreamingApi(self) -> System.Uri:
        """Gets Alpaca streaming API base URL for this environment."""
        ...

    @property
    @abc.abstractmethod
    def PolygonStreamingApi(self) -> System.Uri:
        """Gets Polygon.io streaming API base URL for this environment."""
        ...


class Environments(System.Object):
    """Provides single entry point for obtaining information about different environments."""

    Live: QuantConnect.Brokerages.Alpaca.Markets.IEnvironment
    """Gets environment used by all Alpaca users who has fully registered accounts."""

    Paper: QuantConnect.Brokerages.Alpaca.Markets.IEnvironment
    """Gets environment used by all Alpaca users who have no registered accounts."""


