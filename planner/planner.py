import time

from models.user import User
from models.enums import SearchAlgorithm

from planner.result import PlannerResult

from search.greedy import GreedySearch
from search.astar import AStarSearch


class Planner:
    """
    Smart Planner System.

    Bertugas mengoordinasikan proses penyusunan
    jadwal olahraga mingguan menggunakan
    Greedy Search maupun A* Search.
    """

    def __init__(self):

        self.greedy = GreedySearch()
        self.astar = AStarSearch()

    def generate_schedule(
        self,
        user: User,
        algorithm: SearchAlgorithm,
    ) -> PlannerResult:
        """
        Menjalankan algoritma yang dipilih.
        """

        start_time = time.perf_counter()

        if algorithm == SearchAlgorithm.GREEDY:

            state = self.greedy.search(user)

            expanded_nodes = getattr(
                self.greedy,
                "expanded_nodes",
                0,
            )

        elif algorithm == SearchAlgorithm.ASTAR:

            state = self.astar.search(user)

            expanded_nodes = getattr(
                self.astar,
                "expanded_nodes",
                0,
            )

        else:

            raise ValueError(
                f"Unsupported algorithm: {algorithm}"
            )

        execution_time = (
            time.perf_counter() - start_time
        )

        return PlannerResult(

            schedule=state.schedule,

            total_calories=state.total_calories,

            total_fatigue=state.fatigue,

            algorithm=algorithm.name,

            success=True,

            execution_time=execution_time,

            expanded_nodes=expanded_nodes,

            message="Schedule generated successfully.",
        )

    def run_greedy(
        self,
        user: User,
    ) -> PlannerResult:
        """
        Menjalankan Greedy Search.
        """

        return self.generate_schedule(
            user,
            SearchAlgorithm.GREEDY,
        )

    def run_astar(
        self,
        user: User,
    ) -> PlannerResult:
        """
        Menjalankan A* Search.
        """

        return self.generate_schedule(
            user,
            SearchAlgorithm.ASTAR,
        )

    @staticmethod
    def available_algorithms() -> list[str]:
        """
        Mengembalikan daftar algoritma yang tersedia.
        """

        return [
            algorithm.name
            for algorithm in SearchAlgorithm
        ]