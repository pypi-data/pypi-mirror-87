import typing

import System
import System.Collections.Generic
import System.Collections.Immutable
import System.Linq

System_Linq_ImmutableArrayExtensions_T = typing.TypeVar("System_Linq_ImmutableArrayExtensions_T")
System_Linq_ImmutableArrayExtensions_TAccumulate = typing.TypeVar("System_Linq_ImmutableArrayExtensions_TAccumulate")
System_Linq_ImmutableArrayExtensions_TResult = typing.TypeVar("System_Linq_ImmutableArrayExtensions_TResult")
System_Linq_ImmutableArrayExtensions_TSource = typing.TypeVar("System_Linq_ImmutableArrayExtensions_TSource")
System_Linq_ImmutableArrayExtensions_TCollection = typing.TypeVar("System_Linq_ImmutableArrayExtensions_TCollection")
System_Linq_ImmutableArrayExtensions_TBase = typing.TypeVar("System_Linq_ImmutableArrayExtensions_TBase")
System_Linq_ImmutableArrayExtensions_TDerived = typing.TypeVar("System_Linq_ImmutableArrayExtensions_TDerived")
System_Linq_ImmutableArrayExtensions_TKey = typing.TypeVar("System_Linq_ImmutableArrayExtensions_TKey")
System_Linq_ImmutableArrayExtensions_TElement = typing.TypeVar("System_Linq_ImmutableArrayExtensions_TElement")


class ImmutableArrayExtensions(System.Object):
    """LINQ extension method overrides that offer greater efficiency for ImmutableArray{T} than the standard LINQ methods"""

    @staticmethod
    def Select(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], selector: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], System_Linq_ImmutableArrayExtensions_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_TResult]:
        ...

    @staticmethod
    def SelectMany(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_TSource], collectionSelector: typing.Callable[[System_Linq_ImmutableArrayExtensions_TSource], System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_TCollection]], resultSelector: typing.Callable[[System_Linq_ImmutableArrayExtensions_TSource, System_Linq_ImmutableArrayExtensions_TCollection], System_Linq_ImmutableArrayExtensions_TResult]) -> System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_TResult]:
        """
        Projects each element of a sequence to an IEnumerable{T},
        flattens the resulting sequences into one sequence, and invokes a result
        selector function on each element therein.
        
        :param immutableArray: The immutable array.
        :param collectionSelector: A transform function to apply to each element of the input sequence.
        :param resultSelector: A transform function to apply to each element of the intermediate sequence.
        :returns: An IEnumerable{T} whose elements are the result of invoking the one-to-many transform function  on each element of  and then mapping each of those sequence elements and their corresponding source element to a result element.
        """
        ...

    @staticmethod
    def Where(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], bool]) -> System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_T]:
        """Filters a sequence of values based on a predicate."""
        ...

    @staticmethod
    @typing.overload
    def Any(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T]) -> bool:
        """Gets a value indicating whether any elements are in this collection."""
        ...

    @staticmethod
    @typing.overload
    def Any(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], bool]) -> bool:
        """
        Gets a value indicating whether any elements are in this collection
        that match a given condition.
        
        :param predicate: The predicate.
        """
        ...

    @staticmethod
    def All(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], bool]) -> bool:
        """
        Gets a value indicating whether all elements in this collection
        match a given condition.
        
        :param predicate: The predicate.
        :returns: true if every element of the source sequence passes the test in the specified predicate, or if the sequence is empty; otherwise, false.
        """
        ...

    @staticmethod
    @typing.overload
    def SequenceEqual(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_TBase], items: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_TDerived], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_TBase] = None) -> bool:
        """Determines whether two sequences are equal according to an equality comparer."""
        ...

    @staticmethod
    @typing.overload
    def SequenceEqual(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_TBase], items: System.Collections.Generic.IEnumerable[System_Linq_ImmutableArrayExtensions_TDerived], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_TBase] = None) -> bool:
        """Determines whether two sequences are equal according to an equality comparer."""
        ...

    @staticmethod
    @typing.overload
    def SequenceEqual(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_TBase], items: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_TDerived], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_TBase, System_Linq_ImmutableArrayExtensions_TBase], bool]) -> bool:
        """Determines whether two sequences are equal according to an equality comparer."""
        ...

    @staticmethod
    @typing.overload
    def Aggregate(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], func: typing.Callable[[System_Linq_ImmutableArrayExtensions_T, System_Linq_ImmutableArrayExtensions_T], System_Linq_ImmutableArrayExtensions_T]) -> System_Linq_ImmutableArrayExtensions_T:
        """Applies an accumulator function over a sequence."""
        ...

    @staticmethod
    @typing.overload
    def Aggregate(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], seed: System_Linq_ImmutableArrayExtensions_TAccumulate, func: typing.Callable[[System_Linq_ImmutableArrayExtensions_TAccumulate, System_Linq_ImmutableArrayExtensions_T], System_Linq_ImmutableArrayExtensions_TAccumulate]) -> System_Linq_ImmutableArrayExtensions_TAccumulate:
        """Applies an accumulator function over a sequence."""
        ...

    @staticmethod
    @typing.overload
    def Aggregate(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], seed: System_Linq_ImmutableArrayExtensions_TAccumulate, func: typing.Callable[[System_Linq_ImmutableArrayExtensions_TAccumulate, System_Linq_ImmutableArrayExtensions_T], System_Linq_ImmutableArrayExtensions_TAccumulate], resultSelector: typing.Callable[[System_Linq_ImmutableArrayExtensions_TAccumulate], System_Linq_ImmutableArrayExtensions_TResult]) -> System_Linq_ImmutableArrayExtensions_TResult:
        """Applies an accumulator function over a sequence."""
        ...

    @staticmethod
    def ElementAt(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], index: int) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the element at a specified index in a sequence."""
        ...

    @staticmethod
    def ElementAtOrDefault(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], index: int) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the element at a specified index in a sequence or a default value if the index is out of range."""
        ...

    @staticmethod
    @typing.overload
    def First(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], bool]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the first element in a sequence that satisfies a specified condition."""
        ...

    @staticmethod
    @typing.overload
    def First(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the first element in a sequence that satisfies a specified condition."""
        ...

    @staticmethod
    @typing.overload
    def FirstOrDefault(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the first element of a sequence, or a default value if the sequence contains no elements."""
        ...

    @staticmethod
    @typing.overload
    def FirstOrDefault(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], bool]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the first element of the sequence that satisfies a condition or a default value if no such element is found."""
        ...

    @staticmethod
    @typing.overload
    def Last(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the last element of a sequence."""
        ...

    @staticmethod
    @typing.overload
    def Last(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], bool]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the last element of a sequence that satisfies a specified condition."""
        ...

    @staticmethod
    @typing.overload
    def LastOrDefault(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the last element of a sequence, or a default value if the sequence contains no elements."""
        ...

    @staticmethod
    @typing.overload
    def LastOrDefault(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], bool]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the last element of a sequence that satisfies a condition or a default value if no such element is found."""
        ...

    @staticmethod
    @typing.overload
    def Single(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the only element of a sequence, and throws an exception if there is not exactly one element in the sequence."""
        ...

    @staticmethod
    @typing.overload
    def Single(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], bool]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the only element of a sequence that satisfies a specified condition, and throws an exception if more than one such element exists."""
        ...

    @staticmethod
    @typing.overload
    def SingleOrDefault(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the only element of a sequence, or a default value if the sequence is empty; this method throws an exception if there is more than one element in the sequence."""
        ...

    @staticmethod
    @typing.overload
    def SingleOrDefault(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], predicate: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], bool]) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the only element of a sequence that satisfies a specified condition or a default value if no such element exists; this method throws an exception if more than one element satisfies the condition."""
        ...

    @staticmethod
    @typing.overload
    def ToDictionary(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], keySelector: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], System_Linq_ImmutableArrayExtensions_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_TKey, System_Linq_ImmutableArrayExtensions_T]:
        """
        Creates a dictionary based on the contents of this array.
        
        :param keySelector: The key selector.
        :returns: The newly initialized dictionary.
        """
        ...

    @staticmethod
    @typing.overload
    def ToDictionary(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], keySelector: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], System_Linq_ImmutableArrayExtensions_TKey], elementSelector: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], System_Linq_ImmutableArrayExtensions_TElement]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_TKey, System_Linq_ImmutableArrayExtensions_TElement]:
        """
        Creates a dictionary based on the contents of this array.
        
        :param keySelector: The key selector.
        :param elementSelector: The element selector.
        :returns: The newly initialized dictionary.
        """
        ...

    @staticmethod
    @typing.overload
    def ToDictionary(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], keySelector: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], System_Linq_ImmutableArrayExtensions_TKey], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_TKey, System_Linq_ImmutableArrayExtensions_T]:
        """
        Creates a dictionary based on the contents of this array.
        
        :param keySelector: The key selector.
        :param comparer: The comparer to initialize the dictionary with.
        :returns: The newly initialized dictionary.
        """
        ...

    @staticmethod
    @typing.overload
    def ToDictionary(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T], keySelector: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], System_Linq_ImmutableArrayExtensions_TKey], elementSelector: typing.Callable[[System_Linq_ImmutableArrayExtensions_T], System_Linq_ImmutableArrayExtensions_TElement], comparer: System.Collections.Generic.IEqualityComparer[System_Linq_ImmutableArrayExtensions_TKey]) -> System.Collections.Generic.Dictionary[System_Linq_ImmutableArrayExtensions_TKey, System_Linq_ImmutableArrayExtensions_TElement]:
        """
        Creates a dictionary based on the contents of this array.
        
        :param keySelector: The key selector.
        :param elementSelector: The element selector.
        :param comparer: The comparer to initialize the dictionary with.
        :returns: The newly initialized dictionary.
        """
        ...

    @staticmethod
    def ToArray(immutableArray: System.Collections.Immutable.ImmutableArray[System_Linq_ImmutableArrayExtensions_T]) -> typing.List[System_Linq_ImmutableArrayExtensions_T]:
        """
        Copies the contents of this array to a mutable array.
        
        :returns: The newly instantiated array.
        """
        ...

    @staticmethod
    @typing.overload
    def First(builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_T:
        ...

    @staticmethod
    @typing.overload
    def FirstOrDefault(builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the first element in the collection, or the default value if the collection is empty."""
        ...

    @staticmethod
    @typing.overload
    def Last(builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the last element in the collection."""
        ...

    @staticmethod
    @typing.overload
    def LastOrDefault(builder: System.Collections.Immutable.ImmutableArray.Builder) -> System_Linq_ImmutableArrayExtensions_T:
        """Returns the last element in the collection, or the default value if the collection is empty."""
        ...

    @staticmethod
    @typing.overload
    def Any(builder: System.Collections.Immutable.ImmutableArray.Builder) -> bool:
        """Returns a value indicating whether this collection contains any elements."""
        ...


