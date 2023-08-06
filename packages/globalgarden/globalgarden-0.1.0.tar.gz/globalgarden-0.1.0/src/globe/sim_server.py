from collections import defaultdict
from typing import Dict, Tuple, List, Iterable, Type
import random
from loguru import logger

from blackopt.abc import Problem, Solution, Solver
from blackopt.algorithms import OffspringSelection

from src.globe.api import GlobeApi


class SimServer(GlobeApi):
    """Simulates a Globe server locally. """

    def __init__(self):
        self.problems: Dict[str, Tuple[Problem, type, str]] = {}
        self.populations: Dict[str, List[Solution]] = defaultdict(list)

    def add_problem(
        self,
        prob: Problem,
        solution_cls: Type[Solution],
        identifier: str,
        description: str,
    ) -> None:
        logger.info(f"adding problem '{identifier}'")

        if identifier in self.problems:
            raise Exception(f"The identifier {identifier} is already in use")
        if len(description) < 10:
            raise Exception("Please provide a longer description.")
        self.problems[identifier] = (prob, solution_cls, description)

    def list_problems(self) -> Iterable[Tuple[str, str]]:
        """Lists available problems - returns an iterable over (id, description) tuples. """

        logger.info(f"listing existing problems")
        return [(k, v[2]) for k, v in self.problems.items()]

    def get_task(self, problem_id) -> Solver:
        logger.info(f"problem '{problem_id}': Getting a task")
        problem, solution_cls, descr = self.problems[problem_id]
        solver = OffspringSelection(problem, solution_cls, popsize=30, mutation_rate=1)
        solver.population = random.sample(
            self.populations[problem_id] + solver.population, k=solver.popsize
        )
        return solver

    def upload_population(self, problem_id: str, pop: List[Solution]) -> None:
        logger.info(f"problem '{problem_id}': Uploading population of size {len(pop)}")
        self.populations[problem_id].extend(pop)
        self.populations[problem_id].sort(key=lambda x: x.score, reverse=True)
        logger.info(
            f"problem '{problem_id}': Best known solution has fitness {self.populations[problem_id][0].score}"
        )

    def get_population(self, problem_id: str, number: int) -> List[Solution]:
        logger.info(f"problem '{problem_id}': Retrieving a population of size {number}")
        return random.sample(self.populations[problem_id], k=number)
