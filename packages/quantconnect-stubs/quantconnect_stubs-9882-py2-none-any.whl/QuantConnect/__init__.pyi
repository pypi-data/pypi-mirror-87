import abc
import datetime
import typing

import QuantConnect
import QuantConnect.Algorithm.Framework.Alphas
import QuantConnect.Algorithm.Framework.Portfolio
import QuantConnect.Data
import QuantConnect.Data.Market
import QuantConnect.Data.UniverseSelection
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Scheduling
import QuantConnect.Securities
import QuantConnect.Util
import System
import System.Collections
import System.Collections.Concurrent
import System.Collections.Generic
import System.Drawing
import System.Globalization
import System.IO
import System.Text
import System.Threading
import System.Threading.Tasks

System_EventHandler = typing.Any
QuantConnect_SecurityIdentifier = typing.Any
QuantConnect_Symbol = typing.Any
JsonConverter = typing.Any
DateTimeZone = typing.Any

QuantConnect_ExtendedDictionary_T = typing.TypeVar('QuantConnect_ExtendedDictionary_T')
QuantConnect_StringExtensions_T = typing.TypeVar('QuantConnect_StringExtensions_T')
QuantConnect_Extensions_T = typing.TypeVar('QuantConnect_Extensions_T')
QuantConnect_Extensions_K = typing.TypeVar('QuantConnect_Extensions_K')
QuantConnect_Extensions_V = typing.TypeVar('QuantConnect_Extensions_V')
QuantConnect_Extensions_TValue = typing.TypeVar('QuantConnect_Extensions_TValue')
QuantConnect_Extensions_TKey = typing.TypeVar('QuantConnect_Extensions_TKey')
QuantConnect_Extensions_TElement = typing.TypeVar('QuantConnect_Extensions_TElement')
QuantConnect_Extensions_TResult = typing.TypeVar('QuantConnect_Extensions_TResult')
QuantConnect_Extensions_TCollection = typing.TypeVar('QuantConnect_Extensions_TCollection')


class ZipStreamWriter(System.IO.TextWriter):
    """Provides an implementation of TextWriter to write to a zip file"""

    @property
    def Encoding(self) -> System.Text.Encoding:
        """When overridden in a derived class, returns the character encoding in which the output is written."""
        ...

    def __init__(self, filename: str, zipEntry: str) -> None:
        """
        Initializes a new instance of the ZipStreamWriter class
        
        :param filename: The output zip file name
        :param zipEntry: The file name in the zip file
        """
        ...

    def Write(self, value: str) -> None:
        """
        Writes a character to the text string or stream.
        
        :param value: The character to write to the text stream.
        """
        ...

    def WriteLine(self, value: str) -> None:
        """
        Writes a string followed by a line terminator to the text string or stream.
        
        :param value: The string to write. If  is null, only the line terminator is written.
        """
        ...

    def Flush(self) -> None:
        """Clears all buffers for the current writer and causes any buffered data to be written to the underlying device."""
        ...

    def Dispose(self, disposing: bool) -> None:
        """
        Releases the unmanaged resources used by the System.IO.TextWriter and optionally releases the managed resources.
        
        This method is protected.
        
        :param disposing: true to release both managed and unmanaged resources; false to release only unmanaged resources.
        """
        ...


class Compression(System.Object):
    """Compression class manages the opening and extraction of compressed files (zip, tar, tar.gz)."""

    @staticmethod
    @typing.overload
    def ZipData(zipPath: str, filenamesAndData: System.Collections.Generic.Dictionary[str, str]) -> bool:
        """
        Create a zip file of the supplied file names and string data source
        
        :param zipPath: Output location to save the file.
        :param filenamesAndData: File names and data in a dictionary format.
        :returns: True on successfully creating the zip file.
        """
        ...

    @staticmethod
    @typing.overload
    def ZipData(zipPath: str, filenamesAndData: System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[str, typing.List[int]]]) -> bool:
        """
        Create a zip file of the supplied file names and data using a byte array
        
        :param zipPath: Output location to save the file.
        :param filenamesAndData: File names and data in a dictionary format.
        :returns: True on successfully saving the file
        """
        ...

    @staticmethod
    @typing.overload
    def ZipData(zipPath: str, zipEntry: str, lines: System.Collections.Generic.IEnumerable[str]) -> bool:
        """
        Zips the specified lines of text into the zipPath
        
        :param zipPath: The destination zip file path
        :param zipEntry: The entry name in the zip
        :param lines: The lines to be written to the zip
        :returns: True if successful, otherwise false
        """
        ...

    @staticmethod
    def ZipCreateAppendData(path: str, entry: str, data: str, overrideEntry: bool = False) -> bool:
        """
        Append the zip data to the file-entry specified.
        
        :param path: The zip file path
        :param entry: The entry name
        :param data: The entry data
        :param overrideEntry: True if should override entry if it already exists
        :returns: True on success
        """
        ...

    @staticmethod
    def UnzipData(zipData: typing.List[int], encoding: System.Text.Encoding = None) -> System.Collections.Generic.Dictionary[str, str]:
        """
        Uncompress zip data byte array into a dictionary string array of filename-contents.
        
        :param zipData: Byte data array of zip compressed information
        :param encoding: Specifies the encoding used to read the bytes. If not specified, defaults to ASCII
        :returns: Uncompressed dictionary string-sting of files in the zip
        """
        ...

    @staticmethod
    def ZipBytes(bytes: typing.List[int], zipEntryName: str) -> typing.List[int]:
        """
        Performs an in memory zip of the specified bytes
        
        :param bytes: The file contents in bytes to be zipped
        :param zipEntryName: The zip entry name
        :returns: The zipped file as a byte array
        """
        ...

    @staticmethod
    def UnGZip(gzipFileName: str, targetDirectory: str) -> str:
        """Extract .gz files to disk"""
        ...

    @staticmethod
    @typing.overload
    def Zip(textPath: str, zipEntryName: str, deleteOriginal: bool = True) -> str:
        """
        Compress a given file and delete the original file. Automatically rename the file to name.zip.
        
        :param textPath: Path of the original file
        :param zipEntryName: The name of the entry inside the zip file
        :param deleteOriginal: Boolean flag to delete the original file after completion
        :returns: String path for the new zip file
        """
        ...

    @staticmethod
    @typing.overload
    def Zip(source: str, destination: str, zipEntryName: str, deleteOriginal: bool) -> None:
        """
        Compresses the specified source file.
        
        :param source: The source file to be compressed
        :param destination: The destination zip file path
        :param zipEntryName: The zip entry name for the file
        :param deleteOriginal: True to delete the source file upon completion
        """
        ...

    @staticmethod
    @typing.overload
    def Zip(textPath: str, deleteOriginal: bool = True) -> str:
        """
        Compress a given file and delete the original file. Automatically rename the file to name.zip.
        
        :param textPath: Path of the original file
        :param deleteOriginal: Boolean flag to delete the original file after completion
        :returns: String path for the new zip file
        """
        ...

    @staticmethod
    @typing.overload
    def Zip(data: str, zipPath: str, zipEntry: str) -> None:
        ...

    @staticmethod
    def ZipDirectory(directory: str, destination: str, includeRootInZip: bool = True) -> bool:
        """
        Zips the specified directory, preserving folder structure
        
        :param directory: The directory to be zipped
        :param destination: The output zip file destination
        :param includeRootInZip: True to include the root 'directory' in the zip, false otherwise
        :returns: True on a successful zip, false otherwise
        """
        ...

    @staticmethod
    @typing.overload
    def Unzip(zip: str, directory: str, overwrite: bool = False) -> bool:
        """
        Unzips the specified zip file to the specified directory
        
        :param zip: The zip to be unzipped
        :param directory: The directory to place the unzipped files
        :param overwrite: Flag specifying whether or not to overwrite existing files
        """
        ...

    @staticmethod
    def ZipFiles(destination: str, files: System.Collections.Generic.IEnumerable[str]) -> None:
        """Zips all files specified to a new zip at the destination path"""
        ...

    @staticmethod
    @typing.overload
    def Unzip(filename: str, zip: typing.Any) -> System.IO.StreamReader:
        """
        Streams a local zip file using a streamreader.
        Important: the caller must call Dispose() on the returned ZipFile instance.
        
        :param filename: Location of the original zip file
        :param zip: The ZipFile instance to be returned to the caller
        :returns: Stream reader of the first file contents in the zip file
        """
        ...

    @staticmethod
    @typing.overload
    def Unzip(filename: str, zipEntryName: str, zip: typing.Any) -> System.IO.StreamReader:
        """
        Streams a local zip file using a streamreader.
        Important: the caller must call Dispose() on the returned ZipFile instance.
        
        :param filename: Location of the original zip file
        :param zipEntryName: The zip entry name to open a reader for. Specify null to access the first entry
        :param zip: The ZipFile instance to be returned to the caller
        :returns: Stream reader of the first file contents in the zip file
        """
        ...

    @staticmethod
    @typing.overload
    def Unzip(filename: str) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[str, System.Collections.Generic.IEnumerable[str]]]:
        """
        Streams the unzipped file as key value pairs of file name to file contents.
        NOTE: When the returned enumerable finishes enumerating, the zip stream will be
        closed rendering all key value pair Value properties unaccessible. Ideally this
        would be enumerated depth first.
        
        :param filename: The zip file to stream
        :returns: The stream zip contents
        """
        ...

    @staticmethod
    @typing.overload
    def Unzip(stream: System.IO.Stream) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[str, System.Collections.Generic.IEnumerable[str]]]:
        """
        Lazily unzips the specified stream
        
        :param stream: The zipped stream to be read
        :returns: An enumerable whose elements are zip entry key value pairs with a key of the zip entry name and the value of the zip entry's file lines
        """
        ...

    @staticmethod
    def ReadLines(filename: str) -> System.Collections.Generic.IEnumerable[str]:
        """
        Streams each line from the first zip entry in the specified zip file
        
        :param filename: The zip file path to stream
        :returns: An enumerable containing each line from the first unzipped entry
        """
        ...

    @staticmethod
    def UnzipStreamToStreamReader(zipstream: System.IO.Stream) -> System.IO.StreamReader:
        """Unzip a local file and return its contents via streamreader:"""
        ...

    @staticmethod
    def UnzipStream(zipstream: System.IO.Stream, zipFile: typing.Any) -> System.IO.Stream:
        """Unzip a stream that represents a zip file and return the first entry as a stream"""
        ...

    @staticmethod
    def UnzipToFolder(zipFile: str) -> System.Collections.Generic.List[str]:
        """
        Unzip a local file and return its contents via streamreader to a local the same location as the ZIP.
        
        :param zipFile: Location of the zip on the HD
        :returns: List of unzipped file names
        """
        ...

    @staticmethod
    def UnTarFiles(source: str, destination: str) -> None:
        """
        Extracts all file from a zip archive and copies them to a destination folder.
        
        :param source: The source zip file.
        :param destination: The destination folder to extract the file to.
        """
        ...

    @staticmethod
    def UnTarGzFiles(source: str, destination: str) -> None:
        """
        Extract tar.gz files to disk
        
        :param source: Tar.gz source file
        :param destination: Location folder to unzip to
        """
        ...

    @staticmethod
    @typing.overload
    def UnTar(stream: System.IO.Stream, isTarGz: bool) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[str, typing.List[int]]]:
        """
        Enumerate through the files of a TAR and get a list of KVP names-byte arrays
        
        :param stream: The input tar stream
        :param isTarGz: True if the input stream is a .tar.gz or .tgz
        :returns: An enumerable containing each tar entry and it's contents
        """
        ...

    @staticmethod
    @typing.overload
    def UnTar(source: str) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.KeyValuePair[str, typing.List[int]]]:
        """Enumerate through the files of a TAR and get a list of KVP names-byte arrays."""
        ...

    @staticmethod
    def ValidateZip(path: str) -> bool:
        """
        Validates whether the zip is corrupted or not
        
        :param path: Path to the zip file
        :returns: true if archive tests ok; false otherwise.
        """
        ...

    @staticmethod
    def GetZipEntryFileNames(zipFileName: str) -> System.Collections.Generic.IEnumerable[str]:
        """
        Returns the entry file names contained in a zip file
        
        :param zipFileName: The zip file name
        :returns: An IEnumerable of entry file names
        """
        ...


class AlphaRuntimeStatistics(System.Object):
    """Contains insight population run time statistics"""

    @property
    def MeanPopulationScore(self) -> QuantConnect.Algorithm.Framework.Alphas.InsightScore:
        """Gets the mean scores for the entire population of insights"""
        ...

    @property
    def RollingAveragedPopulationScore(self) -> QuantConnect.Algorithm.Framework.Alphas.InsightScore:
        """Gets the 100 insight ema of insight scores"""
        ...

    @property
    def LongCount(self) -> int:
        """Gets the total number of insights with an up direction"""
        ...

    @LongCount.setter
    def LongCount(self, value: int):
        """Gets the total number of insights with an up direction"""
        ...

    @property
    def ShortCount(self) -> int:
        """Gets the total number of insights with a down direction"""
        ...

    @ShortCount.setter
    def ShortCount(self, value: int):
        """Gets the total number of insights with a down direction"""
        ...

    @property
    def LongShortRatio(self) -> float:
        """The ratio of InsightDirection.Up over InsightDirection.Down"""
        ...

    @property
    def TotalAccumulatedEstimatedAlphaValue(self) -> float:
        """The total accumulated estimated value of trading all insights"""
        ...

    @TotalAccumulatedEstimatedAlphaValue.setter
    def TotalAccumulatedEstimatedAlphaValue(self, value: float):
        """The total accumulated estimated value of trading all insights"""
        ...

    @property
    def KellyCriterionEstimate(self) -> float:
        """Score of the strategy's insights predictive power"""
        ...

    @KellyCriterionEstimate.setter
    def KellyCriterionEstimate(self, value: float):
        """Score of the strategy's insights predictive power"""
        ...

    @property
    def KellyCriterionProbabilityValue(self) -> float:
        """The p-value or probability value of the KellyCriterionEstimate"""
        ...

    @KellyCriterionProbabilityValue.setter
    def KellyCriterionProbabilityValue(self, value: float):
        """The p-value or probability value of the KellyCriterionEstimate"""
        ...

    @property
    def FitnessScore(self) -> float:
        """Score of the strategy's performance, and suitability for the Alpha Stream Market"""
        ...

    @FitnessScore.setter
    def FitnessScore(self, value: float):
        """Score of the strategy's performance, and suitability for the Alpha Stream Market"""
        ...

    @property
    def PortfolioTurnover(self) -> float:
        """
        Measurement of the strategies trading activity with respect to the portfolio value.
        Calculated as the sales volume with respect to the average total portfolio value.
        """
        ...

    @PortfolioTurnover.setter
    def PortfolioTurnover(self, value: float):
        """
        Measurement of the strategies trading activity with respect to the portfolio value.
        Calculated as the sales volume with respect to the average total portfolio value.
        """
        ...

    @property
    def ReturnOverMaxDrawdown(self) -> float:
        """
        Provides a risk adjusted way to factor in the returns and drawdown of the strategy.
        It is calculated by dividing the Portfolio Annualized Return by the Maximum Drawdown seen during the backtest.
        """
        ...

    @ReturnOverMaxDrawdown.setter
    def ReturnOverMaxDrawdown(self, value: float):
        """
        Provides a risk adjusted way to factor in the returns and drawdown of the strategy.
        It is calculated by dividing the Portfolio Annualized Return by the Maximum Drawdown seen during the backtest.
        """
        ...

    @property
    def SortinoRatio(self) -> float:
        """
        Gives a relative picture of the strategy volatility.
        It is calculated by taking a portfolio's annualized rate of return and subtracting the risk free rate of return.
        """
        ...

    @SortinoRatio.setter
    def SortinoRatio(self, value: float):
        """
        Gives a relative picture of the strategy volatility.
        It is calculated by taking a portfolio's annualized rate of return and subtracting the risk free rate of return.
        """
        ...

    @property
    def EstimatedMonthlyAlphaValue(self) -> float:
        """Suggested Value of the Alpha On A Monthly Basis For Licensing"""
        ...

    @EstimatedMonthlyAlphaValue.setter
    def EstimatedMonthlyAlphaValue(self, value: float):
        """Suggested Value of the Alpha On A Monthly Basis For Licensing"""
        ...

    @property
    def TotalInsightsGenerated(self) -> int:
        """The total number of insight signals generated by the algorithm"""
        ...

    @TotalInsightsGenerated.setter
    def TotalInsightsGenerated(self, value: int):
        """The total number of insight signals generated by the algorithm"""
        ...

    @property
    def TotalInsightsClosed(self) -> int:
        """The total number of insight signals generated by the algorithm"""
        ...

    @TotalInsightsClosed.setter
    def TotalInsightsClosed(self, value: int):
        """The total number of insight signals generated by the algorithm"""
        ...

    @property
    def TotalInsightsAnalysisCompleted(self) -> int:
        """The total number of insight signals generated by the algorithm"""
        ...

    @TotalInsightsAnalysisCompleted.setter
    def TotalInsightsAnalysisCompleted(self, value: int):
        """The total number of insight signals generated by the algorithm"""
        ...

    @property
    def MeanPopulationEstimatedInsightValue(self) -> float:
        """Gets the mean estimated insight value"""
        ...

    @typing.overload
    def __init__(self, accountCurrencyProvider: QuantConnect.Interfaces.IAccountCurrencyProvider) -> None:
        """Creates a new instance"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Default constructor"""
        ...

    def ToDictionary(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Creates a dictionary containing the statistics"""
        ...

    def SetDate(self, now: datetime.datetime) -> None:
        """Set the current date of the backtest"""
        ...

    def SetStartDate(self, algorithmStartDate: datetime.datetime) -> None:
        """Set the date range of the statistics"""
        ...


class ChartType(System.Enum):
    """Type of chart - should we draw the series as overlayed or stacked"""

    Overlay = 0

    Stacked = 1


class SeriesType(System.Enum):
    """Available types of charts"""

    Line = 0

    Scatter = 1

    Candle = 2

    Bar = 3

    Flag = 4

    StackedArea = 5

    Pie = 6

    Treemap = 7


class ScatterMarkerSymbol(System.Enum):
    """Shape or symbol for the marker in a scatter plot"""

    # Cannot convert to Python: None = 0

    Circle = 1

    Square = 2

    Diamond = 3

    Triangle = 4

    TriangleDown = 5


class ChartPoint(System.Object):
    """Single Chart Point Value Type for QCAlgorithm.Plot();"""

    @property
    def x(self) -> int:
        ...

    @x.setter
    def x(self, value: int):
        ...

    @property
    def y(self) -> float:
        ...

    @y.setter
    def y(self, value: float):
        ...

    @typing.overload
    def __init__(self) -> None:
        """Default constructor. Using in SeriesSampler."""
        ...

    @typing.overload
    def __init__(self, xValue: int, yValue: float) -> None:
        """
        Constructor that takes both x, y value paris
        
        :param xValue: X value often representing a time in seconds
        :param yValue: Y value
        """
        ...

    @typing.overload
    def __init__(self, time: datetime.datetime, value: float) -> None:
        ...

    @typing.overload
    def __init__(self, point: QuantConnect.ChartPoint) -> None:
        ...

    def ToString(self) -> str:
        """Provides a readable string representation of this instance."""
        ...


class Series(System.Object):
    """Chart Series Object - Series data and properties for a chart:"""

    @property
    def Name(self) -> str:
        """Name of the Series:"""
        ...

    @Name.setter
    def Name(self, value: str):
        """Name of the Series:"""
        ...

    @property
    def Unit(self) -> str:
        """Axis for the chart series."""
        ...

    @Unit.setter
    def Unit(self, value: str):
        """Axis for the chart series."""
        ...

    @property
    def Index(self) -> int:
        """Index/position of the series on the chart."""
        ...

    @Index.setter
    def Index(self, value: int):
        """Index/position of the series on the chart."""
        ...

    @property
    def Values(self) -> System.Collections.Generic.List[QuantConnect.ChartPoint]:
        """
        Values for the series plot:
        These values are assumed to be in ascending time order (first points earliest, last points latest)
        """
        ...

    @Values.setter
    def Values(self, value: System.Collections.Generic.List[QuantConnect.ChartPoint]):
        """
        Values for the series plot:
        These values are assumed to be in ascending time order (first points earliest, last points latest)
        """
        ...

    @property
    def SeriesType(self) -> QuantConnect.SeriesType:
        """Chart type for the series:"""
        ...

    @SeriesType.setter
    def SeriesType(self, value: QuantConnect.SeriesType):
        """Chart type for the series:"""
        ...

    @property
    def Color(self) -> System.Drawing.Color:
        """Color the series"""
        ...

    @Color.setter
    def Color(self, value: System.Drawing.Color):
        """Color the series"""
        ...

    @property
    def ScatterMarkerSymbol(self) -> QuantConnect.ScatterMarkerSymbol:
        """Shape or symbol for the marker in a scatter plot"""
        ...

    @ScatterMarkerSymbol.setter
    def ScatterMarkerSymbol(self, value: QuantConnect.ScatterMarkerSymbol):
        """Shape or symbol for the marker in a scatter plot"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Default constructor for chart series"""
        ...

    @typing.overload
    def __init__(self, name: str) -> None:
        """
        Constructor method for Chart Series
        
        :param name: Name of the chart series
        """
        ...

    @typing.overload
    def __init__(self, name: str, type: QuantConnect.SeriesType) -> None:
        """
        Foundational constructor on the series class
        
        :param name: Name of the series
        :param type: Type of the series
        """
        ...

    @typing.overload
    def __init__(self, name: str, type: QuantConnect.SeriesType, index: int) -> None:
        """
        Foundational constructor on the series class
        
        :param name: Name of the series
        :param type: Type of the series
        :param index: Index position on the chart of the series
        """
        ...

    @typing.overload
    def __init__(self, name: str, type: QuantConnect.SeriesType, index: int, unit: str) -> None:
        """
        Foundational constructor on the series class
        
        :param name: Name of the series
        :param type: Type of the series
        :param index: Index position on the chart of the series
        :param unit: Unit for the series axis
        """
        ...

    @typing.overload
    def __init__(self, name: str, type: QuantConnect.SeriesType = ..., unit: str = "$") -> None:
        """
        Constructor method for Chart Series
        
        :param name: Name of the chart series
        :param type: Type of the chart series
        :param unit: Unit of the serier
        """
        ...

    @typing.overload
    def __init__(self, name: str, type: QuantConnect.SeriesType, unit: str, color: System.Drawing.Color) -> None:
        """
        Constructor method for Chart Series
        
        :param name: Name of the chart series
        :param type: Type of the chart series
        :param unit: Unit of the serier
        :param color: Color of the series
        """
        ...

    @typing.overload
    def __init__(self, name: str, type: QuantConnect.SeriesType, unit: str, color: System.Drawing.Color, symbol: QuantConnect.ScatterMarkerSymbol = ...) -> None:
        """
        Constructor method for Chart Series
        
        :param name: Name of the chart series
        :param type: Type of the chart series
        :param unit: Unit of the serier
        :param color: Color of the series
        :param symbol: Symbol for the marker in a scatter plot series
        """
        ...

    @typing.overload
    def AddPoint(self, time: datetime.datetime, value: float) -> None:
        """
        Add a new point to this series
        
        :param time: Time of the chart point
        :param value: Value of the chart point
        """
        ...

    @typing.overload
    def AddPoint(self, chartPoint: QuantConnect.ChartPoint) -> None:
        """
        Add a new point to this series
        
        :param chartPoint: The data point to add
        """
        ...

    def GetUpdates(self) -> QuantConnect.Series:
        """
        Get the updates since the last call to this function.
        
        :returns: List of the updates from the series
        """
        ...

    def Purge(self) -> None:
        """Removes the data from this series and resets the update position to 0"""
        ...

    def ConsolidateChartPoints(self) -> QuantConnect.ChartPoint:
        """
        Will sum up all chart points into a new single value, using the time of lastest point
        
        :returns: The new chart point
        """
        ...

    def Clone(self) -> QuantConnect.Series:
        """Return a new instance clone of this object"""
        ...


class Chart(System.Object):
    """Single Parent Chart Object for Custom Charting"""

    @property
    def Name(self) -> str:
        ...

    @Name.setter
    def Name(self, value: str):
        ...

    @property
    def ChartType(self) -> QuantConnect.ChartType:
        ...

    @ChartType.setter
    def ChartType(self, value: QuantConnect.ChartType):
        ...

    @property
    def Series(self) -> System.Collections.Generic.Dictionary[str, QuantConnect.Series]:
        ...

    @Series.setter
    def Series(self, value: System.Collections.Generic.Dictionary[str, QuantConnect.Series]):
        ...

    @typing.overload
    def __init__(self) -> None:
        """Default constructor for chart:"""
        ...

    @typing.overload
    def __init__(self, name: str, type: QuantConnect.ChartType = ...) -> None:
        """
        Chart Constructor:
        
        :param name: Name of the Chart
        :param type: Type of the chart
        """
        ...

    @typing.overload
    def __init__(self, name: str) -> None:
        """
        Constructor for a chart
        
        :param name: String name of the chart
        """
        ...

    def AddSeries(self, series: QuantConnect.Series) -> None:
        """
        Add a reference to this chart series:
        
        :param series: Chart series class object
        """
        ...

    def TryAddAndGetSeries(self, name: str, type: QuantConnect.SeriesType, index: int, unit: str, color: System.Drawing.Color, symbol: QuantConnect.ScatterMarkerSymbol, forceAddNew: bool = False) -> QuantConnect.Series:
        """
        Gets Series if already present in chart, else will add a new series and return it
        
        :param name: Name of the series
        :param type: Type of the series
        :param index: Index position on the chart of the series
        :param unit: Unit for the series axis
        :param color: Color of the series
        :param symbol: Symbol for the marker in a scatter plot series
        :param forceAddNew: True will always add a new Series instance, stepping on existing if any
        """
        ...

    def GetUpdates(self) -> QuantConnect.Chart:
        """Fetch the updates of the chart, and save the index position."""
        ...

    def Clone(self) -> QuantConnect.Chart:
        """Return a new instance clone of this object"""
        ...


class Result(System.Object):
    """
    Base class for backtesting and live results that packages result data.
    LiveResultBacktestResult
    """

    @property
    def AlphaRuntimeStatistics(self) -> QuantConnect.AlphaRuntimeStatistics:
        """Contains population averages scores over the life of the algorithm"""
        ...

    @AlphaRuntimeStatistics.setter
    def AlphaRuntimeStatistics(self, value: QuantConnect.AlphaRuntimeStatistics):
        """Contains population averages scores over the life of the algorithm"""
        ...

    @property
    def Charts(self) -> System.Collections.Generic.IDictionary[str, QuantConnect.Chart]:
        """Charts updates for the live algorithm since the last result packet"""
        ...

    @Charts.setter
    def Charts(self, value: System.Collections.Generic.IDictionary[str, QuantConnect.Chart]):
        """Charts updates for the live algorithm since the last result packet"""
        ...

    @property
    def Orders(self) -> System.Collections.Generic.IDictionary[int, QuantConnect.Orders.Order]:
        """Order updates since the last result packet"""
        ...

    @Orders.setter
    def Orders(self, value: System.Collections.Generic.IDictionary[int, QuantConnect.Orders.Order]):
        """Order updates since the last result packet"""
        ...

    @property
    def OrderEvents(self) -> System.Collections.Generic.List[QuantConnect.Orders.OrderEvent]:
        """OrderEvent updates since the last result packet"""
        ...

    @OrderEvents.setter
    def OrderEvents(self, value: System.Collections.Generic.List[QuantConnect.Orders.OrderEvent]):
        """OrderEvent updates since the last result packet"""
        ...

    @property
    def ProfitLoss(self) -> System.Collections.Generic.IDictionary[datetime.datetime, float]:
        """Trade profit and loss information since the last algorithm result packet"""
        ...

    @ProfitLoss.setter
    def ProfitLoss(self, value: System.Collections.Generic.IDictionary[datetime.datetime, float]):
        """Trade profit and loss information since the last algorithm result packet"""
        ...

    @property
    def Statistics(self) -> System.Collections.Generic.IDictionary[str, str]:
        """Statistics information sent during the algorithm operations."""
        ...

    @Statistics.setter
    def Statistics(self, value: System.Collections.Generic.IDictionary[str, str]):
        """Statistics information sent during the algorithm operations."""
        ...

    @property
    def RuntimeStatistics(self) -> System.Collections.Generic.IDictionary[str, str]:
        """Runtime banner/updating statistics in the title banner of the live algorithm GUI."""
        ...

    @RuntimeStatistics.setter
    def RuntimeStatistics(self, value: System.Collections.Generic.IDictionary[str, str]):
        """Runtime banner/updating statistics in the title banner of the live algorithm GUI."""
        ...

    @property
    def ServerStatistics(self) -> System.Collections.Generic.IDictionary[str, str]:
        """Server status information, including CPU/RAM usage, ect..."""
        ...

    @ServerStatistics.setter
    def ServerStatistics(self, value: System.Collections.Generic.IDictionary[str, str]):
        """Server status information, including CPU/RAM usage, ect..."""
        ...


class LocalTimeKeeper(System.Object):
    """
    Represents the current local time. This object is created via the TimeKeeper to
    manage conversions to local time.
    """

    @property
    def TimeUpdated(self) -> typing.List[System_EventHandler]:
        """Event fired each time UpdateTime is called"""
        ...

    @TimeUpdated.setter
    def TimeUpdated(self, value: typing.List[System_EventHandler]):
        """Event fired each time UpdateTime is called"""
        ...

    @property
    def TimeZone(self) -> typing.Any:
        """Gets the time zone of this LocalTimeKeeper"""
        ...

    @property
    def LocalTime(self) -> datetime.datetime:
        """Gets the current time in terms of the TimeZone"""
        ...

    @LocalTime.setter
    def LocalTime(self, value: datetime.datetime):
        """Gets the current time in terms of the TimeZone"""
        ...


class SecurityType(System.Enum):
    """Type of tradable security / underlying asset"""

    Base = 0
    """Base class for all security types:"""

    Equity = 1
    """US Equity Security"""

    Option = 2
    """Option Security Type"""

    Commodity = 3
    """Commodity Security Type"""

    Forex = 4
    """FOREX Security"""

    Future = 5
    """Future Security Type"""

    Cfd = 6
    """Contract For a Difference Security Type."""

    Crypto = 7
    """Cryptocurrency Security Type."""


class OptionRight(System.Enum):
    """Specifies the different types of options"""

    Call = 0
    """A call option, the right to buy at the strike price"""

    Put = 1
    """A put option, the right to sell at the strike price"""


class OptionStyle(System.Enum):
    """Specifies the style of an option"""

    American = 0
    """American style options are able to be exercised at any time on or before the expiration date"""

    European = 1
    """European style options are able to be exercised on the expiration date only."""


class SecurityIdentifier(System.Object, System.IEquatable[QuantConnect_SecurityIdentifier]):
    """Defines a unique identifier for securities"""

    Empty: QuantConnect.SecurityIdentifier = ...
    """Gets an instance of SecurityIdentifier that is empty, that is, one with no symbol specified"""

    # Cannot convert to Python: None: QuantConnect.SecurityIdentifier = ...
    """Gets an instance of SecurityIdentifier that is explicitly no symbol"""

    DefaultDate: datetime.datetime = ...
    """Gets the date to be used when it does not apply."""

    InvalidSymbolCharacters: System.Collections.Generic.HashSet[str] = ...
    """Gets the set of invalids symbol characters"""

    @property
    def HasUnderlying(self) -> bool:
        ...

    @property
    def Underlying(self) -> QuantConnect.SecurityIdentifier:
        """
        Gets the underlying security identifier for this security identifier. When there is
        no underlying, this property will return a value of Empty.
        """
        ...

    @property
    def Date(self) -> datetime.datetime:
        """
        Gets the date component of this identifier. For equities this
        is the first date the security traded. Technically speaking,
        in LEAN, this is the first date mentioned in the map_files.
        For futures and options this is the expiry date of the contract.
        For other asset classes, this property will throw an
        exception as the field is not specified.
        """
        ...

    @property
    def Symbol(self) -> str:
        """
        Gets the original symbol used to generate this security identifier.
        For equities, by convention this is the first ticker symbol for which
        the security traded
        """
        ...

    @property
    def Market(self) -> str:
        """
        Gets the market component of this security identifier. If located in the
        internal mappings, the full string is returned. If the value is unknown,
        the integer value is returned as a string.
        """
        ...

    @property
    def SecurityType(self) -> QuantConnect.SecurityType:
        """Gets the security type component of this security identifier."""
        ...

    @property
    def StrikePrice(self) -> float:
        """
        Gets the option strike price. This only applies to SecurityType.Option
        and will thrown anexception if accessed otherwse.
        """
        ...

    @property
    def OptionRight(self) -> QuantConnect.OptionRight:
        """
        Gets the option type component of this security identifier. This
        only applies to SecurityType.Open and will throw an exception if
        accessed otherwise.
        """
        ...

    @property
    def OptionStyle(self) -> QuantConnect.OptionStyle:
        """
        Gets the option style component of this security identifier. This
        only applies to SecurityType.Open and will throw an exception if
        accessed otherwise.
        """
        ...

    @typing.overload
    def __init__(self, symbol: str, properties: int) -> None:
        ...

    @typing.overload
    def __init__(self, symbol: str, properties: int, underlying: QuantConnect.SecurityIdentifier) -> None:
        """
        Initializes a new instance of the SecurityIdentifier class
        
        :param symbol: The base36 string encoded as a long using alpha [0-9A-Z]
        :param properties: Other data defining properties of the symbol including market, security type, listing or expiry date, strike/call/put/style for options, ect...
        :param underlying: Specifies a SecurityIdentifier that represents the underlying security
        """
        ...

    @staticmethod
    def GenerateOption(expiry: datetime.datetime, underlying: QuantConnect.SecurityIdentifier, market: str, strike: float, optionRight: QuantConnect.OptionRight, optionStyle: QuantConnect.OptionStyle) -> QuantConnect.SecurityIdentifier:
        ...

    @staticmethod
    def GenerateFuture(expiry: datetime.datetime, symbol: str, market: str) -> QuantConnect.SecurityIdentifier:
        """
        Generates a new SecurityIdentifier for a future
        
        :param expiry: The date the future expires
        :param symbol: The security's symbol
        :param market: The market
        :returns: A new SecurityIdentifier representing the specified futures security
        """
        ...

    @staticmethod
    @typing.overload
    def GenerateEquity(symbol: str, market: str, mapSymbol: bool = True, mapFileProvider: QuantConnect.Interfaces.IMapFileProvider = None, mappingResolveDate: typing.Optional[datetime.datetime] = None) -> QuantConnect.SecurityIdentifier:
        """
        Helper overload that will search the mapfiles to resolve the first date. This implementation
        uses the configured IMapFileProvider via the Composer.Instance
        
        :param symbol: The symbol as it is known today
        :param market: The market
        :param mapSymbol: Specifies if symbol should be mapped using map file provider
        :param mapFileProvider: Specifies the IMapFileProvider to use for resolving symbols, specify null to load from Composer
        :param mappingResolveDate: The date to use to resolve the map file. Default value is DateTime.Today
        :returns: A new SecurityIdentifier representing the specified symbol today
        """
        ...

    @staticmethod
    @typing.overload
    def GenerateEquity(date: datetime.datetime, symbol: str, market: str) -> QuantConnect.SecurityIdentifier:
        """
        Generates a new SecurityIdentifier for an equity
        
        :param date: The first date this security traded (in LEAN this is the first date in the map_file
        :param symbol: The ticker symbol this security traded under on the
        :param market: The security's market
        :returns: A new SecurityIdentifier representing the specified equity security
        """
        ...

    @staticmethod
    def GenerateConstituentIdentifier(symbol: str, securityType: QuantConnect.SecurityType, market: str) -> QuantConnect.SecurityIdentifier:
        """
        Generates a new SecurityIdentifier for a ConstituentsUniverseData.
        Note that the symbol ticker is case sensitive here.
        
        :param symbol: The ticker to use for this constituent identifier
        :param securityType: The security type of this constituent universe
        :param market: The security's market
        :returns: A new SecurityIdentifier representing the specified constituent universe
        """
        ...

    @staticmethod
    def GenerateBaseSymbol(dataType: System.Type, symbol: str) -> str:
        """
        Generates the Symbol property for QuantConnect.SecurityType.Base security identifiers
        
        :param dataType: The base data custom data type if namespacing is required, null otherwise
        :param symbol: The ticker symbol
        :returns: The value used for the security identifier's Symbol
        """
        ...

    @staticmethod
    def GenerateBase(dataType: System.Type, symbol: str, market: str, mapSymbol: bool = False, date: typing.Optional[datetime.datetime] = None) -> QuantConnect.SecurityIdentifier:
        """
        Generates a new SecurityIdentifier for a custom security with the option of providing the first date
        
        :param dataType: The custom data type
        :param symbol: The ticker symbol of this security
        :param market: The security's market
        :param mapSymbol: Whether or not we should map this symbol
        :param date: First date that the security traded on
        :returns: A new SecurityIdentifier representing the specified base security
        """
        ...

    @staticmethod
    def GenerateForex(symbol: str, market: str) -> QuantConnect.SecurityIdentifier:
        """
        Generates a new SecurityIdentifier for a forex pair
        
        :param symbol: The currency pair in the format similar to: 'EURUSD'
        :param market: The security's market
        :returns: A new SecurityIdentifier representing the specified forex pair
        """
        ...

    @staticmethod
    def GenerateCrypto(symbol: str, market: str) -> QuantConnect.SecurityIdentifier:
        """
        Generates a new SecurityIdentifier for a Crypto pair
        
        :param symbol: The currency pair in the format similar to: 'EURUSD'
        :param market: The security's market
        :returns: A new SecurityIdentifier representing the specified Crypto pair
        """
        ...

    @staticmethod
    def GenerateCfd(symbol: str, market: str) -> QuantConnect.SecurityIdentifier:
        """
        Generates a new SecurityIdentifier for a CFD security
        
        :param symbol: The CFD contract symbol
        :param market: The security's market
        :returns: A new SecurityIdentifier representing the specified CFD security
        """
        ...

    @staticmethod
    def Parse(value: str) -> QuantConnect.SecurityIdentifier:
        ...

    @staticmethod
    def TryParse(value: str, identifier: QuantConnect.SecurityIdentifier) -> bool:
        """
        Attempts to parse the specified value as a SecurityIdentifier.
        
        :param value: The string value to be parsed
        :param identifier: The result of parsing, when this function returns true,  was properly created and reflects the input string, when this function returns false  will equal default(SecurityIdentifier)
        :returns: True on success, otherwise false
        """
        ...

    @typing.overload
    def Equals(self, other: QuantConnect.SecurityIdentifier) -> bool:
        ...

    @typing.overload
    def Equals(self, obj: System.Object) -> bool:
        """
        Determines whether the specified System.Object is equal to the current System.Object.
        
        :param obj: The object to compare with the current object.
        :returns: true if the specified object  is equal to the current object; otherwise, false.
        """
        ...

    def GetHashCode(self) -> int:
        """
        Serves as a hash function for a particular type.
        
        :returns: A hash code for the current System.Object.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...


class Symbol(System.Object, System.IEquatable[QuantConnect_Symbol], System.IComparable):
    """
    Represents a unique security identifier. This is made of two components,
    the unique SID and the Value. The value is the current ticker symbol while
    the SID is constant over the life of a security
    """

    Empty: QuantConnect.Symbol = ...
    """
    Represents an unassigned symbol. This is intended to be used as an
    uninitialized, default value
    """

    # Cannot convert to Python: None: QuantConnect.Symbol = ...
    """Represents no symbol. This is intended to be used when no symbol is explicitly intended"""

    @property
    def Value(self) -> str:
        ...

    @Value.setter
    def Value(self, value: str):
        ...

    @property
    def ID(self) -> QuantConnect.SecurityIdentifier:
        """Gets the security identifier for this symbol"""
        ...

    @ID.setter
    def ID(self, value: QuantConnect.SecurityIdentifier):
        """Gets the security identifier for this symbol"""
        ...

    @property
    def HasUnderlying(self) -> bool:
        """
        Gets whether or not this Symbol is a derivative,
        that is, it has a valid Underlying property
        """
        ...

    @property
    def Underlying(self) -> QuantConnect.Symbol:
        """Gets the security underlying symbol, if any"""
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Symbol):
        """Gets the security underlying symbol, if any"""
        ...

    @property
    def SecurityType(self) -> QuantConnect.SecurityType:
        """Gets the security type of the symbol"""
        ...

    @staticmethod
    def Create(ticker: str, securityType: QuantConnect.SecurityType, market: str, alias: str = None, baseDataType: System.Type = None) -> QuantConnect.Symbol:
        """
        Provides a convenience method for creating a Symbol for most security types.
        This method currently does not support Commodities
        
        :param ticker: The string ticker symbol
        :param securityType: The security type of the ticker. If securityType == Option, then a canonical symbol is created
        :param market: The market the ticker resides in
        :param alias: An alias to be used for the symbol cache. Required when adding the same security from different markets
        :param baseDataType: Optional for SecurityType.Base and used for generating the base data SID
        :returns: A new Symbol object for the specified ticker
        """
        ...

    @staticmethod
    def CreateBase(baseType: System.Type, underlying: typing.Union[QuantConnect.Symbol, str], market: str) -> QuantConnect.Symbol:
        """
        Creates a new Symbol for custom data. This method allows for the creation of a new Base Symbol
        using the first ticker and the first traded date from the provided underlying Symbol. This avoids
        the issue for mappable types, where the ticker is remapped supposing the provided ticker value is from today.
        See method SecurityIdentifier.GetFirstTickerAndDate(Interfaces.IMapFileProvider, string, string)
        The provided symbol is also set to Symbol.Underlying so that it can be accessed using the custom data Symbol.
        This is useful for associating custom data Symbols to other asset classes so that it is possible to filter using custom data
        and place trades on the underlying asset based on the filtered custom data.
        
        :param baseType: Type of BaseData instance
        :param underlying: Underlying symbol to set for the Base Symbol
        :param market: Market
        :returns: New non-mapped Base Symbol that contains an Underlying Symbol
        """
        ...

    @staticmethod
    @typing.overload
    def CreateOption(underlying: str, market: str, style: QuantConnect.OptionStyle, right: QuantConnect.OptionRight, strike: float, expiry: datetime.datetime, alias: str = None, mapSymbol: bool = True) -> QuantConnect.Symbol:
        """
        Provides a convenience method for creating an option Symbol.
        
        :param underlying: The underlying ticker
        :param market: The market the underlying resides in
        :param style: The option style (American, European, ect..)
        :param right: The option right (Put/Call)
        :param strike: The option strike price
        :param expiry: The option expiry date
        :param alias: An alias to be used for the symbol cache. Required when adding the same security from different markets
        :param mapSymbol: Specifies if symbol should be mapped using map file provider
        :returns: A new Symbol object for the specified option contract
        """
        ...

    @staticmethod
    @typing.overload
    def CreateOption(underlyingSymbol: typing.Union[QuantConnect.Symbol, str], market: str, style: QuantConnect.OptionStyle, right: QuantConnect.OptionRight, strike: float, expiry: datetime.datetime, alias: str = None) -> QuantConnect.Symbol:
        """
        Provides a convenience method for creating an option Symbol using SecurityIdentifier.
        
        :param underlyingSymbol: The underlying security symbol
        :param market: The market the underlying resides in
        :param style: The option style (American, European, ect..)
        :param right: The option right (Put/Call)
        :param strike: The option strike price
        :param expiry: The option expiry date
        :param alias: An alias to be used for the symbol cache. Required when adding the same security from diferent markets
        :returns: A new Symbol object for the specified option contract
        """
        ...

    @staticmethod
    def CreateFuture(ticker: str, market: str, expiry: datetime.datetime, alias: str = None) -> QuantConnect.Symbol:
        """
        Provides a convenience method for creating a future Symbol.
        
        :param ticker: The ticker
        :param market: The market the future resides in
        :param expiry: The future expiry date
        :param alias: An alias to be used for the symbol cache. Required when adding the same security from different markets
        :returns: A new Symbol object for the specified future contract
        """
        ...

    def IsCanonical(self) -> bool:
        """
        Method returns true, if symbol is a derivative canonical symbol
        
        :returns: true, if symbol is a derivative canonical symbol
        """
        ...

    def HasUnderlyingSymbol(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Determines if the specified  is an underlying of this symbol instance
        
        :param symbol: The underlying to check for
        :returns: True if the specified  is an underlying of this symbol instance
        """
        ...

    def __init__(self, sid: QuantConnect.SecurityIdentifier, value: str) -> None:
        ...

    def UpdateMappedSymbol(self, mappedSymbol: str) -> QuantConnect.Symbol:
        """
        Creates new symbol with updated mapped symbol. Symbol Mapping: When symbols change over time (e.g. CHASE-> JPM) need to update the symbol requested.
        Method returns newly created symbol
        """
        ...

    @typing.overload
    def Equals(self, obj: System.Object) -> bool:
        ...

    def GetHashCode(self) -> int:
        """
        Serves as a hash function for a particular type.
        
        :returns: A hash code for the current System.Object.
        """
        ...

    def CompareTo(self, obj: System.Object) -> int:
        """
        Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A value that indicates the relative order of the objects being compared. The return value has these meanings: Value Meaning Less than zero This instance precedes  in the sort order. Zero This instance occurs in the same position in the sort order as . Greater than zero This instance follows  in the sort order.
        """
        ...

    def ToString(self) -> str:
        """
        Returns a string that represents the current object.
        
        :returns: A string that represents the current object.
        """
        ...

    @typing.overload
    def Equals(self, other: typing.Union[QuantConnect.Symbol, str]) -> bool:
        ...

    def Contains(self, value: str) -> bool:
        ...

    def EndsWith(self, value: str) -> bool:
        ...

    def StartsWith(self, value: str) -> bool:
        ...

    def ToLower(self) -> str:
        ...

    def ToUpper(self) -> str:
        ...


class SymbolCache(System.Object):
    """
    Provides a string->Symbol mapping to allow for user defined strings to be lifted into a Symbol
    This is mainly used via the Symbol implicit operator, but also functions that create securities
    should also call Set to add new mappings
    """

    class Cache(System.Object):
        """This class has no documentation."""

        @property
        def Symbols(self) -> System.Collections.Concurrent.ConcurrentDictionary[str, QuantConnect.Symbol]:
            ...

        @property
        def Tickers(self) -> System.Collections.Concurrent.ConcurrentDictionary[QuantConnect.Symbol, str]:
            ...

        def TryGetSymbol(self, ticker: str, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
            """
            Attempts to resolve the ticker to a Symbol via the cache. If not found in the
            cache then
            
            :param ticker: The ticker to resolver to a symbol
            :param symbol: The resolves symbol
            :returns: True if we successfully resolved a symbol, false otherwise
            """
            ...

    @staticmethod
    def Set(ticker: str, symbol: typing.Union[QuantConnect.Symbol, str]) -> None:
        """
        Adds a mapping for the specified ticker
        
        :param ticker: The string ticker symbol
        :param symbol: The symbol object that maps to the string ticker symbol
        """
        ...

    @staticmethod
    def GetSymbol(ticker: str) -> QuantConnect.Symbol:
        """
        Gets the Symbol object that is mapped to the specified string ticker symbol
        
        :param ticker: The string ticker symbol
        :returns: The symbol object that maps to the specified string ticker symbol
        """
        ...

    @staticmethod
    def TryGetSymbol(ticker: str, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Gets the Symbol object that is mapped to the specified string ticker symbol
        
        :param ticker: The string ticker symbol
        :param symbol: The output symbol object
        :returns: The symbol object that maps to the specified string ticker symbol
        """
        ...

    @staticmethod
    def GetTicker(symbol: typing.Union[QuantConnect.Symbol, str]) -> str:
        """
        Gets the string ticker symbol that is mapped to the specified Symbol
        
        :param symbol: The symbol object
        :returns: The string ticker symbol that maps to the specified symbol object
        """
        ...

    @staticmethod
    def TryGetTicker(symbol: typing.Union[QuantConnect.Symbol, str], ticker: str) -> bool:
        """
        Gets the string ticker symbol that is mapped to the specified Symbol
        
        :param symbol: The symbol object
        :param ticker: The output string ticker symbol
        :returns: The string ticker symbol that maps to the specified symbol object
        """
        ...

    @staticmethod
    @typing.overload
    def TryRemove(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Removes the mapping for the specified symbol from the cache
        
        :param symbol: The symbol whose mappings are to be removed
        :returns: True if the symbol mapping were removed from the cache
        """
        ...

    @staticmethod
    @typing.overload
    def TryRemove(ticker: str) -> bool:
        """
        Removes the mapping for the specified symbol from the cache
        
        :param ticker: The ticker whose mappings are to be removed
        :returns: True if the symbol mapping were removed from the cache
        """
        ...

    @staticmethod
    def Clear() -> None:
        """Clears the current caches"""
        ...


class Parse(System.Object):
    """Provides methods for parsing strings using CultureInfo.InvariantCulture"""

    @staticmethod
    def TimeSpan(value: str) -> datetime.timedelta:
        """
        Parses the provided value as a System.TimeSpan using System.TimeSpan.Parse(string,IFormatProvider)
        with CultureInfo.InvariantCulture
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(input: str, value: datetime.timedelta) -> bool:
        """Tries to parse the provided value with TryParse as a System.TimeSpan using CultureInfo.InvariantCulture."""
        ...

    @staticmethod
    @typing.overload
    def TryParseExact(input: str, format: str, timeSpanStyle: System.Globalization.TimeSpanStyles, value: datetime.timedelta) -> bool:
        """
        Tries to parse the provided value with TryParse as a System.TimeSpan, format
        string, TimeSpanStyles, and using CultureInfo.InvariantCulture
        """
        ...

    @staticmethod
    def DateTime(value: str) -> datetime.datetime:
        """
        Parses the provided value as a System.DateTime using System.DateTime.Parse(string,IFormatProvider)
        with CultureInfo.InvariantCulture
        """
        ...

    @staticmethod
    @typing.overload
    def DateTimeExact(value: str, format: str) -> datetime.datetime:
        """
        Parses the provided value as a System.DateTime using System.DateTime.ParseExact(string,string,IFormatProvider)
        with the specified  and CultureInfo.InvariantCulture
        """
        ...

    @staticmethod
    @typing.overload
    def DateTimeExact(value: str, format: str, dateTimeStyles: System.Globalization.DateTimeStyles) -> datetime.datetime:
        """
        Parses the provided value as a System.DateTime using System.DateTime.ParseExact(string,string,IFormatProvider)
        with the specified ,  and CultureInfo.InvariantCulture
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(input: str, dateTimeStyle: System.Globalization.DateTimeStyles, value: datetime.datetime) -> bool:
        """
        Tries to parse the provided value with TryParse as a System.DateTime using the specified 
        and CultureInfo.InvariantCulture.
        """
        ...

    @staticmethod
    @typing.overload
    def TryParseExact(input: str, format: str, dateTimeStyle: System.Globalization.DateTimeStyles, value: datetime.datetime) -> bool:
        """
        Tries to parse the provided value with TryParse as a System.DateTime using the
        specified , the format , and
        CultureInfo.InvariantCulture.
        """
        ...

    @staticmethod
    def Double(value: str) -> float:
        """Parses the provided value as a double using CultureInfo.InvariantCulture"""
        ...

    @staticmethod
    @typing.overload
    def TryParse(input: str, numberStyle: System.Globalization.NumberStyles, value: float) -> bool:
        """
        Tries to parse the provided value with TryParse as a double using the specified 
        and CultureInfo.InvariantCulture.
        """
        ...

    @staticmethod
    @typing.overload
    def Decimal(value: str) -> float:
        """Parses the provided value as a decimal using CultureInfo.InvariantCulture"""
        ...

    @staticmethod
    @typing.overload
    def Decimal(value: str, numberStyles: System.Globalization.NumberStyles) -> float:
        """
        Parses the provided value as a decimal using the specified 
        and CultureInfo.InvariantCulture
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(input: str, numberStyle: System.Globalization.NumberStyles, value: float) -> bool:
        """
        Tries to parse the provided value with TryParse as a decimal using the specified 
        and CultureInfo.InvariantCulture.
        """
        ...

    @staticmethod
    def Int(value: str) -> int:
        """Parses the provided value as a int using CultureInfo.InvariantCulture"""
        ...

    @staticmethod
    @typing.overload
    def TryParse(input: str, numberStyle: System.Globalization.NumberStyles, value: int) -> bool:
        """
        Tries to parse the provided value with TryParse as a int using the specified 
        and CultureInfo.InvariantCulture.
        """
        ...

    @staticmethod
    @typing.overload
    def Long(value: str) -> int:
        """Parses the provided value as a long using CultureInfo.InvariantCulture"""
        ...

    @staticmethod
    @typing.overload
    def Long(value: str, numberStyles: System.Globalization.NumberStyles) -> int:
        """
        Parses the provided value as a long using CultureInfo.InvariantCulture
        and the specified
        """
        ...

    @staticmethod
    @typing.overload
    def TryParse(input: str, numberStyle: System.Globalization.NumberStyles, value: int) -> bool:
        """
        Tries to parse the provided value with TryParse as a long using the specified 
        and CultureInfo.InvariantCulture.
        """
        ...


class TimeZoneOffsetProvider(System.Object):
    """
    Represents the discontinuties in a single time zone and provides offsets to UTC.
    This type assumes that times will be asked in a forward marching manner.
    This type is not thread safe.
    """

    @property
    def TimeZone(self) -> typing.Any:
        """Gets the time zone this instances provides offsets for"""
        ...

    def __init__(self, timeZone: typing.Any, utcStartTime: datetime.datetime, utcEndTime: datetime.datetime) -> None:
        """
        Initializes a new instance of the TimeZoneOffsetProvider class
        
        :param timeZone: The time zone to provide offsets for
        :param utcStartTime: The start of the range of offsets
        :param utcEndTime: The end of the range of offsets
        """
        ...

    def GetOffsetTicks(self, utcTime: datetime.datetime) -> int:
        """
        Gets the offset in ticks from this time zone to UTC, such that UTC time + offset = local time
        
        :param utcTime: The time in UTC to get an offset to local
        :returns: The offset in ticks between UTC and the local time zone
        """
        ...

    def ConvertToUtc(self, localTime: datetime.datetime) -> datetime.datetime:
        """
        Converts the specified local time to UTC. This function will advance this offset provider
        
        :param localTime: The local time to be converted to UTC
        :returns: The specified time in UTC
        """
        ...

    def GetNextDiscontinuity(self) -> int:
        """
        Gets this offset provider's next discontinuity
        
        :returns: The next discontinuity in UTC ticks
        """
        ...

    def ConvertFromUtc(self, utcTime: datetime.datetime) -> datetime.datetime:
        """
        Converts the specified  using the offset resolved from
        a call to GetOffsetTicks
        
        :param utcTime: The time to convert from utc
        :returns: The same instant in time represented in the TimeZone
        """
        ...


class TradingDayType(System.Enum):
    """Enum lists available trading events"""

    BusinessDay = 0
    """Business day"""

    PublicHoliday = 1
    """Public Holiday"""

    Weekend = 2
    """Weekend"""

    OptionExpiration = 3
    """Option Expiration Date"""

    FutureExpiration = 4
    """Futures Expiration Date"""

    FutureRoll = 5
    """Futures Roll Date"""

    SymbolDelisting = 6
    """Symbol Delisting Date"""

    EquityDividends = 7
    """Equity Ex-dividend Date"""

    EconomicEvent = 8
    """FX Economic Event"""


class TradingDay(System.Object):
    """Class contains trading events associated with particular day in TradingCalendar"""

    @property
    def Date(self) -> datetime.datetime:
        """The date that this instance is associated with"""
        ...

    @Date.setter
    def Date(self, value: datetime.datetime):
        """The date that this instance is associated with"""
        ...

    @property
    def BusinessDay(self) -> bool:
        """Property returns true, if the day is a business day"""
        ...

    @BusinessDay.setter
    def BusinessDay(self, value: bool):
        """Property returns true, if the day is a business day"""
        ...

    @property
    def PublicHoliday(self) -> bool:
        """Property returns true, if the day is a public holiday"""
        ...

    @PublicHoliday.setter
    def PublicHoliday(self, value: bool):
        """Property returns true, if the day is a public holiday"""
        ...

    @property
    def Weekend(self) -> bool:
        """Property returns true, if the day is a weekend"""
        ...

    @Weekend.setter
    def Weekend(self, value: bool):
        """Property returns true, if the day is a weekend"""
        ...

    @property
    def OptionExpirations(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """Property returns the list of options (among currently traded) that expire on this day"""
        ...

    @OptionExpirations.setter
    def OptionExpirations(self, value: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]):
        """Property returns the list of options (among currently traded) that expire on this day"""
        ...

    @property
    def FutureExpirations(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """Property returns the list of futures (among currently traded) that expire on this day"""
        ...

    @FutureExpirations.setter
    def FutureExpirations(self, value: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]):
        """Property returns the list of futures (among currently traded) that expire on this day"""
        ...

    @property
    def FutureRolls(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """Property returns the list of futures (among currently traded) that roll forward on this day"""
        ...

    @FutureRolls.setter
    def FutureRolls(self, value: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]):
        """Property returns the list of futures (among currently traded) that roll forward on this day"""
        ...

    @property
    def SymbolDelistings(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """Property returns the list of symbols (among currently traded) that are delisted on this day"""
        ...

    @SymbolDelistings.setter
    def SymbolDelistings(self, value: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]):
        """Property returns the list of symbols (among currently traded) that are delisted on this day"""
        ...

    @property
    def EquityDividends(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """Property returns the list of symbols (among currently traded) that have ex-dividend date on this day"""
        ...

    @EquityDividends.setter
    def EquityDividends(self, value: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]):
        """Property returns the list of symbols (among currently traded) that have ex-dividend date on this day"""
        ...


class ExtendedDictionary(typing.Generic[QuantConnect_ExtendedDictionary_T], System.Object, QuantConnect.Interfaces.IExtendedDictionary[QuantConnect.Symbol, QuantConnect_ExtendedDictionary_T], metaclass=abc.ABCMeta):
    """Provides a base class for types holding instances keyed by Symbol"""

    @property
    @abc.abstractmethod
    def GetKeys(self) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Gets an System.Collections.Generic.ICollection`1 containing the Symbol objects of the System.Collections.Generic.IDictionary`2.
        
        This property is protected.
        """
        ...

    @property
    @abc.abstractmethod
    def GetValues(self) -> System.Collections.Generic.IEnumerable[QuantConnect_ExtendedDictionary_T]:
        """
        Gets an System.Collections.Generic.ICollection`1 containing the values in the System.Collections.Generic.IDictionary`2.
        
        This property is protected.
        """
        ...

    @property
    def IsReadOnly(self) -> bool:
        """Gets a value indicating whether the IDictionary object is read-only."""
        ...

    def Clear(self) -> None:
        """Removes all items from the System.Collections.Generic.ICollection`1."""
        ...

    def TryGetValue(self, symbol: typing.Union[QuantConnect.Symbol, str], value: QuantConnect_ExtendedDictionary_T) -> bool:
        """
        Gets the value associated with the specified Symbol.
        
        :param symbol: The Symbol whose value to get.
        :param value: When this method returns, the value associated with the specified Symbol, if the Symbol is found; otherwise, the default value for the type of the  parameter. This parameter is passed uninitialized.
        :returns: true if the object that implements System.Collections.Generic.IDictionary`2 contains an element with the specified Symbol; otherwise, false.
        """
        ...

    def Remove(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Removes the value with the specified Symbol
        
        :param symbol: The Symbol object of the element to remove.
        :returns: true if the element is successfully found and removed; otherwise, false.
        """
        ...

    @typing.overload
    def __getitem__(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect_ExtendedDictionary_T:
        """
        Indexer method for the base dictioanry to access the objects by their symbol.
        
        :param symbol: Symbol object indexer
        :returns: Object of T
        """
        ...

    @typing.overload
    def __setitem__(self, symbol: typing.Union[QuantConnect.Symbol, str], value: QuantConnect_ExtendedDictionary_T) -> None:
        """
        Indexer method for the base dictioanry to access the objects by their symbol.
        
        :param symbol: Symbol object indexer
        :returns: Object of T
        """
        ...

    @typing.overload
    def __getitem__(self, ticker: str) -> QuantConnect_ExtendedDictionary_T:
        """
        Indexer method for the base dictioanry to access the objects by their symbol.
        
        :param ticker: string ticker symbol indexer
        :returns: Object of T
        """
        ...

    @typing.overload
    def __setitem__(self, ticker: str, value: QuantConnect_ExtendedDictionary_T) -> None:
        """
        Indexer method for the base dictioanry to access the objects by their symbol.
        
        :param ticker: string ticker symbol indexer
        :returns: Object of T
        """
        ...

    def clear(self) -> None:
        """Removes all keys and values from the IExtendedDictionary{TKey, TValue}."""
        ...

    def copy(self) -> typing.Dict[typing.Any, typing.Any]:
        """
        Creates a shallow copy of the IExtendedDictionary{TKey, TValue}.
        
        :returns: Returns a shallow copy of the dictionary. It doesn't modify the original dictionary.
        """
        ...

    @typing.overload
    def fromkeys(self, sequence: typing.List[QuantConnect.Symbol]) -> typing.Dict[typing.Any, typing.Any]:
        """
        Creates a new dictionary from the given sequence of elements.
        
        :param sequence: Sequence of elements which is to be used as keys for the new dictionary
        :returns: Returns a new dictionary with the given sequence of elements as the keys of the dictionary.
        """
        ...

    @typing.overload
    def fromkeys(self, sequence: typing.List[QuantConnect.Symbol], value: QuantConnect_ExtendedDictionary_T) -> typing.Dict[typing.Any, typing.Any]:
        """
        Creates a new dictionary from the given sequence of elements with a value provided by the user.
        
        :param sequence: Sequence of elements which is to be used as keys for the new dictionary
        :param value: Value which is set to each each element of the dictionary
        :returns: Returns a new dictionary with the given sequence of elements as the keys of the dictionary. Each element of the newly created dictionary is set to the provided value.
        """
        ...

    @typing.overload
    def get(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect_ExtendedDictionary_T:
        """
        Returns the value for the specified Symbol if Symbol is in dictionary.
        
        :param symbol: Symbol to be searched in the dictionary
        :returns: The value for the specified Symbol if Symbol is in dictionary. None if the Symbol is not found and value is not specified.
        """
        ...

    @typing.overload
    def get(self, symbol: typing.Union[QuantConnect.Symbol, str], value: QuantConnect_ExtendedDictionary_T) -> QuantConnect_ExtendedDictionary_T:
        """
        Returns the value for the specified Symbol if Symbol is in dictionary.
        
        :param symbol: Symbol to be searched in the dictionary
        :param value: Value to be returned if the Symbol is not found. The default value is null.
        :returns: The value for the specified Symbol if Symbol is in dictionary. value if the Symbol is not found and value is specified.
        """
        ...

    def items(self) -> typing.List[typing.Any]:
        """
        Returns a view object that displays a list of dictionary's (Symbol, value) tuple pairs.
        
        :returns: Returns a view object that displays a list of a given dictionary's (Symbol, value) tuple pair.
        """
        ...

    def popitem(self) -> typing.Any:
        """
        Returns and removes an arbitrary element (Symbol, value) pair from the dictionary.
        
        :returns: Returns an arbitrary element (Symbol, value) pair from the dictionary removes an arbitrary element(the same element which is returned) from the dictionary. Note: Arbitrary elements and random elements are not same.The popitem() doesn't return a random element.
        """
        ...

    @typing.overload
    def setdefault(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect_ExtendedDictionary_T:
        """
        Returns the value of a Symbol (if the Symbol is in dictionary). If not, it inserts Symbol with a value to the dictionary.
        
        :param symbol: Key with null/None value is inserted to the dictionary if Symbol is not in the dictionary.
        :returns: The value of the Symbol if it is in the dictionary None if Symbol is not in the dictionary
        """
        ...

    @typing.overload
    def setdefault(self, symbol: typing.Union[QuantConnect.Symbol, str], default_value: QuantConnect_ExtendedDictionary_T) -> QuantConnect_ExtendedDictionary_T:
        """
        Returns the value of a Symbol (if the Symbol is in dictionary). If not, it inserts Symbol with a value to the dictionary.
        
        :param symbol: Key with a value default_value is inserted to the dictionary if Symbol is not in the dictionary.
        :param default_value: Default value
        :returns: The value of the Symbol if it is in the dictionary default_value if Symbol is not in the dictionary and default_value is specified
        """
        ...

    @typing.overload
    def pop(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect_ExtendedDictionary_T:
        """
        Removes and returns an element from a dictionary having the given Symbol.
        
        :param symbol: Key which is to be searched for removal
        :returns: If Symbol is found - removed/popped element from the dictionary If Symbol is not found - KeyError exception is raised
        """
        ...

    @typing.overload
    def pop(self, symbol: typing.Union[QuantConnect.Symbol, str], default_value: QuantConnect_ExtendedDictionary_T) -> QuantConnect_ExtendedDictionary_T:
        """
        Removes and returns an element from a dictionary having the given Symbol.
        
        :param symbol: Key which is to be searched for removal
        :param default_value: Value which is to be returned when the Symbol is not in the dictionary
        :returns: If Symbol is found - removed/popped element from the dictionary If Symbol is not found - value specified as the second argument(default)
        """
        ...

    def update(self, other: typing.Any) -> None:
        """
        Updates the dictionary with the elements from the another dictionary object or from an iterable of Symbol/value pairs.
        The update() method adds element(s) to the dictionary if the Symbol is not in the dictionary.If the Symbol is in the dictionary, it updates the Symbol with the new value.
        
        :param other: Takes either a dictionary or an iterable object of Symbol/value pairs (generally tuples).
        """
        ...

    def keys(self) -> typing.List[typing.Any]:
        """
        Returns a view object that displays a list of all the Symbol objects in the dictionary
        
        :returns: Returns a view object that displays a list of all the Symbol objects. When the dictionary is changed, the view object also reflect these changes.
        """
        ...

    def values(self) -> typing.List[typing.Any]:
        """
        Returns a view object that displays a list of all the values in the dictionary.
        
        :returns: Returns a view object that displays a list of all values in a given dictionary.
        """
        ...


class SymbolJsonConverter(JsonConverter):
    """
    Defines a JsonConverter to be used when deserializing to
    the Symbol class.
    """

    def WriteJson(self, writer: typing.Any, value: System.Object, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object.
        
        :param writer: The Newtonsoft.Json.JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
        """
        ...

    def ReadJson(self, reader: typing.Any, objectType: System.Type, existingValue: System.Object, serializer: typing.Any) -> System.Object:
        """
        Reads the JSON representation of the object.
        
        :param reader: The Newtonsoft.Json.JsonReader to read from.
        :param objectType: Type of the object.
        :param existingValue: The existing value of object being read.
        :param serializer: The calling serializer.
        :returns: The object value.
        """
        ...

    def CanConvert(self, objectType: System.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param objectType: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...


class OS(System.Object):
    """Operating systems class for managing anything that is operation system specific."""

    IsLinux: bool
    """Global Flag :: Operating System"""

    IsWindows: bool
    """Global Flag :: Operating System"""

    PathSeparation: str
    """Character Separating directories in this OS:"""

    DriveSpaceRemaining: int
    """Get the drive space remaining on windows and linux in MB"""

    DriveSpaceUsed: int
    """Get the drive space remaining on windows and linux in MB"""

    DriveTotalSpace: int
    """Total space on the drive"""

    ApplicationMemoryUsed: int
    """Gets the amount of private memory allocated for the current process (includes both managed and unmanaged memory)."""

    TotalPhysicalMemoryUsed: int
    """Get the RAM used on the machine:"""

    CpuUsage: float
    """Total CPU usage as a percentage"""

    @staticmethod
    def GetServerStatistics() -> System.Collections.Generic.Dictionary[str, str]:
        """Gets the statistics of the machine, including CPU% and RAM"""
        ...


class IsolatorLimitResult(System.Object):
    """Represents the result of the Isolator limiter callback"""

    @property
    def CurrentTimeStepElapsed(self) -> datetime.timedelta:
        """Gets the amount of time spent on the current time step"""
        ...

    @property
    def ErrorMessage(self) -> str:
        """Gets the error message or an empty string if no error on the current time step"""
        ...

    @property
    def IsWithinCustomLimits(self) -> bool:
        """Returns true if there are no errors in the current time step"""
        ...

    def __init__(self, currentTimeStepElapsed: datetime.timedelta, errorMessage: str) -> None:
        """
        Initializes a new instance of the IsolatorLimitResult class
        
        :param currentTimeStepElapsed: The amount of time spent on the current time step
        :param errorMessage: The error message or an empty string if no error on the current time step
        """
        ...


class Isolator(System.Object):
    """
    Isolator class - create a new instance of the algorithm and ensure it doesn't
    exceed memory or time execution limits.
    """

    @property
    def CancellationTokenSource(self) -> System.Threading.CancellationTokenSource:
        """Algo cancellation controls - cancel source."""
        ...

    @CancellationTokenSource.setter
    def CancellationTokenSource(self, value: System.Threading.CancellationTokenSource):
        """Algo cancellation controls - cancel source."""
        ...

    @property
    def CancellationToken(self) -> System.Threading.CancellationToken:
        """Algo cancellation controls - cancellation token for algorithm thread."""
        ...

    @property
    def IsCancellationRequested(self) -> bool:
        """Check if this task isolator is cancelled, and exit the analysis"""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the Isolator class"""
        ...

    @typing.overload
    def ExecuteWithTimeLimit(self, timeSpan: datetime.timedelta, withinCustomLimits: typing.Callable[[], QuantConnect.IsolatorLimitResult], codeBlock: System.Action, memoryCap: int = 1024, sleepIntervalMillis: int = 1000, workerThread: QuantConnect.Util.WorkerThread = None) -> bool:
        """
        Execute a code block with a maximum limit on time and memory.
        
        :param timeSpan: Timeout in timespan
        :param withinCustomLimits: Function used to determine if the codeBlock is within custom limits, such as with algorithm manager timing individual time loops, return a non-null and non-empty string with a message indicating the error/reason for stoppage
        :param codeBlock: Action codeblock to execute
        :param memoryCap: Maximum memory allocation, default 1024Mb
        :param sleepIntervalMillis: Sleep interval between each check in ms
        :param workerThread: The worker thread instance that will execute the provided action, if null will use a Task
        :returns: True if algorithm exited successfully, false if cancelled because it exceeded limits.
        """
        ...

    @typing.overload
    def ExecuteWithTimeLimit(self, timeSpan: datetime.timedelta, codeBlock: System.Action, memoryCap: int, sleepIntervalMillis: int = 1000, workerThread: QuantConnect.Util.WorkerThread = None) -> bool:
        """
        Execute a code block with a maximum limit on time and memory.
        
        :param timeSpan: Timeout in timespan
        :param codeBlock: Action codeblock to execute
        :param memoryCap: Maximum memory allocation, default 1024Mb
        :param sleepIntervalMillis: Sleep interval between each check in ms
        :param workerThread: The worker thread instance that will execute the provided action, if null will use a Task
        :returns: True if algorithm exited successfully, false if cancelled because it exceeded limits.
        """
        ...


class StringExtensions(System.Object):
    """
    Provides extension methods for properly parsing and serializing values while properly using
    an IFormatProvider/CultureInfo when applicable
    """

    @staticmethod
    @typing.overload
    def ConvertInvariant(value: System.Object) -> QuantConnect_StringExtensions_T:
        """
        Converts the provided  as T
        using CultureInfo
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertInvariant(value: System.Object, conversionType: System.Type) -> System.Object:
        """
        Converts the provided  as 
        using CultureInfo
        """
        ...

    @staticmethod
    def Invariant(formattable: System.FormattableString) -> str:
        """
        Non-extension method alias for FormattableString.Invariant
        This supports the using static QuantConnect.StringExtensions syntax
        and is aimed at ensuring all formatting is piped through this class instead of
        alternatively piping through directly to FormattableString.Invariant
        """
        ...

    @staticmethod
    @typing.overload
    def ToStringInvariant(convertible: System.IConvertible) -> str:
        """Converts the provided value to a string using CultureInfo"""
        ...

    @staticmethod
    @typing.overload
    def ToStringInvariant(formattable: System.IFormattable, format: str) -> str:
        """
        Formats the provided value using the specified  and
        CultureInfo
        """
        ...

    @staticmethod
    def ToIso8601Invariant(dateTime: datetime.datetime) -> str:
        """Provides a convenience methods for converting a DateTime to an invariant ISO-8601 string"""
        ...

    @staticmethod
    def StartsWithInvariant(value: str, beginning: str, ignoreCase: bool = False) -> bool:
        """
        Checks if the string starts with the provided  using CultureInfo
        while optionally ignoring case.
        """
        ...

    @staticmethod
    def EndsWithInvariant(value: str, ending: str, ignoreCase: bool = False) -> bool:
        """
        Checks if the string ends with the provided  using CultureInfo
        while optionally ignoring case.
        """
        ...

    @staticmethod
    @typing.overload
    def IndexOfInvariant(value: str, character: str) -> int:
        """Gets the index of the specified  using StringComparison"""
        ...

    @staticmethod
    @typing.overload
    def IndexOfInvariant(value: str, substring: str, ignoreCase: bool = False) -> int:
        """
        Gets the index of the specified  using StringComparison
        or System.StringComparison.InvariantCultureIgnoreCase when  is true
        """
        ...

    @staticmethod
    def LastIndexOfInvariant(value: str, substring: str, ignoreCase: bool = False) -> int:
        """
        Gets the index of the specified  using StringComparison
        or System.StringComparison.InvariantCultureIgnoreCase when  is true
        """
        ...

    @staticmethod
    @typing.overload
    def IfNotNullOrEmpty(value: str, defaultValue: QuantConnect_StringExtensions_T, func: typing.Callable[[str], QuantConnect_StringExtensions_T]) -> QuantConnect_StringExtensions_T:
        """
        Provides a shorthand for avoiding the more verbose ternary equivalent.
        Consider the following:
        
        string.IsNullOrEmpty(str) ? (decimal?)null : Convert.ToDecimal(str, CultureInfo.InvariantCulture)
        
        Can be expressed as:
        
        str.IfNotNullOrEmpty<decimal?>(s => Convert.ToDecimal(str, CultureInfo.InvariantCulture))
        
        When combined with additional methods from this class, reducing further to a declarative:
        
        str.IfNotNullOrEmpty<decimal?>(s => s.ParseDecimalInvariant())
        str.IfNotNullOrEmpty<decimal?>(s => s.ConvertInvariant<decimal>())
        """
        ...

    @staticmethod
    @typing.overload
    def IfNotNullOrEmpty(value: str, func: typing.Callable[[str], QuantConnect_StringExtensions_T]) -> QuantConnect_StringExtensions_T:
        """
        Provides a shorthand for avoiding the more verbose ternary equivalent.
        Consider the following:
        
        string.IsNullOrEmpty(str) ? (decimal?)null : Convert.ToDecimal(str, CultureInfo.InvariantCulture)
        
        Can be expressed as:
        
        str.IfNotNullOrEmpty<decimal?>(s => Convert.ToDecimal(str, CultureInfo.InvariantCulture))
        
        When combined with additional methods from this class, reducing further to a declarative:
        
        str.IfNotNullOrEmpty<decimal?>(s => s.ParseDecimalInvariant())
        str.IfNotNullOrEmpty<decimal?>(s => s.ConvertInvariant<decimal>())
        """
        ...

    @staticmethod
    def SafeSubstring(value: str, startIndex: int, length: int) -> str:
        """
        Retrieves a substring from this instance. The substring starts at a specified
        character position and has a specified length.
        """
        ...


class DateFormat(System.Object):
    """Shortcut date format strings"""

    SixCharacter: str = "yyMMdd"

    EightCharacter: str = "yyyyMMdd"

    TwelveCharacter: str = "yyyyMMdd HH:mm"

    JsonFormat: str = "yyyy-MM-ddTHH:mm:ss"

    DB: str = "yyyy-MM-dd HH:mm:ss"

    UI: str = "yyyy-MM-dd HH:mm:ss"

    USShort: str = "M/d/yy h:mm tt"

    USShortDateOnly: str = "M/d/yy"

    US: str = "M/d/yyyy h:mm:ss tt"

    USDateOnly: str = "M/d/yyyy"

    Forex: str = "yyyyMMdd HH:mm:ss.ffff"

    YearMonth: str = "yyyyMM"


class Holding(System.Object):
    """Singular holding of assets from backend live nodes:"""

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        ...

    @Symbol.setter
    def Symbol(self, value: QuantConnect.Symbol):
        ...

    @property
    def Type(self) -> QuantConnect.SecurityType:
        ...

    @Type.setter
    def Type(self, value: QuantConnect.SecurityType):
        ...

    @property
    def CurrencySymbol(self) -> str:
        ...

    @CurrencySymbol.setter
    def CurrencySymbol(self, value: str):
        ...

    @property
    def AveragePrice(self) -> float:
        ...

    @AveragePrice.setter
    def AveragePrice(self, value: float):
        ...

    @property
    def Quantity(self) -> float:
        ...

    @Quantity.setter
    def Quantity(self, value: float):
        ...

    @property
    def MarketPrice(self) -> float:
        ...

    @MarketPrice.setter
    def MarketPrice(self, value: float):
        ...

    @property
    def ConversionRate(self) -> typing.Optional[float]:
        ...

    @ConversionRate.setter
    def ConversionRate(self, value: typing.Optional[float]):
        ...

    @property
    def MarketValue(self) -> float:
        ...

    @MarketValue.setter
    def MarketValue(self, value: float):
        ...

    @property
    def UnrealizedPnL(self) -> float:
        ...

    @UnrealizedPnL.setter
    def UnrealizedPnL(self, value: float):
        ...

    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, security: QuantConnect.Securities.Security) -> None:
        """
        Create a simple JSON holdings from a Security holding class.
        
        :param security: The security instance
        """
        ...

    def Clone(self) -> QuantConnect.Holding:
        """
        Clones this instance
        
        :returns: A new Holding object with the same values as this one
        """
        ...

    def ToString(self) -> str:
        """Writes out the properties of this instance to string"""
        ...


class BrokerageEnvironment(System.Enum):
    """Represents the types of environments supported by brokerages for trading"""

    Live = 0
    """Live trading"""

    Paper = 1
    """Paper trading"""


class Language(System.Enum):
    """Multilanguage support enum: which language is this project for the interop bridge converter."""

    CSharp = 0
    """C# Language Project"""

    FSharp = 1
    """FSharp Project"""

    VisualBasic = 2
    """Visual Basic Project"""

    Java = 3
    """Java Language Project"""

    Python = 4
    """Python Language Project"""


class UserPlan(System.Enum):
    """User / Algorithm Job Subscription Level"""

    Free = 0
    """Free User (Backtesting)."""

    Hobbyist = 1
    """Hobbyist User with Included 512mb Server."""

    Professional = 2
    """Professional plan for financial advisors"""


class ServerType(System.Enum):
    """Live server types available through the web IDE. / QC deployment."""

    Server512 = 0
    """Additional server"""

    Server1024 = 1
    """Upgraded server"""

    Server2048 = 2
    """Server with 2048 MB Ram."""


class AccountType(System.Enum):
    """Account type: margin or cash"""

    Margin = 0
    """Margin account type"""

    Cash = 1
    """Cash account type"""


class MarketDataType(System.Enum):
    """Market data style: is the market data a summary (OHLC style) bar, or is it a time-price value."""

    Base = 0

    TradeBar = 1

    Tick = 2

    Auxiliary = 3

    QuoteBar = 4

    OptionChain = 5

    FuturesChain = 6


class DataFeedEndpoint(System.Enum):
    """Datafeed enum options for selecting the source of the datafeed."""

    Backtesting = 0

    FileSystem = 1

    LiveTrading = 2

    Database = 3


class StoragePermissions(System.Enum):
    """Cloud storage permission options."""

    Public = 0

    Authenticated = 1


class TickType(System.Enum):
    """Types of tick data"""

    Trade = 0

    Quote = 1

    OpenInterest = 2


class DelistingType(System.Enum):
    """Specifies the type of QuantConnect.Data.Market.Delisting data"""

    Warning = 0
    """Specifies a warning of an imminent delisting"""

    Delisted = 1
    """Specifies the symbol has been delisted"""


class SplitType(System.Enum):
    """Specifies the type of QuantConnect.Data.Market.Split data"""

    Warning = 0
    """Specifies a warning of an imminent split event"""

    SplitOccurred = 1
    """Specifies the symbol has been split"""


class Resolution(System.Enum):
    """Resolution of data requested."""

    Tick = 0

    Second = 1

    Minute = 2

    Hour = 3

    Daily = 4


class SettlementType(System.Enum):
    """Specifies the type of settlement in derivative deals"""

    PhysicalDelivery = 0
    """Physical delivery of the underlying security"""

    Cash = 1
    """Cash is paid/received on settlement"""


class AlgorithmStatus(System.Enum):
    """States of a live deployment."""

    DeployError = 0

    InQueue = 1

    Running = 2

    Stopped = 3

    Liquidated = 4

    Deleted = 5

    Completed = 6

    RuntimeError = 7

    Invalid = 8

    LoggingIn = 9

    Initializing = 10

    History = 11


class AlgorithmControl(System.Object):
    """Wrapper for algorithm status enum to include the charting subscription."""

    @property
    def Initialized(self) -> bool:
        """Register this control packet as not defaults."""
        ...

    @Initialized.setter
    def Initialized(self, value: bool):
        """Register this control packet as not defaults."""
        ...

    @property
    def Status(self) -> QuantConnect.AlgorithmStatus:
        """Current run status of the algorithm id."""
        ...

    @Status.setter
    def Status(self, value: QuantConnect.AlgorithmStatus):
        """Current run status of the algorithm id."""
        ...

    @property
    def ChartSubscription(self) -> str:
        """Currently requested chart."""
        ...

    @ChartSubscription.setter
    def ChartSubscription(self, value: str):
        """Currently requested chart."""
        ...

    @property
    def HasSubscribers(self) -> bool:
        """True if there's subscribers on the channel"""
        ...

    @HasSubscribers.setter
    def HasSubscribers(self, value: bool):
        """True if there's subscribers on the channel"""
        ...

    def __init__(self) -> None:
        """Default initializer for algorithm control class."""
        ...


class SubscriptionTransportMedium(System.Enum):
    """Specifies where a subscription's data comes from"""

    LocalFile = 0
    """The subscription's data comes from disk"""

    RemoteFile = 1
    """The subscription's data is downloaded from a remote source"""

    Rest = 2
    """The subscription's data comes from a rest call that is polled and returns a single line/data point of information"""

    Streaming = 3
    """The subscription's data is streamed"""


class Period(System.Enum):
    """enum Period - Enum of all the analysis periods, AS integers. Reference "Period" Array to access the values"""

    TenSeconds = 10

    ThirtySeconds = 30

    OneMinute = 60

    TwoMinutes = 120

    ThreeMinutes = 180

    FiveMinutes = 300

    TenMinutes = 600

    FifteenMinutes = 900

    TwentyMinutes = 1200

    ThirtyMinutes = 1800

    OneHour = 3600

    TwoHours = 7200

    FourHours = 14400

    SixHours = 21600


class DataNormalizationMode(System.Enum):
    """Specifies how data is normalized before being sent into an algorithm"""

    Raw = 0
    """The raw price with dividends added to cash book"""

    Adjusted = 1
    """The adjusted prices with splits and dividends factored in"""

    SplitAdjusted = 2
    """The adjusted prices with only splits factored in, dividends paid out to the cash book"""

    TotalReturn = 3
    """The split adjusted price plus dividends"""


class MarketCodes(System.Object):
    """Global Market Short Codes and their full versions: (used in tick objects)"""

    US: System.Collections.Generic.Dictionary[str, str] = ...

    Canada: System.Collections.Generic.Dictionary[str, str] = ...


class ChannelStatus(System.Object):
    """Defines the different channel status values"""

    Vacated: str = "channel_vacated"
    """The channel is empty"""

    Occupied: str = "channel_occupied"
    """The channel has subscribers"""


class USHoliday(System.Object):
    """US Public Holidays - Not Tradeable:"""

    Dates: System.Collections.Generic.HashSet[datetime.datetime] = ...
    """Public Holidays"""


class AlgorithmSettings(System.Object, QuantConnect.Interfaces.IAlgorithmSettings):
    """This class includes user settings for the algorithm which can be changed in the IAlgorithm.Initialize method"""

    @property
    def RebalancePortfolioOnSecurityChanges(self) -> typing.Optional[bool]:
        """True if should rebalance portfolio on security changes. True by default"""
        ...

    @RebalancePortfolioOnSecurityChanges.setter
    def RebalancePortfolioOnSecurityChanges(self, value: typing.Optional[bool]):
        """True if should rebalance portfolio on security changes. True by default"""
        ...

    @property
    def RebalancePortfolioOnInsightChanges(self) -> typing.Optional[bool]:
        """True if should rebalance portfolio on new insights or expiration of insights. True by default"""
        ...

    @RebalancePortfolioOnInsightChanges.setter
    def RebalancePortfolioOnInsightChanges(self, value: typing.Optional[bool]):
        """True if should rebalance portfolio on new insights or expiration of insights. True by default"""
        ...

    @property
    def MaxAbsolutePortfolioTargetPercentage(self) -> float:
        """The absolute maximum valid total portfolio value target percentage"""
        ...

    @MaxAbsolutePortfolioTargetPercentage.setter
    def MaxAbsolutePortfolioTargetPercentage(self, value: float):
        """The absolute maximum valid total portfolio value target percentage"""
        ...

    @property
    def MinAbsolutePortfolioTargetPercentage(self) -> float:
        """The absolute minimum valid total portfolio value target percentage"""
        ...

    @MinAbsolutePortfolioTargetPercentage.setter
    def MinAbsolutePortfolioTargetPercentage(self, value: float):
        """The absolute minimum valid total portfolio value target percentage"""
        ...

    @property
    def DataSubscriptionLimit(self) -> int:
        """Gets/sets the maximum number of concurrent market data subscriptions available"""
        ...

    @DataSubscriptionLimit.setter
    def DataSubscriptionLimit(self, value: int):
        """Gets/sets the maximum number of concurrent market data subscriptions available"""
        ...

    @property
    def FreePortfolioValue(self) -> float:
        """
        Gets/sets the SetHoldings buffers value.
        The buffer is used for orders not to be rejected due to volatility when using SetHoldings and CalculateOrderQuantity
        """
        ...

    @FreePortfolioValue.setter
    def FreePortfolioValue(self, value: float):
        """
        Gets/sets the SetHoldings buffers value.
        The buffer is used for orders not to be rejected due to volatility when using SetHoldings and CalculateOrderQuantity
        """
        ...

    @property
    def FreePortfolioValuePercentage(self) -> float:
        """
        Gets/sets the SetHoldings buffers value percentage.
        This percentage will be used to set the FreePortfolioValue
        based on the SecurityPortfolioManager.TotalPortfolioValue
        """
        ...

    @FreePortfolioValuePercentage.setter
    def FreePortfolioValuePercentage(self, value: float):
        """
        Gets/sets the SetHoldings buffers value percentage.
        This percentage will be used to set the FreePortfolioValue
        based on the SecurityPortfolioManager.TotalPortfolioValue
        """
        ...

    @property
    def LiquidateEnabled(self) -> bool:
        """Gets/sets if Liquidate() is enabled"""
        ...

    @LiquidateEnabled.setter
    def LiquidateEnabled(self, value: bool):
        """Gets/sets if Liquidate() is enabled"""
        ...

    @property
    def StalePriceTimeSpan(self) -> datetime.timedelta:
        """Gets/sets the minimum time span elapsed to consider a market fill price as stale (defaults to one hour)"""
        ...

    @StalePriceTimeSpan.setter
    def StalePriceTimeSpan(self, value: datetime.timedelta):
        """Gets/sets the minimum time span elapsed to consider a market fill price as stale (defaults to one hour)"""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the AlgorithmSettings class"""
        ...


class IIsolatorLimitResultProvider(metaclass=abc.ABCMeta):
    """
    Provides an abstraction for managing isolator limit results.
    This is originally intended to be used by the training feature to permit a single
    algorithm time loop to extend past the default of ten minutes
    """

    def IsWithinLimit(self) -> QuantConnect.IsolatorLimitResult:
        """Determines whether or not a custom isolator limit has be reached."""
        ...

    def RequestAdditionalTime(self, minutes: int) -> None:
        """
        Requests additional time from the isolator result provider. This is intended
        to prevent IsWithinLimit from returning an error result.
        This method will throw a TimeoutException if there is insufficient
        resources available to fulfill the specified number of minutes.
        
        :param minutes: The number of additional minutes to request
        """
        ...

    def TryRequestAdditionalTime(self, minutes: int) -> bool:
        """
        Attempts to request additional time from the isolator result provider. This is intended
        to prevent IsWithinLimit from returning an error result.
        This method will only return false if there is insufficient resources available to fulfill
        the specified number of minutes.
        
        :param minutes: The number of additional minutes to request
        """
        ...


class ITimeProvider(metaclass=abc.ABCMeta):
    """
    Provides access to the current time in UTC. This doesn't necessarily
    need to be wall-clock time, but rather the current time in some system
    """

    def GetUtcNow(self) -> datetime.datetime:
        """
        Gets the current time in UTC
        
        :returns: The current time in UTC
        """
        ...


class IsolatorLimitResultProvider(System.Object):
    """Provides access to the NullIsolatorLimitResultProvider and extension methods supporting ScheduledEvent"""

    Null: QuantConnect.IIsolatorLimitResultProvider = ...
    """Provides access to a null implementation of IIsolatorLimitResultProvider"""

    @staticmethod
    @typing.overload
    def Consume(isolatorLimitProvider: QuantConnect.IIsolatorLimitResultProvider, scheduledEvent: QuantConnect.Scheduling.ScheduledEvent, scanTimeUtc: datetime.datetime, timeMonitor: QuantConnect.Scheduling.TimeMonitor) -> None:
        """Convenience method for invoking a scheduled event's Scan method inside the IsolatorLimitResultProvider"""
        ...

    @staticmethod
    @typing.overload
    def Consume(isolatorLimitProvider: QuantConnect.IIsolatorLimitResultProvider, timeProvider: QuantConnect.ITimeProvider, code: System.Action, timeMonitor: QuantConnect.Scheduling.TimeMonitor) -> None:
        """
        Executes the provided code block and while the code block is running, continually consume from
        the limit result provided one token each minute. This function allows the code to run for the
        first full minute without requesting additional time from the provider. Following that, every
        minute an additional one minute will be requested from the provider.
        """
        ...


class SeriesSampler(System.Object):
    """A type capable of taking a chart and resampling using a linear interpolation strategy"""

    def __init__(self, resolution: datetime.timedelta) -> None:
        """
        Creates a new SeriesSampler to sample Series data on the specified resolution
        
        :param resolution: The desired sampling resolution
        """
        ...

    def Sample(self, series: QuantConnect.Series, start: datetime.datetime, stop: datetime.datetime) -> QuantConnect.Series:
        """
        Samples the given series
        
        :param series: The series to be sampled
        :param start: The date to start sampling, if before start of data then start of data will be used
        :param stop: The date to stop sampling, if after stop of data, then stop of data will be used
        :returns: The sampled series
        """
        ...

    def SampleCharts(self, charts: System.Collections.Generic.IDictionary[str, QuantConnect.Chart], start: datetime.datetime, stop: datetime.datetime) -> System.Collections.Generic.Dictionary[str, QuantConnect.Chart]:
        """
        Samples the given charts
        
        :param charts: The charts to be sampled
        :param start: The date to start sampling
        :param stop: The date to stop sampling
        :returns: The sampled charts
        """
        ...


class SymbolRepresentation(System.Object):
    """Public static helper class that does parsing/generation of symbol representations (options, futures)"""

    class FutureTickerProperties(System.Object):
        """Class contains future ticker properties returned by ParseFutureTicker()"""

        @property
        def Underlying(self) -> str:
            """Underlying name"""
            ...

        @Underlying.setter
        def Underlying(self, value: str):
            """Underlying name"""
            ...

        @property
        def ExpirationYearShort(self) -> int:
            """Short expiration year"""
            ...

        @ExpirationYearShort.setter
        def ExpirationYearShort(self, value: int):
            """Short expiration year"""
            ...

        @property
        def ExpirationMonth(self) -> int:
            """Expiration month"""
            ...

        @ExpirationMonth.setter
        def ExpirationMonth(self, value: int):
            """Expiration month"""
            ...

        @property
        def ExpirationDay(self) -> int:
            """Expiration day"""
            ...

        @ExpirationDay.setter
        def ExpirationDay(self, value: int):
            """Expiration day"""
            ...

    class OptionTickerProperties(System.Object):
        """Class contains option ticker properties returned by ParseOptionTickerIQFeed()"""

        @property
        def Underlying(self) -> str:
            """Underlying name"""
            ...

        @Underlying.setter
        def Underlying(self, value: str):
            """Underlying name"""
            ...

        @property
        def OptionRight(self) -> QuantConnect.OptionRight:
            """Option right"""
            ...

        @OptionRight.setter
        def OptionRight(self, value: QuantConnect.OptionRight):
            """Option right"""
            ...

        @property
        def OptionStrike(self) -> float:
            """Option strike"""
            ...

        @OptionStrike.setter
        def OptionStrike(self, value: float):
            """Option strike"""
            ...

        @property
        def ExpirationDate(self) -> datetime.datetime:
            """Expiration date"""
            ...

        @ExpirationDate.setter
        def ExpirationDate(self, value: datetime.datetime):
            """Expiration date"""
            ...

    @staticmethod
    def ParseFutureTicker(ticker: str) -> QuantConnect.SymbolRepresentation.FutureTickerProperties:
        """
        Function returns underlying name, expiration year, expiration month, expiration day for the future contract ticker. Function detects if
        the format used is either 1 or 2 digits year, and if day code is present (will default to 1rst day of month). Returns null, if parsing failed.
        Format [Ticker][2 digit day code OPTIONAL][1 char month code][2/1 digit year code]
        
        :returns: Results containing 1) underlying name, 2) short expiration year, 3) expiration month
        """
        ...

    @staticmethod
    def GenerateFutureTicker(underlying: str, expiration: datetime.datetime, doubleDigitsYear: bool = True) -> str:
        """
        Returns future symbol ticker from underlying and expiration date. Function can generate tickers of two formats: one and two digits year.
        Format [Ticker][2 digit day code][1 char month code][2/1 digit year code], more information at http://help.tradestation.com/09_01/tradestationhelp/symbology/futures_symbology.htm
        
        :param underlying: String underlying
        :param expiration: Expiration date
        :param doubleDigitsYear: True if year should represented by two digits; False - one digit
        """
        ...

    @staticmethod
    @typing.overload
    def GenerateOptionTickerOSI(symbol: typing.Union[QuantConnect.Symbol, str]) -> str:
        """
        Returns option symbol ticker in accordance with OSI symbology
        More information can be found at http://www.optionsclearing.com/components/docs/initiatives/symbology/symbology_initiative_v1_8.pdf
        
        :param symbol: Symbol object to create OSI ticker from
        :returns: The OSI ticker representation
        """
        ...

    @staticmethod
    @typing.overload
    def GenerateOptionTickerOSI(underlying: str, right: QuantConnect.OptionRight, strikePrice: float, expiration: datetime.datetime) -> str:
        """
        Returns option symbol ticker in accordance with OSI symbology
        More information can be found at http://www.optionsclearing.com/components/docs/initiatives/symbology/symbology_initiative_v1_8.pdf
        
        :param underlying: Underlying string
        :param right: Option right
        :param strikePrice: Option strike
        :param expiration: Option expiration date
        :returns: The OSI ticker representation
        """
        ...

    @staticmethod
    def ParseOptionTickerOSI(ticker: str) -> QuantConnect.Symbol:
        """
        Parses the specified OSI options ticker into a Symbol object
        
        :param ticker: The OSI compliant option ticker string
        :returns: Symbol object for the specified OSI option ticker string
        """
        ...

    @staticmethod
    def ParseOptionTickerIQFeed(ticker: str) -> QuantConnect.SymbolRepresentation.OptionTickerProperties:
        """
        Function returns option contract parameters (underlying name, expiration date, strike, right) from IQFeed option ticker
        Symbology details: http://www.iqfeed.net/symbolguide/index.cfm?symbolguide=guide&displayaction=support%C2%A7ion=guide&web=iqfeed&guide=options&web=IQFeed&type=stock
        
        :param ticker: IQFeed option ticker
        :returns: Results containing 1) underlying name, 2) option right, 3) option strike 4) expiration date
        """
        ...


class RealTimeSynchronizedTimer(System.Object):
    """Real time timer class for precise callbacks on a millisecond resolution in a self managed thread."""

    @typing.overload
    def __init__(self) -> None:
        """Constructor for Real Time Event Driver:"""
        ...

    @typing.overload
    def __init__(self, period: datetime.timedelta, callback: typing.Callable[[], datetime.datetime]) -> None:
        """
        Trigger an event callback after precisely milliseconds-lapsed.
        This is expensive, it creates a new thread and closely monitors the loop.
        
        :param period: delay period between event callbacks
        :param callback: Callback event passed the UTC time the event is intended to be triggered
        """
        ...

    def Start(self) -> None:
        """Start the synchronized real time timer - fire events at start of each second or minute"""
        ...

    def Scanner(self) -> None:
        """Scan the stopwatch for the desired millisecond delay:"""
        ...

    def Pause(self) -> None:
        """Hang the real time event:"""
        ...

    def Resume(self) -> None:
        """Resume clock"""
        ...

    def Stop(self) -> None:
        """Stop the real time timer:"""
        ...


class TimeUpdatedEventArgs(System.EventArgs):
    """Event arguments class for the LocalTimeKeeper.TimeUpdated event"""

    @property
    def Time(self) -> datetime.datetime:
        """Gets the new time"""
        ...

    @property
    def TimeZone(self) -> typing.Any:
        """Gets the time zone"""
        ...

    def __init__(self, time: datetime.datetime, timeZone: typing.Any) -> None:
        """
        Initializes a new instance of the TimeUpdatedEventArgs class
        
        :param time: The newly updated time
        :param timeZone: The time zone of the new time
        """
        ...


class Field(System.Object):
    """Provides static properties to be used as selectors with the indicator system"""

    Open: typing.Callable[[QuantConnect.Data.IBaseData], float]
    """Gets a selector that selects the Open value"""

    High: typing.Callable[[QuantConnect.Data.IBaseData], float]
    """Gets a selector that selects the High value"""

    Low: typing.Callable[[QuantConnect.Data.IBaseData], float]
    """Gets a selector that selects the Low value"""

    Close: typing.Callable[[QuantConnect.Data.IBaseData], float]
    """Gets a selector that selects the Close value"""

    Average: typing.Callable[[QuantConnect.Data.IBaseData], float]
    """Defines an average price that is equal to (O + H + L + C) / 4"""

    Median: typing.Callable[[QuantConnect.Data.IBaseData], float]
    """Defines an average price that is equal to (H + L) / 2"""

    Typical: typing.Callable[[QuantConnect.Data.IBaseData], float]
    """Defines an average price that is equal to (H + L + C) / 3"""

    Weighted: typing.Callable[[QuantConnect.Data.IBaseData], float]
    """Defines an average price that is equal to (H + L + 2*C) / 4"""

    SevenBar: typing.Callable[[QuantConnect.Data.IBaseData], float]
    """Defines an average price that is equal to (2*O + H + L + 3*C)/7"""

    Volume: typing.Callable[[QuantConnect.Data.IBaseData], float]
    """Gets a selector that selectors the Volume value"""


class Market(System.Object):
    """Markets Collection: Soon to be expanded to a collection of items specifying the market hour, timezones and country codes."""

    USA: str = "usa"
    """USA Market"""

    Oanda: str = "oanda"
    """Oanda Market"""

    FXCM: str = "fxcm"
    """FXCM Market Hours"""

    Dukascopy: str = "dukascopy"
    """Dukascopy Market"""

    Bitfinex: str = "bitfinex"
    """Bitfinex market"""

    Globex: str = "cmeglobex"

    NYMEX: str = "nymex"
    """NYMEX"""

    CBOT: str = "cbot"
    """CBOT"""

    ICE: str = "ice"
    """ICE"""

    CBOE: str = "cboe"
    """CBOE"""

    NSE: str = "nse"
    """NSE"""

    COMEX: str = "comex"
    """Comex"""

    CME: str = "cme"
    """CME"""

    SGX: str = "sgx"
    """Singapore Exchange"""

    HKFE: str = "hkfe"
    """Hong Kong Exchange"""

    GDAX: str = "gdax"
    """GDAX"""

    Kraken: str = "kraken"
    """Kraken"""

    Bitstamp: str = "bitstamp"
    """Bitstamp"""

    OkCoin: str = "okcoin"
    """OkCoin"""

    Bithumb: str = "bithumb"
    """Bithumb"""

    Binance: str = "binance"
    """Binance"""

    Poloniex: str = "poloniex"
    """Poloniex"""

    Coinone: str = "coinone"
    """Coinone"""

    HitBTC: str = "hitbtc"
    """HitBTC"""

    Bittrex: str = "bittrex"
    """Bittrex"""

    @staticmethod
    def Add(market: str, identifier: int) -> None:
        """
        Adds the specified market to the map of available markets with the specified identifier.
        
        :param market: The market string to add
        :param identifier: The identifier for the market, this value must be positive and less than 1000
        """
        ...

    @staticmethod
    def Encode(market: str) -> typing.Optional[int]:
        """
        Gets the market code for the specified market. Returns null if the market is not found
        
        :param market: The market to check for (case sensitive)
        :returns: The internal code used for the market. Corresponds to the value used when calling Add
        """
        ...

    @staticmethod
    def Decode(code: int) -> str:
        """
        Gets the market string for the specified market code.
        
        :param code: The market code to be decoded
        :returns: The string representation of the market, or null if not found
        """
        ...


class TradingCalendar(System.Object):
    """Class represents trading calendar, populated with variety of events relevant to currently trading instruments"""

    def __init__(self, securityManager: QuantConnect.Securities.SecurityManager, marketHoursDatabase: QuantConnect.Securities.MarketHoursDatabase) -> None:
        ...

    @typing.overload
    def GetTradingDay(self) -> QuantConnect.TradingDay:
        """
        Method returns TradingDay that contains trading events associated with today's date
        
        :returns: Populated instance of TradingDay
        """
        ...

    @typing.overload
    def GetTradingDay(self, day: datetime.datetime) -> QuantConnect.TradingDay:
        """
        Method returns TradingDay that contains trading events associated with the given date
        
        :returns: Populated instance of TradingDay
        """
        ...

    def GetTradingDays(self, start: datetime.datetime, end: datetime.datetime) -> System.Collections.Generic.IEnumerable[QuantConnect.TradingDay]:
        """
        Method returns TradingDay that contains trading events associated with the range of dates
        
        :param start: Start date of the range (inclusive)
        :param end: End date of the range (inclusive)
        :returns: >Populated list of TradingDay
        """
        ...

    def GetDaysByType(self, type: QuantConnect.TradingDayType, start: datetime.datetime, end: datetime.datetime) -> System.Collections.Generic.IEnumerable[QuantConnect.TradingDay]:
        """
        Method returns TradingDay of the specified type (TradingDayType) that contains trading events associated with the range of dates
        
        :param type: Type of the events
        :param start: Start date of the range (inclusive)
        :param end: End date of the range (inclusive)
        :returns: >Populated list of TradingDay
        """
        ...


class DataProviderEventArgs(System.EventArgs, metaclass=abc.ABCMeta):
    """Defines a base class for IDataProviderEvents"""

    @property
    def Symbol(self) -> QuantConnect.Symbol:
        """Gets the symbol being processed that generated the event"""
        ...

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> None:
        """
        Initializes a new instance of the DataProviderEventArgs class
        
        This method is protected.
        
        :param symbol: Symbol being processed that generated the event
        """
        ...


class InvalidConfigurationDetectedEventArgs(QuantConnect.DataProviderEventArgs):
    """Event arguments for the IDataProviderEvents.InvalidConfigurationDetected event"""

    @property
    def Message(self) -> str:
        """Gets the error message"""
        ...

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], message: str) -> None:
        """
        Initializes a new instance of the InvalidConfigurationDetectedEventArgs class
        
        :param symbol: Symbol being processed that generated the event
        :param message: The error message
        """
        ...


class NumericalPrecisionLimitedEventArgs(QuantConnect.DataProviderEventArgs):
    """Event arguments for the IDataProviderEvents.NumericalPrecisionLimited event"""

    @property
    def Message(self) -> str:
        """Gets the error message"""
        ...

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], message: str) -> None:
        """
        Initializes a new instance of the NumericalPrecisionLimitedEventArgs class
        
        :param symbol: Symbol being processed that generated the event
        :param message: The error message
        """
        ...


class DownloadFailedEventArgs(QuantConnect.DataProviderEventArgs):
    """Event arguments for the IDataProviderEvents.DownloadFailed event"""

    @property
    def Message(self) -> str:
        """Gets the error message"""
        ...

    @property
    def StackTrace(self) -> str:
        """Gets the error stack trace"""
        ...

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], message: str, stackTrace: str = ...) -> None:
        """
        Initializes a new instance of the DownloadFailedEventArgs class
        
        :param symbol: Symbol being processed that generated the event
        :param message: The error message
        :param stackTrace: The error stack trace
        """
        ...


class ReaderErrorDetectedEventArgs(QuantConnect.DataProviderEventArgs):
    """Event arguments for the IDataProviderEvents.ReaderErrorDetected event"""

    @property
    def Message(self) -> str:
        """Gets the error message"""
        ...

    @property
    def StackTrace(self) -> str:
        """Gets the error stack trace"""
        ...

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], message: str, stackTrace: str = ...) -> None:
        """
        Initializes a new instance of the ReaderErrorDetectedEventArgs class
        
        :param symbol: Symbol being processed that generated the event
        :param message: The error message
        :param stackTrace: The error stack trace
        """
        ...


class StartDateLimitedEventArgs(QuantConnect.DataProviderEventArgs):
    """Event arguments for the IDataProviderEvents.StartDateLimited event"""

    @property
    def Message(self) -> str:
        """Gets the error message"""
        ...

    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], message: str) -> None:
        """
        Initializes a new instance of the StartDateLimitedEventArgs class
        
        :param symbol: Symbol being processed that generated the event
        :param message: The error message
        """
        ...


class NewTradableDateEventArgs(QuantConnect.DataProviderEventArgs):
    """Event arguments for the NewTradableDate event"""

    @property
    def Date(self) -> datetime.datetime:
        """The new tradable date"""
        ...

    @property
    def LastBaseData(self) -> QuantConnect.Data.BaseData:
        """
        The last BaseData of the Security
        for which we are enumerating
        """
        ...

    @property
    def LastRawPrice(self) -> typing.Optional[float]:
        """The last raw security price we have"""
        ...

    def __init__(self, date: datetime.datetime, lastBaseData: QuantConnect.Data.BaseData, symbol: typing.Union[QuantConnect.Symbol, str], lastRawPrice: typing.Optional[float]) -> None:
        """
        Initializes a new instance of the NewTradableDateEventArgs class
        
        :param date: The new tradable date
        :param lastBaseData: The last BaseData of the Security for which we are enumerating
        :param symbol: The Symbol of the new tradable date
        :param lastRawPrice: The last raw security price we have
        """
        ...


class TimeZones(System.Object):
    """Provides access to common time zones"""

    Utc: typing.Any = ...
    """Gets the Universal Coordinated time zone."""

    NewYork: typing.Any = ...
    """Gets the time zone for New York City, USA. This is a daylight savings time zone."""

    EasternStandard: typing.Any = ...
    """Get the Eastern Standard Time (EST) WITHOUT daylight savings, this is a constant -5 hour offset"""

    London: typing.Any = ...
    """Gets the time zone for London, England. This is a daylight savings time zone."""

    HongKong: typing.Any = ...
    """Gets the time zone for Hong Kong, China."""

    Tokyo: typing.Any = ...
    """Gets the time zone for Tokyo, Japan."""

    Rome: typing.Any = ...
    """Gets the time zone for Rome, Italy. This is a daylight savings time zone."""

    Sydney: typing.Any = ...
    """Gets the time zone for Sydney, Australia. This is a daylight savings time zone."""

    Vancouver: typing.Any = ...
    """Gets the time zone for Vancouver, Canada."""

    Toronto: typing.Any = ...
    """Gets the time zone for Toronto, Canada. This is a daylight savings time zone."""

    Chicago: typing.Any = ...
    """Gets the time zone for Chicago, USA. This is a daylight savings time zone."""

    LosAngeles: typing.Any = ...
    """Gets the time zone for Los Angeles, USA. This is a daylight savings time zone."""

    Phoenix: typing.Any = ...
    """Gets the time zone for Phoenix, USA. This is a daylight savings time zone."""

    Auckland: typing.Any = ...
    """Gets the time zone for Auckland, New Zealand. This is a daylight savings time zone."""

    Moscow: typing.Any = ...
    """Gets the time zone for Moscow, Russia."""

    Madrid: typing.Any = ...
    """Gets the time zone for Madrid, Span. This is a daylight savings time zone."""

    BuenosAires: typing.Any = ...
    """Gets the time zone for Buenos Aires, Argentia."""

    Brisbane: typing.Any = ...
    """Gets the time zone for Brisbane, Australia."""

    SaoPaulo: typing.Any = ...
    """Gets the time zone for Sao Paulo, Brazil. This is a daylight savings time zone."""

    Cairo: typing.Any = ...
    """Gets the time zone for Cairo, Egypt."""

    Johannesburg: typing.Any = ...
    """Gets the time zone for Johannesburg, South Africa."""

    Anchorage: typing.Any = ...
    """Gets the time zone for Anchorage, USA. This is a daylight savings time zone."""

    Denver: typing.Any = ...
    """Gets the time zone for Denver, USA. This is a daylight savings time zone."""

    Detroit: typing.Any = ...
    """Gets the time zone for Detroit, USA. This is a daylight savings time zone."""

    MexicoCity: typing.Any = ...
    """Gets the time zone for Mexico City, Mexico. This is a daylight savings time zone."""

    Jerusalem: typing.Any = ...
    """Gets the time zone for Jerusalem, Israel. This is a daylight savings time zone."""

    Shanghai: typing.Any = ...
    """Gets the time zone for Shanghai, China."""

    Melbourne: typing.Any = ...
    """Gets the time zone for Melbourne, Australia. This is a daylight savings time zone."""

    Amsterdam: typing.Any = ...
    """Gets the time zone for Amsterdam, Netherlands. This is a daylight savings time zone."""

    Athens: typing.Any = ...
    """Gets the time zone for Athens, Greece. This is a daylight savings time zone."""

    Berlin: typing.Any = ...
    """Gets the time zone for Berlin, Germany. This is a daylight savings time zone."""

    Bucharest: typing.Any = ...
    """Gets the time zone for Bucharest, Romania. This is a daylight savings time zone."""

    Dublin: typing.Any = ...
    """Gets the time zone for Dublin, Ireland. This is a daylight savings time zone."""

    Helsinki: typing.Any = ...
    """Gets the time zone for Helsinki, Finland. This is a daylight savings time zone."""

    Istanbul: typing.Any = ...
    """Gets the time zone for Istanbul, Turkey. This is a daylight savings time zone."""

    Minsk: typing.Any = ...
    """Gets the time zone for Minsk, Belarus."""

    Paris: typing.Any = ...
    """Gets the time zone for Paris, France. This is a daylight savings time zone."""

    Zurich: typing.Any = ...
    """Gets the time zone for Zurich, Switzerland. This is a daylight savings time zone."""

    Honolulu: typing.Any = ...
    """Gets the time zone for Honolulu, USA. This is a daylight savings time zone."""


class TimeKeeper(System.Object, QuantConnect.Interfaces.ITimeKeeper):
    """Provides a means of centralizing time for various time zones."""

    @property
    def UtcTime(self) -> datetime.datetime:
        """Gets the current time in UTC"""
        ...

    @typing.overload
    def __init__(self, utcDateTime: datetime.datetime, *timeZones: DateTimeZone) -> None:
        """
        Initializes a new instance of the TimeKeeper class at the specified
        UTC time and for the specified time zones. Each time zone specified will cause the
        creation of a LocalTimeKeeper to handle conversions for that time zone.
        
        :param utcDateTime: The initial time
        :param timeZones: The time zones used to instantiate LocalTimeKeeper instances.
        """
        ...

    @typing.overload
    def __init__(self, utcDateTime: datetime.datetime, timeZones: System.Collections.Generic.IEnumerable[DateTimeZone]) -> None:
        """
        Initializes a new instance of the TimeKeeper class at the specified
        UTC time and for the specified time zones. Each time zone specified will cause the
        creation of a LocalTimeKeeper to handle conversions for that time zone.
        
        :param utcDateTime: The initial time
        :param timeZones: The time zones used to instantiate LocalTimeKeeper instances.
        """
        ...

    def SetUtcDateTime(self, utcDateTime: datetime.datetime) -> None:
        """
        Sets the current UTC time for this time keeper and the attached child LocalTimeKeeper instances.
        
        :param utcDateTime: The current time in UTC
        """
        ...

    def GetTimeIn(self, timeZone: typing.Any) -> datetime.datetime:
        """
        Gets the local time in the specified time zone. If the specified DateTimeZone
        has not already been added, this will throw a KeyNotFoundException.
        
        :param timeZone: The time zone to get local time for
        :returns: The local time in the specifed time zone
        """
        ...

    def GetLocalTimeKeeper(self, timeZone: typing.Any) -> QuantConnect.LocalTimeKeeper:
        """
        Gets the LocalTimeKeeper instance for the specified time zone
        
        :param timeZone: The time zone whose LocalTimeKeeper we seek
        :returns: The LocalTimeKeeper instance for the specified time zone
        """
        ...

    def AddTimeZone(self, timeZone: typing.Any) -> None:
        """Adds the specified time zone to this time keeper"""
        ...


class Extensions(System.Object):
    """Extensions function collections - group all static extensions functions here."""

    @staticmethod
    def GetMemoryStream(guid: System.Guid) -> System.IO.MemoryStream:
        """Will return a memory stream using the RecyclableMemoryStreamManager instance."""
        ...

    @staticmethod
    def RentId() -> System.Guid:
        """
        Gets a unique id. Should be returned using ReturnId
        
        :returns: A unused Guid
        """
        ...

    @staticmethod
    def ReturnId(guid: System.Guid) -> None:
        """
        Returns a rented unique id RentId
        
        :param guid: The guid to return
        """
        ...

    @staticmethod
    @typing.overload
    def ProtobufSerialize(ticks: System.Collections.Generic.List[QuantConnect.Data.Market.Tick]) -> typing.List[int]:
        """
        Serialize a list of ticks using protobuf
        
        :param ticks: The list of ticks to serialize
        :returns: The resulting byte array
        """
        ...

    @staticmethod
    @typing.overload
    def ProtobufSerialize(baseData: QuantConnect.Data.IBaseData) -> typing.List[int]:
        """
        Serialize a base data instance using protobuf
        
        :param baseData: The data point to serialize
        :returns: The resulting byte array
        """
        ...

    @staticmethod
    def GetZeroPriceMessage(symbol: typing.Union[QuantConnect.Symbol, str]) -> str:
        """Extension method to get security price is 0 messages for users"""
        ...

    @staticmethod
    def ToCamelCase(value: str) -> str:
        """Converts the provided string into camel case notation"""
        ...

    @staticmethod
    def Batch(resultPackets: System.Collections.Generic.List[QuantConnect.Packets.AlphaResultPacket]) -> QuantConnect.Packets.AlphaResultPacket:
        """
        Helper method to batch a collection of AlphaResultPacket into 1 single instance.
        Will return null if the provided list is empty. Will keep the last Order instance per order id,
        which is the latest. Implementations trusts the provided 'resultPackets' list to batch is in order
        """
        ...

    @staticmethod
    def StopSafely(thread: System.Threading.Thread, timeout: datetime.timedelta, token: System.Threading.CancellationTokenSource = None) -> None:
        """
        Helper method to safely stop a running thread
        
        :param thread: The thread to stop
        :param timeout: The timeout to wait till the thread ends after which abort will be called
        :param token: Cancellation token source to use if any
        """
        ...

    @staticmethod
    def GetHash(orders: System.Collections.Generic.IDictionary[int, QuantConnect.Orders.Order]) -> int:
        """
        Generates a hash code from a given collection of orders
        
        :param orders: The order collection
        :returns: The hash value
        """
        ...

    @staticmethod
    def ToFunc(dateRule: QuantConnect.Scheduling.IDateRule) -> typing.Callable[[datetime.datetime], typing.Optional[datetime.datetime]]:
        """
        Converts a date rule into a function that receives current time
        and returns the next date.
        
        :param dateRule: The date rule to convert
        :returns: A function that will enumerate the provided date rules
        """
        ...

    @staticmethod
    @typing.overload
    def IsEmpty(series: QuantConnect.Series) -> bool:
        """Returns true if the specified Series instance holds no ChartPoint"""
        ...

    @staticmethod
    @typing.overload
    def IsEmpty(chart: QuantConnect.Chart) -> bool:
        """
        Returns if the specified Chart instance  holds no Series
        or they are all empty IsEmpty(Series)
        """
        ...

    @staticmethod
    def GetPythonMethod(instance: typing.Any, name: str) -> typing.Any:
        """
        Gets a python method by name
        
        :param instance: The object instance to search the method in
        :param name: The name of the method
        :returns: The python method or null if not defined or CSharp implemented
        """
        ...

    @staticmethod
    def OrderTargetsByMarginImpact(targets: System.Collections.Generic.IEnumerable[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget], algorithm: QuantConnect.Interfaces.IAlgorithm, targetIsDelta: bool = False) -> System.Collections.Generic.IEnumerable[QuantConnect.Algorithm.Framework.Portfolio.IPortfolioTarget]:
        """
        Returns an ordered enumerable where position reducing orders are executed first
        and the remaining orders are executed in decreasing order value.
        Will NOT return targets for securities that have no data yet.
        Will NOT return targets for which current holdings + open orders quantity, sum up to the target quantity
        
        :param targets: The portfolio targets to order by margin
        :param algorithm: The algorithm instance
        :param targetIsDelta: True if the target quantity is the delta between the desired and existing quantity
        """
        ...

    @staticmethod
    def GetBaseDataInstance(type: System.Type) -> QuantConnect.Data.BaseData:
        """
        Given a type will create a new instance using the parameterless constructor
        and assert the type implements BaseData
        """
        ...

    @staticmethod
    def GetAndDispose(instance: typing.Any) -> QuantConnect_Extensions_T:
        """
        Helper method that will cast the provided PyObject
        to a T type and dispose of it.
        
        :param instance: The PyObject instance to cast and dispose
        :returns: The instance of type T. Will return default value if provided instance is null
        """
        ...

    @staticmethod
    def Move(list: System.Collections.Generic.List[QuantConnect_Extensions_T], oldIndex: int, newIndex: int) -> None:
        """
        Extension to move one element from list from A to position B.
        
        :param list: List we're operating on.
        :param oldIndex: Index of variable we want to move.
        :param newIndex: New location for the variable
        """
        ...

    @staticmethod
    def GetBytes(str: str) -> typing.List[int]:
        """
        Extension method to convert a string into a byte array
        
        :param str: String to convert to bytes.
        :returns: Byte array
        """
        ...

    @staticmethod
    def Clear(queue: System.Collections.Concurrent.ConcurrentQueue[QuantConnect_Extensions_T]) -> None:
        """
        Extentsion method to clear all items from a thread safe queue
        
        :param queue: queue object
        """
        ...

    @staticmethod
    def GetString(bytes: typing.List[int], encoding: System.Text.Encoding = None) -> str:
        """
        Extension method to convert a byte array into a string.
        
        :param bytes: Byte array to convert.
        :param encoding: The encoding to use for the conversion. Defaults to Encoding.ASCII
        :returns: String from bytes.
        """
        ...

    @staticmethod
    def ToMD5(str: str) -> str:
        """
        Extension method to convert a string to a MD5 hash.
        
        :param str: String we want to MD5 encode.
        :returns: MD5 hash of a string
        """
        ...

    @staticmethod
    def ToSHA256(data: str) -> str:
        """
        Encrypt the token:time data to make our API hash.
        
        :param data: Data to be hashed by SHA256
        :returns: Hashed string.
        """
        ...

    @staticmethod
    def LazyToUpper(data: str) -> str:
        """
        Lazy string to upper implementation.
        Will first verify the string is not already upper and avoid
        the call to string.ToUpperInvariant() if possible.
        
        :param data: The string to upper
        :returns: The upper string
        """
        ...

    @staticmethod
    @typing.overload
    def AddOrUpdate(dictionary: System.Collections.Concurrent.ConcurrentDictionary[QuantConnect_Extensions_K, QuantConnect_Extensions_V], key: QuantConnect_Extensions_K, value: QuantConnect_Extensions_V) -> None:
        """
        Extension method to automatically set the update value to same as "add" value for TryAddUpdate.
        This makes the API similar for traditional and concurrent dictionaries.
        
        :param dictionary: Dictionary object we're operating on
        :param key: Key we want to add or update.
        :param value: Value we want to set.
        """
        ...

    @staticmethod
    @typing.overload
    def AddOrUpdate(dictionary: System.Collections.Concurrent.ConcurrentDictionary[QuantConnect_Extensions_TKey, System.Lazy[QuantConnect_Extensions_TValue]], key: QuantConnect_Extensions_TKey, addValueFactory: typing.Callable[[QuantConnect_Extensions_TKey], QuantConnect_Extensions_TValue], updateValueFactory: typing.Callable[[QuantConnect_Extensions_TKey, QuantConnect_Extensions_TValue], QuantConnect_Extensions_TValue]) -> QuantConnect_Extensions_TValue:
        """
        Extension method to automatically add/update lazy values in concurrent dictionary.
        
        :param dictionary: Dictionary object we're operating on
        :param key: Key we want to add or update.
        :param addValueFactory: The function used to generate a value for an absent key
        :param updateValueFactory: The function used to generate a new value for an existing key based on the key's existing value
        """
        ...

    @staticmethod
    @typing.overload
    def Add(dictionary: System.Collections.Generic.IDictionary[QuantConnect_Extensions_TKey, QuantConnect_Extensions_TCollection], key: QuantConnect_Extensions_TKey, element: QuantConnect_Extensions_TElement) -> None:
        """
        Adds the specified element to the collection with the specified key. If an entry does not exist for the
        specified key then one will be created.
        
        :param dictionary: The source dictionary to be added to
        :param key: The key
        :param element: The element to be added
        """
        ...

    @staticmethod
    @typing.overload
    def Add(dictionary: QuantConnect.Data.Market.Ticks, key: typing.Union[QuantConnect.Symbol, str], tick: QuantConnect.Data.Market.Tick) -> None:
        """
        Adds the specified Tick to the Ticks collection. If an entry does not exist for the specified key then one will be created.
        
        :param dictionary: The ticks dictionary
        :param key: The symbol
        :param tick: The tick to add
        """
        ...

    @staticmethod
    @typing.overload
    def RoundToSignificantDigits(d: float, digits: int) -> float:
        """
        Extension method to round a double value to a fixed number of significant figures instead of a fixed decimal places.
        
        :param d: Double we're rounding
        :param digits: Number of significant figures
        :returns: New double rounded to digits-significant figures
        """
        ...

    @staticmethod
    @typing.overload
    def RoundToSignificantDigits(d: float, digits: int) -> float:
        """
        Extension method to round a double value to a fixed number of significant figures instead of a fixed decimal places.
        
        :param d: Double we're rounding
        :param digits: Number of significant figures
        :returns: New double rounded to digits-significant figures
        """
        ...

    @staticmethod
    def TruncateTo3DecimalPlaces(value: float) -> float:
        """
        Will truncate the provided decimal, without rounding, to 3 decimal places
        
        :param value: The value to truncate
        :returns: New instance with just 3 decimal places
        """
        ...

    @staticmethod
    def SmartRounding(input: float) -> float:
        """
        Provides global smart rounding, numbers larger than 1000 will round to 4 decimal places,
        while numbers smaller will round to 7 significant digits
        """
        ...

    @staticmethod
    def SafeDecimalCast(input: float) -> float:
        """
        Casts the specified input value to a decimal while acknowledging the overflow conditions
        
        :param input: The value to be cast
        :returns: The input value as a decimal, if the value is too large or to small to be represented as a decimal, then the closest decimal value will be returned
        """
        ...

    @staticmethod
    @typing.overload
    def Normalize(input: float) -> float:
        """
        Will remove any trailing zeros for the provided decimal input
        
        :param input: The decimal to remove trailing zeros from
        :returns: Provided input with no trailing zeros
        """
        ...

    @staticmethod
    def NormalizeToStr(input: float) -> str:
        """
        Will remove any trailing zeros for the provided decimal and convert to string.
        Uses Normalize.
        
        :param input: The decimal to convert to string
        :returns: Input converted to string with no trailing zeros
        """
        ...

    @staticmethod
    def ToDecimal(str: str) -> float:
        """
        Extension method for faster string to decimal conversion.
        
        :param str: String to be converted to positive decimal value
        :returns: Decimal value of the string
        """
        ...

    @staticmethod
    def ToDecimalAllowExponent(str: str) -> float:
        """
        Extension method for string to decimal conversion where string can represent a number with exponent xe-y
        
        :param str: String to be converted to decimal value
        :returns: Decimal value of the string
        """
        ...

    @staticmethod
    def ToInt32(str: str) -> int:
        """
        Extension method for faster string to Int32 conversion.
        
        :param str: String to be converted to positive Int32 value
        :returns: Int32 value of the string
        """
        ...

    @staticmethod
    def ToInt64(str: str) -> int:
        """
        Extension method for faster string to Int64 conversion.
        
        :param str: String to be converted to positive Int64 value
        :returns: Int32 value of the string
        """
        ...

    @staticmethod
    def ToCsv(str: str, size: int = 4) -> System.Collections.Generic.List[str]:
        """
        Breaks the specified string into csv components, all commas are considered separators
        
        :param str: The string to be broken into csv
        :param size: The expected size of the output list
        :returns: A list of the csv pieces
        """
        ...

    @staticmethod
    def ToCsvData(str: str, size: int = 4, delimiter: str = ...) -> System.Collections.Generic.List[str]:
        """
        Breaks the specified string into csv components, works correctly with commas in data fields
        
        :param str: The string to be broken into csv
        :param size: The expected size of the output list
        :param delimiter: The delimiter used to separate entries in the line
        :returns: A list of the csv pieces
        """
        ...

    @staticmethod
    def IsNaNOrZero(value: float) -> bool:
        """
        Check if a number is NaN or equal to zero
        
        :param value: The double value to check
        """
        ...

    @staticmethod
    def GetDecimalEpsilon() -> float:
        """
        Gets the smallest positive number that can be added to a decimal instance and return
        a new value that does not == the old value
        """
        ...

    @staticmethod
    def GetExtension(str: str) -> str:
        """
        Extension method to extract the extension part of this file name if it matches a safe list, or return a ".custom" extension for ones which do not match.
        
        :param str: String we're looking for the extension for.
        :returns: Last 4 character string of string.
        """
        ...

    @staticmethod
    def ToStream(str: str) -> System.IO.Stream:
        """
        Extension method to convert strings to stream to be read.
        
        :param str: String to convert to stream
        :returns: Stream instance
        """
        ...

    @staticmethod
    @typing.overload
    def Round(time: datetime.timedelta, roundingInterval: datetime.timedelta, roundingType: System.MidpointRounding) -> datetime.timedelta:
        """
        Extension method to round a timeSpan to nearest timespan period.
        
        :param time: TimeSpan To Round
        :param roundingInterval: Rounding Unit
        :param roundingType: Rounding method
        :returns: Rounded timespan
        """
        ...

    @staticmethod
    @typing.overload
    def Round(time: datetime.timedelta, roundingInterval: datetime.timedelta) -> datetime.timedelta:
        """
        Extension method to round timespan to nearest timespan period.
        
        :param time: Base timespan we're looking to round.
        :param roundingInterval: Timespan period we're rounding.
        :returns: Rounded timespan period
        """
        ...

    @staticmethod
    def RoundDown(dateTime: datetime.datetime, interval: datetime.timedelta) -> datetime.datetime:
        """
        Extension method to round a datetime down by a timespan interval.
        
        :param dateTime: Base DateTime object we're rounding down.
        :param interval: Timespan interval to round to
        :returns: Rounded datetime
        """
        ...

    @staticmethod
    def RoundDownInTimeZone(dateTime: datetime.datetime, roundingInterval: datetime.timedelta, sourceTimeZone: typing.Any, roundingTimeZone: typing.Any) -> datetime.datetime:
        """
        Rounds the specified date time in the specified time zone. Careful with calling this method in a loop while modifying dateTime, check unit tests.
        
        :param dateTime: Date time to be rounded
        :param roundingInterval: Timespan rounding period
        :param sourceTimeZone: Time zone of the date time
        :param roundingTimeZone: Time zone in which the rounding is performed
        :returns: The rounded date time in the source time zone
        """
        ...

    @staticmethod
    def ExchangeRoundDown(dateTime: datetime.datetime, interval: datetime.timedelta, exchangeHours: QuantConnect.Securities.SecurityExchangeHours, extendedMarket: bool) -> datetime.datetime:
        """
        Extension method to round a datetime down by a timespan interval until it's
        within the specified exchange's open hours. This works by first rounding down
        the specified time using the interval, then producing a bar between that
        rounded time and the interval plus the rounded time and incrementally walking
        backwards until the exchange is open
        
        :param dateTime: Time to be rounded down
        :param interval: Timespan interval to round to.
        :param exchangeHours: The exchange hours to determine open times
        :param extendedMarket: True for extended market hours, otherwise false
        :returns: Rounded datetime
        """
        ...

    @staticmethod
    def ExchangeRoundDownInTimeZone(dateTime: datetime.datetime, interval: datetime.timedelta, exchangeHours: QuantConnect.Securities.SecurityExchangeHours, roundingTimeZone: typing.Any, extendedMarket: bool) -> datetime.datetime:
        """
        Extension method to round a datetime down by a timespan interval until it's
        within the specified exchange's open hours. The rounding is performed in the
        specified time zone
        
        :param dateTime: Time to be rounded down
        :param interval: Timespan interval to round to.
        :param exchangeHours: The exchange hours to determine open times
        :param roundingTimeZone: The time zone to perform the rounding in
        :param extendedMarket: True for extended market hours, otherwise false
        :returns: Rounded datetime
        """
        ...

    @staticmethod
    @typing.overload
    def Round(datetime: datetime.datetime, roundingInterval: datetime.timedelta) -> datetime.datetime:
        """
        Extension method to round a datetime to the nearest unit timespan.
        
        :param datetime: Datetime object we're rounding.
        :param roundingInterval: Timespan rounding period.
        :returns: Rounded datetime
        """
        ...

    @staticmethod
    def RoundUp(time: datetime.datetime, interval: datetime.timedelta) -> datetime.datetime:
        """
        Extension method to explicitly round up to the nearest timespan interval.
        
        :param time: Base datetime object to round up.
        :param interval: Timespan interval to round to
        :returns: Rounded datetime
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertTo(time: datetime.datetime, _from: typing.Any, to: typing.Any, strict: bool = False) -> datetime.datetime:
        """
        Converts the specified time from the  time zone to the  time zone
        
        :param time: The time to be converted in terms of the  time zone
        :param _from: The time zone the specified  is in
        :param to: The time zone to be converted to
        :param strict: True for strict conversion, this will throw during ambiguitities, false for lenient conversion
        :returns: The time in terms of the to time zone
        """
        ...

    @staticmethod
    def ConvertFromUtc(time: datetime.datetime, to: typing.Any, strict: bool = False) -> datetime.datetime:
        """
        Converts the specified time from UTC to the  time zone
        
        :param time: The time to be converted expressed in UTC
        :param to: The destinatio time zone
        :param strict: True for strict conversion, this will throw during ambiguitities, false for lenient conversion
        :returns: The time in terms of the  time zone
        """
        ...

    @staticmethod
    def ConvertToUtc(time: datetime.datetime, _from: typing.Any, strict: bool = False) -> datetime.datetime:
        """
        Converts the specified time from the  time zone to TimeZones.Utc
        
        :param time: The time to be converted in terms of the  time zone
        :param _from: The time zone the specified  is in
        :param strict: True for strict conversion, this will throw during ambiguitities, false for lenient conversion
        :returns: The time in terms of the to time zone
        """
        ...

    @staticmethod
    def IsCommonBusinessDay(date: datetime.datetime) -> bool:
        """
        Business day here is defined as any day of the week that is not saturday or sunday
        
        :param date: The date to be examined
        :returns: A bool indicating wether the datetime is a weekday or not
        """
        ...

    @staticmethod
    def Reset(timer: typing.Any) -> None:
        """
        Add the reset method to the System.Timer class.
        
        :param timer: System.timer object
        """
        ...

    @staticmethod
    def MatchesTypeName(type: System.Type, typeName: str) -> bool:
        """
        Function used to match a type against a string type name. This function compares on the AssemblyQualfiedName,
        the FullName, and then just the Name of the type.
        
        :param type: The type to test for a match
        :param typeName: The name of the type to match
        :returns: True if the specified type matches the type name, false otherwise
        """
        ...

    @staticmethod
    def IsSubclassOfGeneric(type: System.Type, possibleSuperType: System.Type) -> bool:
        """
        Checks the specified type to see if it is a subclass of the . This method will
        crawl up the inheritance heirarchy to check for equality using generic type definitions (if exists)
        
        :param type: The type to be checked as a subclass of
        :param possibleSuperType: The possible superclass of
        :returns: True if  is a subclass of the generic type definition
        """
        ...

    @staticmethod
    def GetBetterTypeName(type: System.Type) -> str:
        """
        Gets a type's name with the generic parameters filled in the way they would look when
        defined in code, such as converting Dictionary<`1,`2> to Dictionary<string,int>
        
        :param type: The type who's name we seek
        :returns: A better type name
        """
        ...

    @staticmethod
    def ToTimeSpan(resolution: QuantConnect.Resolution) -> datetime.timedelta:
        """
        Converts the Resolution instance into a TimeSpan instance
        
        :param resolution: The resolution to be converted
        :returns: A TimeSpan instance that represents the resolution specified
        """
        ...

    @staticmethod
    def ToHigherResolutionEquivalent(timeSpan: datetime.timedelta, requireExactMatch: bool) -> QuantConnect.Resolution:
        """
        Converts the specified time span into a resolution enum value. If an exact match
        is not found and `requireExactMatch` is false, then the higher resoluion will be
        returned. For example, timeSpan=5min will return Minute resolution.
        
        :param timeSpan: The time span to convert to resolution
        :param requireExactMatch: True to throw an exception if an exact match is not found
        :returns: The resolution
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertTo(value: str) -> QuantConnect_Extensions_T:
        """
        Converts the specified string value into the specified type
        
        :param value: The string value to be converted
        :returns: The converted value
        """
        ...

    @staticmethod
    @typing.overload
    def ConvertTo(value: str, type: System.Type) -> System.Object:
        """
        Converts the specified string value into the specified type
        
        :param value: The string value to be converted
        :param type: The output type
        :returns: The converted value
        """
        ...

    @staticmethod
    @typing.overload
    def WaitOne(waitHandle: System.Threading.WaitHandle, cancellationToken: System.Threading.CancellationToken) -> bool:
        """
        Blocks the current thread until the current System.Threading.WaitHandle receives a signal, while observing a System.Threading.CancellationToken.
        
        :param waitHandle: The wait handle to wait on
        :param cancellationToken: The System.Threading.CancellationToken to observe.
        """
        ...

    @staticmethod
    @typing.overload
    def WaitOne(waitHandle: System.Threading.WaitHandle, timeout: datetime.timedelta, cancellationToken: System.Threading.CancellationToken) -> bool:
        """
        Blocks the current thread until the current System.Threading.WaitHandle is set, using a System.TimeSpan to measure the time interval, while observing a System.Threading.CancellationToken.
        
        :param waitHandle: The wait handle to wait on
        :param timeout: A System.TimeSpan that represents the number of milliseconds to wait, or a System.TimeSpan that represents -1 milliseconds to wait indefinitely.
        :param cancellationToken: The System.Threading.CancellationToken to observe.
        :returns: true if the System.Threading.WaitHandle was set; otherwise, false.
        """
        ...

    @staticmethod
    @typing.overload
    def WaitOne(waitHandle: System.Threading.WaitHandle, millisecondsTimeout: int, cancellationToken: System.Threading.CancellationToken) -> bool:
        """
        Blocks the current thread until the current System.Threading.WaitHandle is set, using a 32-bit signed integer to measure the time interval, while observing a System.Threading.CancellationToken.
        
        :param waitHandle: The wait handle to wait on
        :param millisecondsTimeout: The number of milliseconds to wait, or System.Threading.Timeout.Infinite(-1) to wait indefinitely.
        :param cancellationToken: The System.Threading.CancellationToken to observe.
        :returns: true if the System.Threading.WaitHandle was set; otherwise, false.
        """
        ...

    @staticmethod
    def GetMD5Hash(stream: System.IO.Stream) -> typing.List[int]:
        """
        Gets the MD5 hash from a stream
        
        :param stream: The stream to compute a hash for
        :returns: The MD5 hash
        """
        ...

    @staticmethod
    def WithEmbeddedHtmlAnchors(source: str) -> str:
        """
        Convert a string into the same string with a URL! :)
        
        :param source: The source string to be converted
        :returns: The same source string but with anchor tags around substrings matching a link regex
        """
        ...

    @staticmethod
    def GetStringBetweenChars(value: str, left: str, right: str) -> str:
        """
        Get the first occurence of a string between two characters from another string
        
        :param value: The original string
        :param left: Left bound of the substring
        :param right: Right bound of the substring
        :returns: Substring from original string bounded by the two characters
        """
        ...

    @staticmethod
    def SingleOrAlgorithmTypeName(names: System.Collections.Generic.List[str], algorithmTypeName: str) -> str:
        """
        Return the first in the series of names, or find the one that matches the configured algirithmTypeName
        
        :param names: The list of class names
        :param algorithmTypeName: The configured algorithm type name from the config
        :returns: The name of the class being run
        """
        ...

    @staticmethod
    def ToLower(_enum: System.Enum) -> str:
        """
        Converts the specified  value to its corresponding lower-case string representation
        
        :returns: A lower-case string representation of the specified enumeration value
        """
        ...

    @staticmethod
    def IsValid(securityType: QuantConnect.SecurityType) -> bool:
        """
        Asserts the specified  value is valid
        
        :param securityType: The SecurityType value
        :returns: True if valid security type value
        """
        ...

    @staticmethod
    def ToStringPerformance(optionRight: QuantConnect.OptionRight) -> str:
        """
        Converts the specified  value to its corresponding string representation
        
        :param optionRight: The optionRight value
        :returns: A string representation of the specified OptionRight value
        """
        ...

    @staticmethod
    def SecurityTypeToLower(securityType: QuantConnect.SecurityType) -> str:
        """
        Converts the specified  value to its corresponding lower-case string representation
        
        :param securityType: The SecurityType value
        :returns: A lower-case string representation of the specified SecurityType value
        """
        ...

    @staticmethod
    def TickTypeToLower(tickType: QuantConnect.TickType) -> str:
        """
        Converts the specified  value to its corresponding lower-case string representation
        
        :param tickType: The tickType value
        :returns: A lower-case string representation of the specified tickType value
        """
        ...

    @staticmethod
    def ResolutionToLower(resolution: QuantConnect.Resolution) -> str:
        """
        Converts the specified  value to its corresponding lower-case string representation
        
        :param resolution: The resolution value
        :returns: A lower-case string representation of the specified resolution value
        """
        ...

    @staticmethod
    def ToOrderTicket(order: QuantConnect.Orders.Order, transactionManager: QuantConnect.Securities.SecurityTransactionManager) -> QuantConnect.Orders.OrderTicket:
        """
        Turn order into an order ticket
        
        :param order: The Order being converted
        :param transactionManager: The transaction manager, SecurityTransactionManager
        """
        ...

    @staticmethod
    def ProcessUntilEmpty(collection: System.Collections.Concurrent.IProducerConsumerCollection[QuantConnect_Extensions_T], handler: typing.Callable[[], QuantConnect_Extensions_T]) -> None:
        ...

    @staticmethod
    def ToSafeString(pyObject: typing.Any) -> str:
        """
        Returns a string that represents the current PyObject
        
        :param pyObject: The PyObject being converted
        :returns: string that represents the current PyObject
        """
        ...

    @staticmethod
    def TryConvert(pyObject: typing.Any, result: QuantConnect_Extensions_T, allowPythonDerivative: bool = False) -> bool:
        """
        Tries to convert a PyObject into a managed object
        
        :param pyObject: PyObject to be converted
        :param result: Managed object
        :param allowPythonDerivative: True will convert python subclasses of T
        :returns: True if successful conversion
        """
        ...

    @staticmethod
    def TryConvertToDelegate(pyObject: typing.Any, result: QuantConnect_Extensions_T) -> bool:
        """
        Tries to convert a PyObject into a managed object
        
        :param pyObject: PyObject to be converted
        :param result: Managed object
        :returns: True if successful conversion
        """
        ...

    @staticmethod
    def ConvertToUniverseSelectionSymbolDelegate(selector: typing.Callable[[QuantConnect_Extensions_T], System.Object]) -> typing.Callable[[QuantConnect_Extensions_T], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]]:
        """
        Wraps the provided universe selection selector checking if it returned Universe.Unchanged
        and returns it instead, else enumerates result as IEnumerable{Symbol}
        """
        ...

    @staticmethod
    def ConvertToUniverseSelectionStringDelegate(selector: typing.Callable[[QuantConnect_Extensions_T], System.Object]) -> typing.Callable[[QuantConnect_Extensions_T], System.Collections.Generic.IEnumerable[str]]:
        """
        Wraps the provided universe selection selector checking if it returned Universe.Unchanged
        and returns it instead, else enumerates result as IEnumerable{String}
        """
        ...

    @staticmethod
    def ConvertToDelegate(pyObject: typing.Any) -> QuantConnect_Extensions_T:
        """
        Convert a PyObject into a managed object
        
        :param pyObject: PyObject to be converted
        :returns: Instance of type T
        """
        ...

    @staticmethod
    def ConvertToDictionary(pyObject: typing.Any) -> System.Collections.Generic.Dictionary[QuantConnect_Extensions_TKey, QuantConnect_Extensions_TValue]:
        """
        Convert a PyObject into a managed dictionary
        
        :param pyObject: PyObject to be converted
        :returns: Dictionary of TValue keyed by TKey
        """
        ...

    @staticmethod
    def ConvertToSymbolEnumerable(pyObject: typing.Any) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Gets Enumerable of Symbol from a PyObject
        
        :param pyObject: PyObject containing Symbol or Array of Symbol
        :returns: Enumerable of Symbol
        """
        ...

    @staticmethod
    def ToPyList(enumerable: System.Collections.IEnumerable) -> typing.List[typing.Any]:
        """
        Converts an IEnumerable to a PyList
        
        :param enumerable: IEnumerable object to convert
        :returns: PyList
        """
        ...

    @staticmethod
    def GetEnumString(value: int, pyObject: typing.Any) -> str:
        """
        Converts the numeric value of one or more enumerated constants to an equivalent enumerated string.
        
        :param value: Numeric value
        :param pyObject: Python object that encapsulated a Enum Type
        :returns: String that represents the enumerated object
        """
        ...

    @staticmethod
    def CreateType(pyObject: typing.Any) -> System.Type:
        """
        Creates a type with a given name, if PyObject is not a CLR type. Otherwise, convert it.
        
        :param pyObject: Python object representing a type.
        :returns: Type object
        """
        ...

    @staticmethod
    def BatchBy(enumerable: System.Collections.Generic.IEnumerable[QuantConnect_Extensions_T], batchSize: int) -> System.Collections.Generic.IEnumerable[System.Collections.Generic.List[QuantConnect_Extensions_T]]:
        """
        Performs on-line batching of the specified enumerator, emitting chunks of the requested batch size
        
        :param enumerable: The enumerable to be batched
        :param batchSize: The number of items per batch
        :returns: An enumerable of lists
        """
        ...

    @staticmethod
    def SynchronouslyAwaitTaskResult(task: System.Threading.Tasks.Task[QuantConnect_Extensions_TResult]) -> QuantConnect_Extensions_TResult:
        """
        Safely blocks until the specified task has completed executing
        
        :param task: The task to be awaited
        :returns: The result of the task
        """
        ...

    @staticmethod
    def SynchronouslyAwaitTask(task: System.Threading.Tasks.Task) -> None:
        """
        Safely blocks until the specified task has completed executing
        
        :param task: The task to be awaited
        :returns: The result of the task
        """
        ...

    @staticmethod
    def ToQueryString(pairs: System.Collections.Generic.IDictionary[str, System.Object]) -> str:
        """Convert dictionary to query string"""
        ...

    @staticmethod
    def RemoveFromEnd(s: str, ending: str) -> str:
        """
        Returns a new string in which specified ending in the current instance is removed.
        
        :param s: original string value
        :param ending: the string to be removed
        """
        ...

    @staticmethod
    def GetNormalizedPrice(config: QuantConnect.Data.SubscriptionDataConfig, price: float) -> float:
        """Normalizes the specified price based on the DataNormalizationMode"""
        ...

    @staticmethod
    def Scale(data: QuantConnect.Data.BaseData, factor: typing.Callable[[float], float]) -> QuantConnect.Data.BaseData:
        """Scale data based on factor function"""
        ...

    @staticmethod
    @typing.overload
    def Normalize(data: QuantConnect.Data.BaseData, config: QuantConnect.Data.SubscriptionDataConfig) -> QuantConnect.Data.BaseData:
        """
        Normalize prices based on configuration
        
        :param data: Data to be normalized
        :param config: Price scale
        """
        ...

    @staticmethod
    def Adjust(data: QuantConnect.Data.BaseData, scale: float) -> QuantConnect.Data.BaseData:
        """
        Adjust prices based on price scale
        
        :param data: Data to be adjusted
        :param scale: Price scale
        """
        ...

    @staticmethod
    def ToHexString(source: typing.List[int]) -> str:
        """
        Returns a hex string of the byte array.
        
        :param source: the byte array to be represented as string
        :returns: A new string containing the items in the enumerable
        """
        ...

    @staticmethod
    def GetExerciseDirection(right: QuantConnect.OptionRight, isShort: bool) -> QuantConnect.Orders.OrderDirection:
        """
        Gets the option exercise order direction resulting from the specified  and
        whether or not we wrote the option ( is true) or bought to
        option ( is false)
        
        :param right: The option right
        :param isShort: True if we wrote the option, false if we purchased the option
        :returns: The order direction resulting from an exercised option
        """
        ...

    @staticmethod
    def GetOrderDirection(quantity: float) -> QuantConnect.Orders.OrderDirection:
        """Gets the OrderDirection for the specified"""
        ...

    @staticmethod
    def CreateOptionChain(algorithm: QuantConnect.Interfaces.IAlgorithm, symbol: typing.Union[QuantConnect.Symbol, str], filter: typing.Callable[[QuantConnect.Securities.OptionFilterUniverse], QuantConnect.Securities.OptionFilterUniverse], universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings = None) -> QuantConnect.Data.UniverseSelection.OptionChainUniverse:
        """
        Creates a OptionChainUniverse for a given symbol
        
        :param algorithm: The algorithm instance to create universes for
        :param symbol: Symbol of the option
        :param filter: The option filter to use
        :param universeSettings: The universe settings, will use algorithm settings if null
        :returns: OptionChainUniverse for the given symbol
        """
        ...


class RealTimeProvider(System.Object, QuantConnect.ITimeProvider):
    """
    Provides an implementation of ITimeProvider that
    uses DateTime.UtcNow to provide the current time
    """

    Instance: QuantConnect.ITimeProvider = ...
    """Provides a static instance of the RealTimeProvider"""

    def GetUtcNow(self) -> datetime.datetime:
        """
        Gets the current time in UTC
        
        :returns: The current time in UTC
        """
        ...


class Globals(System.Object):
    """Provides application level constant values"""

    DataFolder: str
    """The root directory of the data folder for this application"""

    Cache: str = "./cache/data"
    """The directory used for storing downloaded remote files"""

    Version: str
    """The version of lean"""

    CacheDataFolder: str
    """Data path to cache folder location"""

    @staticmethod
    def Reset() -> None:
        """Resets global values with the Config data."""
        ...


class Expiry(System.Object):
    """Provides static functions that can be used to compute a future DateTime (expiry) given a DateTime."""

    OneMonth: typing.Callable[[datetime.datetime], datetime.datetime]
    """Computes a date/time one month after a given date/time (nth day to nth day)"""

    OneQuarter: typing.Callable[[datetime.datetime], datetime.datetime]
    """Computes a date/time one quarter after a given date/time (nth day to nth day)"""

    OneYear: typing.Callable[[datetime.datetime], datetime.datetime]
    """Computes a date/time one year after a given date/time (nth day to nth day)"""

    EndOfDay: typing.Callable[[datetime.datetime], datetime.datetime]
    """Computes the end of day (mid-night of the next day) of given date/time"""

    EndOfWeek: typing.Callable[[datetime.datetime], datetime.datetime]
    """Computes the end of week (next Monday) of given date/time"""

    EndOfMonth: typing.Callable[[datetime.datetime], datetime.datetime]
    """Computes the end of month (1st of the next month) of given date/time"""

    EndOfQuarter: typing.Callable[[datetime.datetime], datetime.datetime]
    """Computes the end of quarter (1st of the starting month of next quarter) of given date/time"""

    EndOfYear: typing.Callable[[datetime.datetime], datetime.datetime]
    """Computes the end of year (1st of the next year) of given date/time"""


class Currencies(System.Object):
    """Provides commonly used currency pairs and symbols"""

    USD: str = "USD"
    """USD currency string"""

    EUR: str = "EUR"
    """EUR currency string"""

    GBP: str = "GBP"
    """GBP currency string"""

    NullCurrency: str = "QCC"
    """Null currency used when a real one is not required"""

    CurrencySymbols: System.Collections.Generic.IReadOnlyDictionary[str, str] = ...
    """A mapping of currency codes to their display symbols"""

    @staticmethod
    def GetCurrencySymbol(currency: str) -> str:
        """
        Gets the currency symbol for the specified currency code
        
        :param currency: The currency code
        :returns: The currency symbol
        """
        ...


class Time(System.Object):
    """Time helper class collection for working with trading dates"""

    class DateTimeWithZone:
        """Live charting is sensitive to timezone so need to convert the local system time to a UTC and display in browser as UTC."""

        @property
        def UniversalTime(self) -> datetime.datetime:
            """Gets the universal time."""
            ...

        @property
        def TimeZone(self) -> System.TimeZoneInfo:
            """Gets the time zone."""
            ...

        @property
        def LocalTime(self) -> datetime.datetime:
            """Gets the local time."""
            ...

        def __init__(self, dateTime: datetime.datetime, timeZone: System.TimeZoneInfo) -> None:
            """
            Initializes a new instance of the QuantConnect.Time.DateTimeWithZone struct.
            
            :param dateTime: Date time.
            :param timeZone: Time zone.
            """
            ...

    EndOfTime: datetime.datetime = ...
    """Provides a value far enough in the future the current computer hardware will have decayed :)"""

    EndOfTimeTimeSpan: datetime.timedelta = ...
    """Provides a time span based on EndOfTime"""

    BeginningOfTime: datetime.datetime = ...
    """Provides a value far enough in the past that can be used as a lower bound on dates"""

    MaxTimeSpan: datetime.timedelta = ...
    """
    Provides a value large enough that we won't hit the limit, while small enough
    we can still do math against it without checking everywhere for TimeSpan.MaxValue
    """

    OneYear: datetime.timedelta = ...
    """One Year TimeSpan Period Constant"""

    OneDay: datetime.timedelta = ...
    """One Day TimeSpan Period Constant"""

    OneHour: datetime.timedelta = ...
    """One Hour TimeSpan Period Constant"""

    OneMinute: datetime.timedelta = ...
    """One Minute TimeSpan Period Constant"""

    OneSecond: datetime.timedelta = ...
    """One Second TimeSpan Period Constant"""

    OneMillisecond: datetime.timedelta = ...
    """One Millisecond TimeSpan Period Constant"""

    @staticmethod
    def UnixTimeStampToDateTime(unixTimeStamp: float) -> datetime.datetime:
        """
        Create a C# DateTime from a UnixTimestamp
        
        :param unixTimeStamp: Double unix timestamp (Time since Midnight Jan 1 1970)
        :returns: C# date timeobject
        """
        ...

    @staticmethod
    def UnixMillisecondTimeStampToDateTime(unixTimeStamp: float) -> datetime.datetime:
        """
        Create a C# DateTime from a UnixTimestamp
        
        :param unixTimeStamp: Double unix timestamp (Time since Midnight Jan 1 1970) in milliseconds
        :returns: C# date timeobject
        """
        ...

    @staticmethod
    def UnixNanosecondTimeStampToDateTime(unixTimeStamp: int) -> datetime.datetime:
        """
        Create a C# DateTime from a UnixTimestamp
        
        :param unixTimeStamp: Int64 unix timestamp (Time since Midnight Jan 1 1970) in nanoseconds
        :returns: C# date timeobject
        """
        ...

    @staticmethod
    def DateTimeToUnixTimeStamp(time: datetime.datetime) -> float:
        """
        Convert a Datetime to Unix Timestamp
        
        :param time: C# datetime object
        :returns: Double unix timestamp
        """
        ...

    @staticmethod
    def DateTimeToUnixTimeStampMilliseconds(time: datetime.datetime) -> float:
        """
        Convert a Datetime to Unix Timestamp
        
        :param time: C# datetime object
        :returns: Double unix timestamp
        """
        ...

    @staticmethod
    def DateTimeToUnixTimeStampNanoseconds(time: datetime.datetime) -> int:
        """
        Convert a Datetime to Unix Timestamp
        
        :param time: C# datetime object
        :returns: Int64 unix timestamp
        """
        ...

    @staticmethod
    def TimeStamp() -> float:
        """
        Get the current time as a unix timestamp
        
        :returns: Double value of the unix as UTC timestamp
        """
        ...

    @staticmethod
    @typing.overload
    def Max(one: datetime.timedelta, two: datetime.timedelta) -> datetime.timedelta:
        """Returns the timespan with the larger value"""
        ...

    @staticmethod
    @typing.overload
    def Min(one: datetime.timedelta, two: datetime.timedelta) -> datetime.timedelta:
        """Returns the timespan with the smaller value"""
        ...

    @staticmethod
    @typing.overload
    def Max(one: datetime.datetime, two: datetime.datetime) -> datetime.datetime:
        """Returns the larger of two date times"""
        ...

    @staticmethod
    @typing.overload
    def Min(one: datetime.datetime, two: datetime.datetime) -> datetime.datetime:
        """Returns the smaller of two date times"""
        ...

    @staticmethod
    def Multiply(interval: datetime.timedelta, multiplier: float) -> datetime.timedelta:
        """
        Multiplies the specified interval by the multiplier
        
        :param interval: The interval to be multiplied, such as TimeSpan.FromSeconds(1)
        :param multiplier: The number of times to multiply the interval
        :returns: The multiplied interval, such as 1s*5 = 5s
        """
        ...

    @staticmethod
    def ParseDate(dateToParse: str) -> datetime.datetime:
        """
        Parse a standard YY MM DD date into a DateTime. Attempt common date formats
        
        :param dateToParse: String date time to parse
        :returns: Date time
        """
        ...

    @staticmethod
    def EachDay(_from: datetime.datetime, thru: datetime.datetime) -> System.Collections.Generic.IEnumerable[datetime.datetime]:
        """
        Define an enumerable date range and return each date as a datetime object in the date range
        
        :param _from: DateTime start date
        :param thru: DateTime end date
        :returns: Enumerable date range
        """
        ...

    @staticmethod
    @typing.overload
    def EachTradeableDay(securities: System.Collections.Generic.ICollection[QuantConnect.Securities.Security], _from: datetime.datetime, thru: datetime.datetime) -> System.Collections.Generic.IEnumerable[datetime.datetime]:
        """
        Define an enumerable date range of tradeable dates - skip the holidays and weekends when securities in this algorithm don't trade.
        
        :param securities: Securities we have in portfolio
        :param _from: Start date
        :param thru: End date
        :returns: Enumerable date range
        """
        ...

    @staticmethod
    @typing.overload
    def EachTradeableDay(security: QuantConnect.Securities.Security, _from: datetime.datetime, thru: datetime.datetime) -> System.Collections.Generic.IEnumerable[datetime.datetime]:
        """
        Define an enumerable date range of tradeable dates - skip the holidays and weekends when securities in this algorithm don't trade.
        
        :param security: The security to get tradeable dates for
        :param _from: Start date
        :param thru: End date
        :returns: Enumerable date range
        """
        ...

    @staticmethod
    @typing.overload
    def EachTradeableDay(exchange: QuantConnect.Securities.SecurityExchangeHours, _from: datetime.datetime, thru: datetime.datetime) -> System.Collections.Generic.IEnumerable[datetime.datetime]:
        """
        Define an enumerable date range of tradeable dates - skip the holidays and weekends when securities in this algorithm don't trade.
        
        :param exchange: The security to get tradeable dates for
        :param _from: Start date
        :param thru: End date
        :returns: Enumerable date range
        """
        ...

    @staticmethod
    def EachTradeableDayInTimeZone(exchange: QuantConnect.Securities.SecurityExchangeHours, _from: datetime.datetime, thru: datetime.datetime, timeZone: typing.Any, includeExtendedMarketHours: bool = True) -> System.Collections.Generic.IEnumerable[datetime.datetime]:
        """
        Define an enumerable date range of tradeable dates but expressed in a different time zone.
        
        :param exchange: The exchange hours
        :param _from: The start time in the exchange time zone
        :param thru: The end time in the exchange time zone (inclusive of the final day)
        :param timeZone: The timezone to project the dates into (inclusive of the final day)
        :param includeExtendedMarketHours: True to include extended market hours trading in the search, false otherwise
        """
        ...

    @staticmethod
    def TradableDate(securities: System.Collections.Generic.IEnumerable[QuantConnect.Securities.Security], day: datetime.datetime) -> bool:
        """
        Make sure this date is not a holiday, or weekend for the securities in this algorithm.
        
        :param securities: Security manager from the algorithm
        :param day: DateTime to check if trade-able.
        :returns: True if tradeable date
        """
        ...

    @staticmethod
    def TradeableDates(securities: System.Collections.Generic.ICollection[QuantConnect.Securities.Security], start: datetime.datetime, finish: datetime.datetime) -> int:
        """
        Could of the number of tradeable dates within this period.
        
        :param securities: Securities we're trading
        :param start: Start of Date Loop
        :param finish: End of Date Loop
        :returns: Number of dates
        """
        ...

    @staticmethod
    def GetStartTimeForTradeBars(exchangeHours: QuantConnect.Securities.SecurityExchangeHours, end: datetime.datetime, barSize: datetime.timedelta, barCount: int, extendedMarketHours: bool, dataTimeZone: typing.Any) -> datetime.datetime:
        """
        Determines the start time required to produce the requested number of bars and the given size
        
        :param exchangeHours: The exchange hours used to test for market open hours
        :param end: The end time of the last bar over the requested period
        :param barSize: The length of each bar
        :param barCount: The number of bars requested
        :param extendedMarketHours: True to allow extended market hours bars, otherwise false for only normal market hours
        :returns: The start time that would provide the specified number of bars ending at the specified end time, rounded down by the requested bar size
        """
        ...

    @staticmethod
    def GetEndTimeForTradeBars(exchangeHours: QuantConnect.Securities.SecurityExchangeHours, start: datetime.datetime, barSize: datetime.timedelta, barCount: int, extendedMarketHours: bool) -> datetime.datetime:
        """
        Determines the end time at which the requested number of bars of the given  will have elapsed.
        NOTE: The start time is not discretized by barSize units like is done in GetStartTimeForTradeBars
        
        :param exchangeHours: The exchange hours used to test for market open hours
        :param start: The end time of the last bar over the requested period
        :param barSize: The length of each bar
        :param barCount: The number of bars requested
        :param extendedMarketHours: True to allow extended market hours bars, otherwise false for only normal market hours
        :returns: The start time that would provide the specified number of bars ending at the specified end time, rounded down by the requested bar size
        """
        ...

    @staticmethod
    def GetNumberOfTradeBarsInInterval(exchangeHours: QuantConnect.Securities.SecurityExchangeHours, start: datetime.datetime, end: datetime.datetime, barSize: datetime.timedelta) -> int:
        """
        Gets the number of trade bars of the specified  that fit between the  and
        
        :param exchangeHours: The exchange used to test for market open hours
        :param start: The start time of the interval in the exchange time zone
        :param end: The end time of the interval in the exchange time zone
        :param barSize: The step size used to count number of bars between start and end
        :returns: The number of bars of the specified size between start and end times
        """
        ...

    @staticmethod
    def NormalizeInstantWithinRange(start: datetime.datetime, current: datetime.datetime, period: datetime.timedelta) -> float:
        """
        Normalizes the current time within the specified period
        time = start => 0
        time = start + period => 1
        
        :param start: The start time of the range
        :param current: The current time we seek to normalize
        :param period: The time span of the range
        :returns: The normalized time
        """
        ...

    @staticmethod
    def NormalizeTimeStep(period: datetime.timedelta, stepSize: datetime.timedelta) -> float:
        """
        Normalizes the step size as a percentage of the period.
        
        :param period: The period to normalize against
        :param stepSize: The step size to be normaized
        :returns: The normalized step size as a percentage of the period
        """
        ...

    @staticmethod
    def Abs(timeSpan: datetime.timedelta) -> datetime.timedelta:
        """
        Gets the absolute value of the specified time span
        
        :param timeSpan: Time span whose absolute value we seek
        :returns: The absolute value of the specified time span
        """
        ...


class SymbolValueJsonConverter(JsonConverter):
    """
    Defines a JsonConverter to be used when you only want to serialize
    the Symbol.Value property instead of the full Symbol
    instance
    """

    def WriteJson(self, writer: typing.Any, value: System.Object, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object.
        
        :param writer: The Newtonsoft.Json.JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
        """
        ...

    def ReadJson(self, reader: typing.Any, objectType: System.Type, existingValue: System.Object, serializer: typing.Any) -> System.Object:
        """
        Reads the JSON representation of the object.
        
        :param reader: The Newtonsoft.Json.JsonReader to read from.
        :param objectType: Type of the object.
        :param existingValue: The existing value of object being read.
        :param serializer: The calling serializer.
        :returns: The object value.
        """
        ...

    def CanConvert(self, objectType: System.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param objectType: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...


