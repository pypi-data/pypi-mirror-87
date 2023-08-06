import time

from loguru import logger
from blackopt import EarlyStopException

from globe.api import GlobeApi
from globe.sim_server import SimServer


class Worker:
    WORK_PERIOD = 15 * 60  # 15 minutes

    def __init__(self, connection: GlobeApi):
        self.connection = connection

    def iteration(self, problem_id: str):
        solver = self.connection.get_task(problem_id)
        start = time.time()
        logger.info(f"Running solver {solver}.")
        try:
            while time.time() - start < self.WORK_PERIOD:
                solver.step()
        except EarlyStopException:
            logger.info(
                f"Optimization converged after {time.time() - start:.2f} seconds."
            )
        self.connection.upload_population(problem_id, solver.population)

    def launch(self, problem_id: str):
        logger.info(f"Solving problem '{problem_id}'.")
        while True:
            self.iteration(problem_id)


if __name__ == "__main__":
    from blackopt.examples.problems.bumpy import BumpySolution, BumpyProblem

    server = SimServer()
    prob = BumpyProblem.random_problem(10, 10)
    server.add_problem(prob, BumpySolution, "bumpy", "a hard math problem.")

    w = Worker(server)
    w.work_period = 5
    w.launch("bumpy")
