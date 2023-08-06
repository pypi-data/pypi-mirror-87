#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#
"""Type objects (stubs).

Here we only provide typing information for the type checker (with very little
or no implementation).

"""
import enum
import numbers
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from locale import getdefaultlocale
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
)
from typing import Type as PythonType
from typing import TypeVar, Union

from babel.numbers import format_decimal, parse_decimal
from typing_extensions import Protocol, runtime
from xotl.tools.objects import memoized_property
from xotl.tools.symbols import Unset
from xotless.domains import Domain, Range
from xotless.pickablenv import PickableRecordset
from xotless.types import EqTypeClass, OrdTypeClass

from .exceptions import SoftTimeLimitExceeded
from .i18n import _


class Commodity(Protocol):
    """A commodity is a description of what's being consumed.

    This is different from the product that's being sold/purchased.  A product
    is way to sale/purchase a commodity.

    The definition of a Commodity is a vast one.  This type only serves as way
    to document what the Pricing Systems elements use.

    """

    def replace(self, **attrs) -> "Commodity":
        ...


C = TypeVar(
    "C", bound=Commodity
)  # The type of items in a demand: commodities, products, etc.
R = TypeVar("R", bound="Request")


@runtime
class Request(Protocol[C]):
    """A request for a commodity in a given quantity."""

    #: The commodity requested
    commodity: C

    #: The quantity requested.  It's given in terms of the commodity itself.
    #: This is usually 1, because the commodity may comprise several Units of
    #: Consumption.
    quantity: int

    def replace(self: R, **attrs) -> R:
        ...


D = TypeVar("D", bound="Demand")


@runtime
class Demand(Protocol[C]):
    """An abstract view of what's being priced."""

    #: We assume that prices may change due to the demand's date.
    date: datetime

    #: The requested "items" (commodities).
    requests: Sequence[Request[C]]

    def get_commodities(self) -> Iterable[C]:
        "Get all the commodities of the demand."
        ...

    def replace(self: D, **attrs) -> D:
        "Return a new demand replacing some its attributes"
        ...

    def to_html(self):
        requests = " ".join(
            [
                f"<p>{getattr(r.commodity, 'name', str(r.commodity))}: {r.quantity}</p>"
                for r in self.requests
            ]
        )
        result = (
            f"<p><strong>Demand date:&nbsp;</strong>{self.date.strftime('%F %H:%m')}</p>"
        )
        if requests:
            result += f"<strong>Demand requests:</strong>{requests}"
        return result


class _Undefined(numbers.Number):
    _instances = {}  # type: Mapping[str, _Undefined]

    def __new__(cls, name):
        res = cls._instances.get(name, Unset)
        if res is Unset:
            res = super().__new__(cls)
            res.__init__(name)
            cls._instances[name] = res
        return res

    def __getnewargs__(self):
        return (self.__name,)

    def __init__(self, name):
        self.__name = name

    def idem(self, other: Any) -> "Result":
        return self

    def selfy(self) -> "Result":
        return self

    __add__ = __radd__ = __iadd__ = idem
    __sub__ = __rsub__ = __isub__ = idem
    __mul__ = __rmul__ = __imul__ = idem
    __div__ = __rdiv__ = __idiv__ = idem
    __truediv__ = __rtruediv__ = __itruediv__ = idem
    __floordiv__ = __rfloordiv__ = __ifloordiv__ = idem
    __mod__ = __rmod__ = __imod__ = idem
    __pow__ = __rpow__ = __ipow__ = idem

    __trunc__ = selfy

    def __float__(self):
        raise ValueError("cannot convert Undefined to float")

    def __int__(self):
        raise ValueError("cannot convert Undefined to int")

    __abs__ = selfy
    __neg__ = selfy
    __invert__ = selfy

    def __bool__(self):
        return False

    def __str__(self):
        return self.__name

    __repr__ = __str__

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return other is self

    def __ne__(self, other):
        return self is not other

    def nope(self, other):
        # `date` is included so that we can use _Undefined to represent the
        # AnyOtherValue.  At this point, _Undefined should compare with any
        # OrdTypeClass instance.
        if isinstance(other, (numbers.Number, date, timedelta)):
            return False
        else:
            return NotImplemented

    __lt__ = __le__ = __gt__ = __ge__ = nope

    del idem, selfy, nope


Undefined = _Undefined(_("Undefined"))
assert Undefined is _Undefined(_("Undefined"))


#: Possible values for pricing results: a number or Undefined.
Result = Union[float, int, _Undefined]


#: A mapping from names to values (of type Result) that can be used during
#: price computation.
Environment = Mapping[str, Result]


class PriceResultType(Protocol[C]):
    """The result of price computation.

    The procedure can provide a `title` for the `result`, and also
    sub-results to provide insight about how the price was computed.

    """

    title: str
    procedure: Optional["Procedure"]
    result: Result

    # A price result has several 'children' result which contain information
    # about the method used to compute `result` and `title`.
    #
    # There's no a pre-established requirement between the `result` of the
    # children and the parent's result.
    #
    # It's up to the program to create the information.
    @property
    def subresults(self) -> Sequence["PriceResultType[C]"]:
        ...

    # The same procedure can be used iteratively to compute sub-demands.  Also
    # the environment can change from one call to the other.  The only way to
    # distinguish price results resulting from the same procedure is to know
    # both the demand priced and the environment.
    @property
    def demand(self) -> Demand[C]:
        ...

    @property
    def env(self) -> Environment:
        ...

    def replace(self, **kwargs) -> "PriceResultType[C]":
        ...


class ATTRIBUTE_OWNER(enum.IntEnum):
    DEMAND = 1
    REQUEST = 2
    COMMODITY = 3


class TypeName(enum.Enum):
    """Basic (or primitive) type names.

    We have an UNKNOWN type which represent undecidable values.  No value has
    actually that type, but `from_value`:meth: will default to it.

    """

    INT = "integer"
    FLOAT = "float"
    STR = "char"

    # FIXME: This is actually a polymorphic type, very much like the type
    # `forall a. [a]` in Haskell.
    #
    # I thought SELECTION as an equivalent of sum-types (without type
    # arguments); but this has been shown shortsighted.
    #
    # We use the SELECTION to abstract details of how those values are
    # implemented:
    #
    # 1. An attribute correspoding to field.Selection with int keys.
    #
    # 2. An attribute correspoding to field.Selection with str keys.
    #
    # 3. An attribute correspoding to field.Many2one,
    #
    # 4. (REMOVED) Any attribute of any type for which the AVM contains a
    #    limited set of possible values.
    #
    # The first two cases play fairly nicely with the Web Client.  The 3rd
    # requires that we expose the underlying many2one type to the web client
    # (or implement a completely new field and widget).
    #
    # The 4th rule, however, can completely fool the web client and the
    # website for some types of values (e.g, datetime).  When
    # serializing/unserializing values of this type, we must know how to
    # serialize/unseralized its underlying type.
    #
    # For the time being, we're hacking our way out of this mess in clients of
    # this module.  But I need to let this clear: This type must be fixed!
    SELECTION = "selection"

    DATE = "date"
    DATETIME = "datetime"
    BOOL = "boolean"
    TIMEDELTA = "timedelta"
    UNKNOWN = "unknown"

    @classmethod
    def from_python_type(cls, ttype: PythonType) -> "TypeName":
        """Get the equivalent TypeName from a python type."""
        return cls.__members__.get(ttype.__name__.upper(), cls.UNKNOWN)

    @classmethod
    def from_value(cls, val: Any) -> "TypeName":
        return cls.from_python_type(type(val))


class Record(PickableRecordset):
    """A pickable object to represent a singleton recorset."""

    @property
    def display_name(self) -> str:
        return self.instance.display_name

    @memoized_property
    def id(self):
        return self.instance.id

    @classmethod
    def from_recordset(cls, recordset):
        if len(recordset) > 1:
            recordset = recordset[0]
        return super(Record, cls).from_recordset(recordset)


class EnumerationMember(NamedTuple):
    id: Union[str, int]
    name: str
    object: Optional[Record] = None


GET_VALUES_TYPE = Callable[[], Sequence[EnumerationMember]]
FIND_VALUE_TYPE = Callable[[str], Any]


@dataclass(unsafe_hash=True)
class SimpleType:
    """A simple type.

    The `TypeName` just names the types, but it doesn't have access to the
    values.  A `SimpleType` can be queries about values.

    Some types have an infinite number of members, and, then,
    `get_values`:func: and `search_value`:func: return the empty sequence.

    """

    name: TypeName

    # IMPORTANT: these callable must be pickable and comparable.
    _get_values: Optional[GET_VALUES_TYPE]
    _find_value: Optional[FIND_VALUE_TYPE]

    __slots__ = ("name", "_get_values", "_find_value")

    @property
    def get_values(self) -> GET_VALUES_TYPE:
        if self._get_values is not None:
            return self._get_values
        else:
            return lambda: []

    @property
    def find_value(self) -> FIND_VALUE_TYPE:
        if self._find_value is not None:
            return self._find_value
        else:
            return lambda name: None

    def __init__(
        self,
        name: TypeName,
        get_values: Optional[GET_VALUES_TYPE] = None,
        find_value: Optional[FIND_VALUE_TYPE] = None,
    ) -> None:
        self.name = name
        self._get_values = get_values
        self._find_value = find_value

    @classmethod
    def from_python_type(cls, ttype: PythonType) -> "SimpleType":
        return cls(TypeName.from_python_type(ttype))

    @classmethod
    def from_python_enum(cls, enumcls) -> "SimpleType":
        """Create a selection simple type from an enumeration class.

        We assume the values of the enumerations are all strings.

        """

        def get_values() -> Sequence[EnumerationMember]:
            return [
                EnumerationMember(str(val), str(val).title())
                for val in enumcls.__members__.values()
            ]

        def find_value(name) -> Any:
            return next(
                (
                    EnumerationMember(str(val), str(val).title())
                    for member, val in enumcls.__members__.items()
                    if name == member
                ),
                None,
            )

        return cls(TypeName.SELECTION, get_values, find_value)

    def typecheck_value(self, val: Any) -> bool:
        """Try to check if 'val' is an instance of this type."""
        if self.name == TypeName.INT:
            return isinstance(val, int)
        elif self.name == TypeName.FLOAT:
            return isinstance(val, (float, int))
        elif self.name == TypeName.STR:
            return isinstance(val, str)
        elif self.name == TypeName.DATE:
            return isinstance(val, date) and not isinstance(val, datetime)
        elif self.name == TypeName.DATETIME:
            return isinstance(val, datetime)
        elif self.name == TypeName.BOOL:
            return isinstance(val, bool)
        elif self.name == TypeName.TIMEDELTA:
            return isinstance(val, timedelta)
        elif self.name == TypeName.SELECTION:
            try:
                values = {
                    member.object.instance if member.object else member.id
                    for member in self.get_values()
                }
                return val in values
            except SoftTimeLimitExceeded:
                raise
            except Exception:
                pass
        return False


class TypedAttribute:
    """An attribute annotated with a type.

    The `name` is attribute's name in the commodity, it must be a property
    Python identifier.

    The `type` is a instance of `SimpleType`:class: describe the possible
    values the attribute can take.

    The `display_name`, if provided, is used to return a *display name*, i.e a
    name which is sensible to show to users in UI and reports.

    .. important:: Should not store an i18n-ed value in `display_name`.

       Instances of TypeAttribute might be saved for reuse in other contexts,
       so it's best to apply i18n when you're going to show the value to
       users.  Don't store it.

    """

    name: str
    type: SimpleType

    # I don't think we should use the display_name for comparison.  If `name`
    # and `type` are equal, then the instances are equal as well.
    display_name: Optional[str]

    __slots__ = ("name", "type", "display_name")

    def __init__(self, name: str, type: SimpleType, display_name: str = None):
        self.name = name
        self.type = type
        self.display_name = display_name

    def __eq__(self, other):
        if isinstance(other, TypedAttribute):
            return self.name == other.name and self.type == other.type
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.name, self.type))

    def __repr__(self):
        return f"TypedAttribute({self.name!r}, {self.type!r})"

    def get_display_name(self, capitalize="none"):
        """A printable name for the attribute.

        If `display_name` was provided, return it without any transformation.

        If no `display_name` was provided, we take the name and replace '_' by
        spaces.  The argument to `capitalize` could be:

        - 'none'; perform no capitalization
        - 'first'; capitalize the first word only
        - 'all'; capitalize all the words

        """
        if self.display_name:
            return self.display_name

        result = self.name.replace("_", " ")
        capitalize = capitalize.lower()
        if capitalize == "first":
            result = result.capitalize()
        elif capitalize == "all":
            result = " ".join(word.capitalize() for word in result.split(" "))
        else:
            assert capitalize == "none"
        return result

    @classmethod
    def from_typed_name(
        cls, name: str, ttype: PythonType, display_name: str = None
    ) -> "TypedAttribute":
        return cls(name, SimpleType.from_python_type(ttype), display_name)


class Text(str):
    "A string which is meant to have several lines and be big"
    pass


@dataclass(unsafe_hash=True)
class AttributeLocator:
    owner: ATTRIBUTE_OWNER
    attr: TypedAttribute

    __slots__ = ("owner", "attr")

    def __init__(self, owner: ATTRIBUTE_OWNER, attr: TypedAttribute) -> None:
        assert isinstance(owner, ATTRIBUTE_OWNER), f"Invalid value for owner: {owner}"
        assert isinstance(attr, TypedAttribute), f"Invalid value for attr: {attr}"
        self.owner = owner
        self.attr = attr

    @classmethod
    def _typed_attr_from_args(
        cls,
        attr_or_name: Union[str, TypedAttribute],
        _type: PythonType = None,
        display_name: str = None,
    ) -> TypedAttribute:
        if isinstance(attr_or_name, TypedAttribute):
            return attr_or_name
        else:
            assert _type is not None
            return TypedAttribute(
                str(attr_or_name),
                SimpleType.from_python_type(_type),
                display_name=display_name,
            )

    @classmethod
    def of_demand(
        cls, attr_or_name: Union[str, TypedAttribute], _type: PythonType = None
    ) -> "AttributeLocator":
        return cls(ATTRIBUTE_OWNER.DEMAND, cls._typed_attr_from_args(attr_or_name, _type))

    @classmethod
    def of_request(
        cls, attr_or_name: Union[str, TypedAttribute], _type: PythonType = None
    ) -> "AttributeLocator":
        return cls(
            ATTRIBUTE_OWNER.REQUEST, cls._typed_attr_from_args(attr_or_name, _type)
        )

    @classmethod
    def of_commodity(
        cls,
        attr_or_name: Union[str, TypedAttribute],
        _type: PythonType = None,
        display_name: str = None,
    ) -> "AttributeLocator":
        return cls(
            ATTRIBUTE_OWNER.COMMODITY,
            cls._typed_attr_from_args(attr_or_name, _type, display_name),
        )

    def get(self, obj, default=Unset):
        from xotl.tools.objects import traverse

        assert self.owner != ATTRIBUTE_OWNER.DEMAND or isinstance(obj, Demand)
        assert self.owner != ATTRIBUTE_OWNER.REQUEST or isinstance(obj, Request)
        return traverse(obj, self.attr.name, default=default)

    def lookup(self, demand: D, default=None) -> Sequence[Any]:
        """Lookup this attribute in a demand.

        The return type must be a sequence, because a demand can have multiple
        requests (and commodities) and when the locator points to REQUEST or
        COMMODITY, we must return all values.

        """
        if self.owner == ATTRIBUTE_OWNER.DEMAND:
            return (getattr(demand, self.attr.name, default),)
        elif self.owner == ATTRIBUTE_OWNER.REQUEST:
            return tuple(
                getattr(request, self.attr.name, default) for request in demand.requests
            )
        else:
            return tuple(
                getattr(request.commodity, self.attr.name, default)
                for request in demand.requests
            )

    def update(self, demand: D, value: Any) -> D:
        """Get a new demand updating the locator's value.

        If the original demand has no requests and the locator's owner is
        REQUEST or COMMODITY, create a new request with a commodity.

        """

        from .structs import Request as RequestImpl

        if self.owner == ATTRIBUTE_OWNER.DEMAND:
            return demand.replace(**{str(self.attr.name): value})
        else:
            if not demand.requests:
                requests: Sequence[Request] = (RequestImpl.new(),)
            else:
                requests = demand.requests
            if self.owner == ATTRIBUTE_OWNER.REQUEST:
                return demand.replace(
                    requests=tuple(
                        request.replace(**{str(self.attr.name): value})
                        for request in requests
                    )
                )
            elif self.owner == ATTRIBUTE_OWNER.COMMODITY:
                return demand.replace(
                    requests=tuple(
                        request.replace(
                            commodity=request.commodity.replace(
                                **{str(self.attr.name): value}
                            )
                        )
                        for request in requests
                    )
                )
            else:
                assert False


# Attribute Variability Map.  Each pair is composed by an attribute locator
# and a sequence domains.
#
# We used to say that the domains must be disjoint, but MergeAVM does not
# warrant domains are not disjoint.  I think this is true for all *sensible*
# pricing programs.  But it's not easy to actually enforce.
#
# A simple program with:
#
#                    Sum Procedure
#                           |
#           .---------------+--------------.
#           |                              |
#           v                              v
#        Branches                       Branches
#        1   to 10                      1  to 15
#        10  to 20                      15 to 30
#
# Yields an AVM with overlapping domains.  However, it's quite hard to
# describe this program as a table (the AVM's primary use case).
#
# Possibly the issue is that MergeAVM is not a proper combinator, and we need
# a better combinator for this kind of programs.
#
AVM = Mapping[AttributeLocator, Sequence[Domain]]

# Some internal caches require this to type-check
_MutableAVM = MutableMapping[AttributeLocator, Sequence[Domain]]


# Environment Variable Map.  The name of the variable a possible default value
# for it.
EVM = Mapping[str, Result]


class SupportsAVM(Protocol):
    "Any object which has a Attribute Variability Map"

    @property
    def avm(self) -> AVM:
        ...


class SupportsEVM(Protocol):
    "Any object which has a EnvVariablesMap"

    @property
    def evm(self) -> EVM:
        ...


class SupportsPartialDefinition(Protocol):
    "Any object which may be partially defined"

    # All steps in the UI support partial definition.  Since the introduction
    # of FormulaProcedure some procedures can be built and still be partially
    # defined.
    #
    # Thus the UI now SHOULD test if the base_procedure supports this
    # protocol.

    @property
    def completely_defined(self) -> bool:
        ...


class Procedure(SupportsAVM, SupportsEVM, Protocol[C]):
    """The computational unit to compute a price of a demand on a given
    environment.

    """

    def __call__(self, demand: Demand[C], env: Environment) -> PriceResultType[C]:
        ...

    def __hash__(self):
        ...

    def __len__(self):
        ...

    @property
    def depth(self) -> int:
        ...

    def __iter__(self) -> Iterator["Procedure"]:
        ...

    def add_to_travertine_program(self, program):
        r"""Add the current procedure to a Travertine Program.

        You cannot add the same procedure in the program twice.  That's why
        this is not intended to be a recursive method.  Instead you should
        follow a depth-first traversal of the pricing program and add the
        procedures following that order.

        To add the following graph of nodes::

            a ------> c -----------------.
            |        / \                 |
            | .-----'   '----.           v
            | |               '-> f <--- e
            v v                   |
             b  -----> d <--------'

        You must add first the procedure in node 'd', then you could add 'b',
        'f', 'e', 'c', and finally 'a'.

        This is actually following a topological order of the graph.

        """
        ...


class NamedProcedureType(Procedure[C], Protocol):
    title: str


class KIND(type):
    "The type for RANGE and MATCH"
    pass


@dataclass(frozen=True)
class RANGE(metaclass=KIND):
    "A predicate that does lower <= value < upper"
    lower: OrdTypeClass
    upper: OrdTypeClass

    __slots__ = ("lower", "upper")

    @classmethod
    def from_range(self, r: Range):
        return RANGE(r.lowerbound, r.upperbound)


@dataclass(frozen=True)
class MATCH(metaclass=KIND):
    "A predicate that does demand_value == value"
    value: EqTypeClass

    __slots__ = ("value",)


@dataclass
class PredicateKind:
    comparison_kind: Optional[Union[RANGE, MATCH]]
    attr: Optional[AttributeLocator]

    __slots__ = ("attr", "comparison_kind")

    def same_kind(self, other: "PredicateKind") -> bool:
        if self.attr is None or self.comparison_kind is None:
            return False
        if other.attr == self.attr:
            return type(self.comparison_kind) == type(other.comparison_kind)  # noqa
        return False


NO_KIND = PredicateKind(None, None)


class Predicate(SupportsAVM, Protocol):
    """Tests some specific condition on the demand and/or the environment.

    Currently, we use it to model branching.

    """

    def __hash__(self):
        ...

    def get_kind(self) -> PredicateKind:
        ...


#: A Branch just the pair of a Predicate and a Procedure (in the context of
#: the BranchProcedure).
Branch = Tuple[Predicate, Procedure]


class Splitter(Protocol[C]):
    """A splitter takes a demand a splits it into many sub-demands.

    This allows for iteration in the computation.  The simplest splitter (the
    identity) returns the same demand.  Others may simply group request by
    given attributes, other may split request per quantity, etc.

    """

    def __call__(self, demand: Demand[C], env: Environment) -> Iterable[Demand[C]]:
        ...

    def __hash__(self):
        ...


class Aggregator(Protocol):
    "An aggregator takes many results and produces a single one."

    def __call__(
        self,
        results: Sequence[PriceResultType],
        title: str,
        demand: Demand,
        env: Environment,
        proc: Procedure = None,
    ) -> PriceResultType:
        ...

    def __hash__(self):
        ...


def parse_result(value, locale=None, undefined_repr="-"):
    """Parse a possibly localized representation a result given in `value`.

    If `value` is already a number or Undefined, return it unchanged.  If not
    it should be a string representing a number in the given `locale`.

    The value of `locale` must a string with name of locale, compatible with
    `~babel.numbers.parse_decimal`:func.  If `locale` is None, we get from
    `~locale.getdefaultlocale`:func:.

    If `value` is not parseable, but is equal to `undefined_repr`, return
    Undefined.

    """
    if isinstance(value, (int, float, _Undefined)):
        return value
    if not locale:
        locale = ".".join(getdefaultlocale())
    try:
        # Convert to float because Object of type 'Decimal' is not JSON
        # serializable
        return float(parse_decimal(value, locale=locale))
    except ValueError:
        if value == undefined_repr:
            return Undefined
        else:
            raise


def format_result(value, locale=None, undefined_repr="-"):
    """Format a `value` as a string representation in a given `locale`.

    The value of `locale` must a string with name of locale, compatible with
    `~babel.numbers.format_decimal`:func.  If `locale` is None, we get from
    `~locale.getdefaultlocale`:func:.

    """
    if not locale:
        locale = ".".join(getdefaultlocale())
    if isinstance(value, _Undefined):
        return undefined_repr
    else:
        return format_decimal(value, locale=locale)
