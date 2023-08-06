import unittest
from ..problem import Problem
from ..individual import Individual
from ..operators import CustomGenerator, LHSGenerator, Evaluator
from ..algorithm import DummyAlgorithm
from ..algorithm_sweep import SweepAlgorithm


class SweepProblem(Problem):
    """ Describe simple one objective optimization problem. """
    def set(self):
        self.name = "SweepProblem"
        self.parameters = [{'name': 'x_1', 'initial_value': 10, 'bounds': [-10, 30]}]
        self.costs = [{'name': 'F_1', 'criteria': 'minimize'}]

    def evaluate(self, individual: Individual):
        result = 0
        for i in individual.vector:
            result += i**2

        return [result]


class TestJob(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_sweep_evaluate_parallel(self):
        problem = SweepProblem()
        generator = LHSGenerator(problem.parameters)
        generator.init(4)

        algorithm = SweepAlgorithm(problem, generator=generator)
        algorithm.options['max_processes'] = 2
        algorithm.run()

        individuals = problem.individuals
        # print(individuals)

        # values
        self.assertEqual(len(individuals), 4)
        self.assertAlmostEqual(individuals[0].costs[0], individuals[0].vector[0] ** 2)
        self.assertAlmostEqual(individuals[1].costs[0], individuals[1].vector[0] ** 2)
        self.assertAlmostEqual(individuals[2].costs[0], individuals[2].vector[0] ** 2)
        self.assertAlmostEqual(individuals[3].costs[0], individuals[3].vector[0] ** 2)

    def test_sweep_evaluate_serial(self):
        problem = SweepProblem()

        gen = CustomGenerator(problem.parameters)
        gen.init([[1, 2, 2], [3, 3, 2]])

        algorithm = SweepAlgorithm(problem, generator=gen)
        algorithm.run()

        individuals = problem.individuals
        self.assertEqual(individuals[0].costs, [9])
        self.assertEqual(individuals[1].costs, [22])

    def test_dummy_evaluate_serial(self):
        problem = SweepProblem()

        i1 = Individual([1, 2, 2])
        i2 = Individual([3, 3, 2])
        individuals = [i1, i2]

        algorithm = DummyAlgorithm(problem)
        algorithm.evaluate(individuals)

        self.assertEqual(individuals[0].costs, [9])
        self.assertEqual(individuals[1].costs, [22])

    def test_dummy_evaluate_parallel(self):
        problem = SweepProblem()

        i1 = Individual([1, 2, 2])
        i2 = Individual([3, 3, 2])
        individuals = [i1, i2]

        algorithm = DummyAlgorithm(problem)
        algorithm.options['max_processes'] = 2
        algorithm.evaluate(individuals)

        self.assertEqual(individuals[0].costs, [9])
        self.assertEqual(individuals[1].costs, [22])


if __name__ == '__main__':
    unittest.main()
