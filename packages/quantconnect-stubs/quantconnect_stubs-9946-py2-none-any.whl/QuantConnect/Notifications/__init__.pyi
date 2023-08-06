import abc
import typing

import QuantConnect.Notifications
import System
import System.Collections.Concurrent
import System.Collections.Generic


class Notification(System.Object, metaclass=abc.ABCMeta):
    """Local/desktop implementation of messaging system for Lean Engine."""

    def Send(self) -> None:
        """Method for sending implementations of notification object types."""
        ...


class NotificationManager(System.Object):
    """Local/desktop implementation of messaging system for Lean Engine."""

    @property
    def Messages(self) -> System.Collections.Concurrent.ConcurrentQueue[QuantConnect.Notifications.Notification]:
        """Public access to the messages"""
        ...

    @Messages.setter
    def Messages(self, value: System.Collections.Concurrent.ConcurrentQueue[QuantConnect.Notifications.Notification]):
        """Public access to the messages"""
        ...

    def __init__(self, liveMode: bool) -> None:
        """Initialize the messaging system"""
        ...

    @typing.overload
    def Email(self, address: str, subject: str, message: str, data: str, headers: typing.Any) -> bool:
        """
        Send an email to the address specified for live trading notifications.
        
        :param address: Email address to send to
        :param subject: Subject of the email
        :param message: Message body, up to 10kb
        :param data: Data attachment (optional)
        :param headers: Optional email headers to use
        """
        ...

    @typing.overload
    def Email(self, address: str, subject: str, message: str, data: str = ..., headers: System.Collections.Generic.Dictionary[str, str] = None) -> bool:
        """
        Send an email to the address specified for live trading notifications.
        
        :param address: Email address to send to
        :param subject: Subject of the email
        :param message: Message body, up to 10kb
        :param data: Data attachment (optional)
        :param headers: Optional email headers to use
        """
        ...

    def Sms(self, phoneNumber: str, message: str) -> bool:
        """
        Send an SMS to the phone number specified
        
        :param phoneNumber: Phone number to send to
        :param message: Message to send
        """
        ...

    def Web(self, address: str, data: typing.Any = None) -> bool:
        """
        Place REST POST call to the specified address with the specified DATA.
        
        :param address: Endpoint address
        :param data: Data to send in body JSON encoded (optional)
        """
        ...


class NotificationWeb(QuantConnect.Notifications.Notification):
    """Web Notification Class"""

    @property
    def Address(self) -> str:
        """Send a notification message to this web address"""
        ...

    @Address.setter
    def Address(self, value: str):
        """Send a notification message to this web address"""
        ...

    @property
    def Data(self) -> System.Object:
        """Object data to send."""
        ...

    @Data.setter
    def Data(self, value: System.Object):
        """Object data to send."""
        ...

    def __init__(self, address: str, data: typing.Any = None) -> None:
        """Constructor for sending a notification SMS to a specified phone number"""
        ...


class NotificationSms(QuantConnect.Notifications.Notification):
    """Sms Notification Class"""

    @property
    def PhoneNumber(self) -> str:
        """Send a notification message to this phone number"""
        ...

    @PhoneNumber.setter
    def PhoneNumber(self, value: str):
        """Send a notification message to this phone number"""
        ...

    @property
    def Message(self) -> str:
        """Message to send. Limited to 160 characters"""
        ...

    @Message.setter
    def Message(self, value: str):
        """Message to send. Limited to 160 characters"""
        ...

    def __init__(self, number: str, message: str) -> None:
        """Constructor for sending a notification SMS to a specified phone number"""
        ...


class NotificationEmail(QuantConnect.Notifications.Notification):
    """Email notification data."""

    @property
    def Headers(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Optional email headers"""
        ...

    @Headers.setter
    def Headers(self, value: System.Collections.Generic.Dictionary[str, str]):
        """Optional email headers"""
        ...

    @property
    def Address(self) -> str:
        """Send to address:"""
        ...

    @Address.setter
    def Address(self, value: str):
        """Send to address:"""
        ...

    @property
    def Subject(self) -> str:
        """Email subject"""
        ...

    @Subject.setter
    def Subject(self, value: str):
        """Email subject"""
        ...

    @property
    def Message(self) -> str:
        """Message to send."""
        ...

    @Message.setter
    def Message(self, value: str):
        """Message to send."""
        ...

    @property
    def Data(self) -> str:
        """Email Data"""
        ...

    @Data.setter
    def Data(self, value: str):
        """Email Data"""
        ...

    def __init__(self, address: str, subject: str = ..., message: str = ..., data: str = ..., headers: System.Collections.Generic.Dictionary[str, str] = None) -> None:
        """
        Default constructor for sending an email notification
        
        :param address: Address to send to. Will throw ArgumentException if invalid Validate.EmailAddress
        :param subject: Subject of the email. Will set to string.Empty if null
        :param message: Message body of the email. Will set to string.Empty if null
        :param data: Data to attach to the email. Will set to string.Empty if null
        :param headers: Optional email headers to use
        """
        ...


