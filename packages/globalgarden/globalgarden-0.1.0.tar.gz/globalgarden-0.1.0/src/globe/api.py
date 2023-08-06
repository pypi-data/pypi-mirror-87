from abc import ABC, abstractmethod
from typing import List, Tuple, Iterable, Type

from blackopt.abc import Solver, Problem, Solution


class GlobeApi(ABC):
    @abstractmethod
    def add_problem(
        self,
        prob: Problem,
        solution_cls: Type[Solution],
        description: str,
        identifier: str,
    ) -> None:
        """Add a problem to catalog of managed problems. """
        raise NotImplementedError

    @abstractmethod
    def list_problems(self) -> Iterable[Tuple[str, str]]:
        """Lists available problems - returns an iterable over (id, description) tuples. """
        raise NotImplementedError

    @abstractmethod
    def get_task(self, problem_id: str) -> Solver:
        """Get a solver for a problem. """
        raise NotImplementedError

    @abstractmethod
    def upload_population(self, problem_id: str, pop: List[Solution]) -> None:
        """Upload a population of solutions that were found locally for given problem. """
        raise NotImplementedError

    @abstractmethod
    def get_population(self, problem_id: str, number: int) -> List[Solution]:
        """Request a number of solutions to a given problem.

        Provided solutions will be the ones with better scores and lower similarity."""
        raise NotImplementedError
