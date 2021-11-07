from collections import defaultdict, Counter
from itertools import repeat
from random import Random
from typing import Iterable, Optional, T


State = T
Subchain = tuple[Optional[State],...]


class Chain:

    """ 

        A minimal, generic Markov chain for use with uniform, hashable,
        non-NoneType elements. Behavior with mixed type elements is undefined.

    """

    class Distribution:

        """ Represents a frequency distribution for an arbitrary step in the chain. """

        def __init__(self) -> None:
            self._tally = Counter()

        def __iter__(self):
            return iter(self._tally.items())

        def record(self, outcome: State) -> None:
            self._tally[outcome] += 1

        def sample(self, rng: Random) -> Optional[State]:                  #TODO: python 3.10:
            total, limit = 0, sum(self._tally.values()) * rng.random()     #limit = self._tally.total() * rrng.andom()
            for outcome, occurences in self:
                total += occurences
                if total > limit:
                    return outcome
            return None

    def __init__(self, order: int, random: Optional[Random] = None) -> None:
        if not int(order) > 0:
            raise ValueError('Order must be a positive integer.')
        self._order = order
        self._rng = random or Random()
        self._map = defaultdict(Chain.Distribution)

    def train(self, example: Iterable[State]) -> None:
        if self._is_readable(example := list(example)):
            example = self._delimit(example)
            for i in range(len(example)-self._order):
                cause = example[i : i+self._order]
                effect = example[i+self._order]
                self._map[(*cause,)].record(effect)

    # The validation performed by _from(...) has to be done outside the generator function,
    # otherwise it doesn't raise errors until client code iterates our return value.
    # Otherwise, this wrapper function has no reason to exist.    
    def finite(self, first: Optional[State]=None) -> Iterable[State]:
        return self._make_finite_model(self._from(first))

    # The validation performed by _from(...) has to be done outside the generator function,
    # otherwise it doesn't raise errors until client code iterates our return value.
    # Otherwise, this wrapper function has no reason to exist.
    def infinite(self) -> Iterable[State]:
        return self._make_infinite_model(self._from(None))
    
    def _delimit(self, sequence: list[State]) -> list[State]:
        return [*repeat(None, self._order), *sequence, None]

    def _sample(self, input: Subchain) -> Optional[State]:
        return self._map[input].sample(self._rng)

    def _is_readable(self, states: list[State]):
        if len(states) > 0:                                             # Should it NOT throw an error if given an empty list?
            if all(state is not None for state in states):              # if all(state is not None for state in states):
                return True                                             #     return len(states) > 0
            else: raise TypeError('Chain input cannot be NoneType.')    # raise TypeError('Chain input cannot be NoneType.')
        else: raise ValueError('Chain input was empty.')

    def _from(self, first: State) -> Subchain:
        if len(self._map) > 0:
            prefix =  repeat(None, self._order-1)
            origin =  (*prefix, first)
            if origin in self._map:
                return origin
            else: raise ValueError('State was not an entry point into the chain.')
        else: raise ValueError('Chain could not be modeled because it is empty.')

    def _make_finite_model(self, from_: Subchain) -> Iterable[State]:
        first_ = from_[-1]
        if first_ is not None: yield first_
        while (next_ := self._sample(from_)) is not None:
            yield next_
            from_ = (*from_[1:], next_)
        
    def _make_infinite_model(self, from_: Subchain):
        while True: yield from self._make_finite_model(from_)