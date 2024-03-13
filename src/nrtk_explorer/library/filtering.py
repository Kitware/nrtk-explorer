from typing import Protocol, Iterable, Literal, Callable, FrozenSet, TypeVar, Generic

LogicalOperator = Literal["and", "or"]
OperatorFunction = Callable[[bool, bool], bool]


def get_operator_function(operator: LogicalOperator) -> OperatorFunction:
    if operator == "and":
        return lambda a, b: a and b
    else:
        return lambda a, b: a or b


T = TypeVar("T", contravariant=True)


class FilterProtocol(Protocol, Generic[T]):
    def evaluate(self, item: T) -> bool: ...


class NoneFilter(FilterProtocol, Generic[T]):
    def evaluate(self, item: T) -> bool:
        return True


class NotFilter(FilterProtocol, Generic[T]):
    def __init__(self, filter: FilterProtocol):
        self.filter = filter

    def evaluate(self, item: T) -> bool:
        return not self.filter.evaluate(item)


class ComposableFilter(FilterProtocol[T]):
    filter_a: FilterProtocol[T]
    filter_b: FilterProtocol[T]
    operator: LogicalOperator
    operator_fn: OperatorFunction

    def __init__(self):
        self.compose(NoneFilter(), NoneFilter(), "and")

    def compose(self, a: FilterProtocol[T], b: FilterProtocol[T], operator: LogicalOperator):
        self.filter_a = a
        self.filter_b = b
        self.operator = operator
        self.operator_fn = get_operator_function(self.operator)

    def evaluate(self, item: T) -> bool:
        return self.operator_fn(self.filter_a.evaluate(item), self.filter_b.evaluate(item))


class ConcreteIdFilter(FilterProtocol[Iterable[int]]):
    ids: FrozenSet[int]
    operator: LogicalOperator
    operator_fn: OperatorFunction

    def __init__(self):
        self.set_ids([], "and")

    def set_ids(self, ids: Iterable[int], operator: LogicalOperator):
        self.ids = frozenset(ids)
        self.operator = operator

    def evaluate(self, item: Iterable[int]) -> bool:
        if len(self.ids) == 0:
            return True

        matches = 0

        unique_item_ids = frozenset(item)

        for id in unique_item_ids:
            if id in self.ids:
                matches += 1

        if self.operator == "and":
            return matches == len(self.ids)
        else:
            return matches > 0
