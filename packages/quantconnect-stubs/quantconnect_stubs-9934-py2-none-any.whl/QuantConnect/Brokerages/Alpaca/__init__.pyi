import QuantConnect
import QuantConnect.Brokerages
import QuantConnect.Brokerages.Alpaca
import QuantConnect.Data
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Securities
import System.Collections.Generic


class AlpacaBrokerage(QuantConnect.Brokerages.Brokerage):
    """Alpaca Brokerage utility methods"""

    @property
    def IsConnected(self) -> bool:
        ...

    @property
    def AccountBaseCurrency(self) -> str:
        """Returns the brokerage account's base currency"""
        ...

    @AccountBaseCurrency.setter
    def AccountBaseCurrency(self, value: str):
        """Returns the brokerage account's base currency"""
        ...

    def GetRates(self, instrument: str) -> QuantConnect.Data.Market.Tick:
        """
        Retrieves the current quotes for an instrument
        
        :param instrument: the instrument to check
        :returns: Returns a Tick object with the current bid/ask prices for the instrument.
        """
        ...

    def __init__(self, orderProvider: QuantConnect.Securities.IOrderProvider, securityProvider: QuantConnect.Securities.ISecurityProvider, accountKeyId: str, secretKey: str, tradingMode: str) -> None:
        """
        Initializes a new instance of the AlpacaBrokerage class.
        
        :param orderProvider: The order provider.
        :param securityProvider: The holdings provider.
        :param accountKeyId: The Alpaca api key id
        :param secretKey: The api secret key
        :param tradingMode: The Alpaca trading mode. paper/live
        """
        ...

    def Connect(self) -> None:
        """Connects the client to the broker's remote servers"""
        ...

    def Disconnect(self) -> None:
        """Disconnects the client from the broker's remote servers"""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """
        Gets the current cash balance for each currency held in the brokerage account
        
        :returns: The current cash balance for each currency available for trading.
        """
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """
        Gets all holdings for the account
        
        :returns: The current holdings from the account.
        """
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """
        Gets all open orders on the account.
        NOTE: The order objects returned do not have QC order IDs.
        
        :returns: The open orders returned from Alpaca.
        """
        ...

    def PlaceOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Places a new order and assigns a new broker ID to the order
        
        :param order: The order to be placed
        :returns: True if the request for a new order has been placed, false otherwise.
        """
        ...

    def UpdateOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Updates the order with the same id
        
        :param order: The new order information
        :returns: True if the request was made for the order to be updated, false otherwise.
        """
        ...

    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Cancels the order with the specified ID
        
        :param order: The order to cancel
        :returns: True if the request was made for the order to be canceled, false otherwise.
        """
        ...

    def GetHistory(self, request: QuantConnect.Data.HistoryRequest) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Gets the history for the requested security
        
        :param request: The historical data request
        :returns: An enumerable of bars covering the span specified in the request.
        """
        ...


class AlpacaBrokerageFactory(QuantConnect.Brokerages.BrokerageFactory):
    """Provides an implementations of IBrokerageFactory that produces a AlpacaBrokerage"""

    @property
    def BrokerageData(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Gets the brokerage data required to run the brokerage from configuration/disk"""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the AlpacaBrokerageFactory class."""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def GetBrokerageModel(self, orderProvider: QuantConnect.Securities.IOrderProvider) -> QuantConnect.Brokerages.IBrokerageModel:
        """
        Gets a new instance of the AlpacaBrokerageModel
        
        :param orderProvider: The order provider
        """
        ...

    def CreateBrokerage(self, job: QuantConnect.Packets.LiveNodePacket, algorithm: QuantConnect.Interfaces.IAlgorithm) -> QuantConnect.Interfaces.IBrokerage:
        """
        Creates a new IBrokerage instance
        
        :param job: The job packet to create the brokerage for
        :param algorithm: The algorithm instance
        :returns: A new brokerage instance.
        """
        ...


