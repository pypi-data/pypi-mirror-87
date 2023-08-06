# Ārtap

Ārtap is a framework for robust design optimization in Python. It contains an integrated, multi-physical FEM solver: Agros suite, furthermore it provides simple interfaces for commercial FEM solvers (COMSOL) and meta-heuristic, bayesian or neural network based optimization algorithms surrogate modelling techniques and neural networks.

## Installation

Artap and its dependencies are available as wheel packages for Windows and Linux* distributions:
We recommend to install Artap under a [virtual environment](https://docs.python.org/3/tutorial/venv.html).

    pip install --upgrade pip # make sure that pip is reasonably new
    pip install artap

*The Windows versions are only partially, the linux packages are fully supported at the current version.

### Linux 

You can install the full package, which contains the agrossuite package by the following command:

    pip install --upgrade pip # make sure that pip is reasonably new
    pip install artap[full]

## Basic usage

The goal of this example to show, how we can use Artap to solve a simple, bi-objective optimization problem.

The problem is defined in the following way [GDE3]:

    Minimize f1 = x1
    Minimize f2 = (1+x2) / x1

    subject to
            x1 e [0.1, 1]
            x2 e [0, 5]

The Pareto - front of the following problem is known, it is a simple hyperbola. This problem is very simple for an Evolutionary algorithm, it finds its solution within 20-30 generations.
 NSGA - II algorithm is used to solve this example.

### The Problem definition and solution with NSGA-II in Ārtap:

    class BiObjectiveTestProblem(Problem):

        def set(self):

            self.name = 'Biobjective Test Problem'
            
            self.parameters = [{'name':'x_1', 'bounds': [0.1, 1.]},
                               {'name':'x_2', 'bounds': [0.0, 5.0]}]

            self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                          {'name': 'f_2', 'criteria': 'minimize'}]

        def evaluate(self, individual):
            f1 = individual.vector[0]
            f2 = (1+individual.vector[1])/individual.vector[0]
        return [f1, f2]
 
    # Perform the optimization iterating over 100 times on 100 individuals.
    problem = BiObjectiveTestProblem()
    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 100
    algorithm.options['max_population_size'] = 100
    algorithm.run()

## References

* [GDE3] Saku Kukkonen, Jouni Lampinen, The third Evolution Step of Generalized Differential Evolution


## Citing

If you use Ārtap in your research, the developers would be grateful if you would cite the relevant publications:

[1]  Karban, Pavel, David Pánek, Tamás Orosz, Iveta Petrášová, and Ivo Doležel. “FEM based robust design optimization with Agros and Ārtap.” Computers & Mathematics with Applications (2020) https://doi.org/10.1016/j.camwa.2020.02.010.

[2] Pánek, David, Tamás Orosz, and Pavel Karban. ” Ārtap: robust design optimization framework for engineering applications.” arXiv preprint arXiv:1912.11550 (2019).

### Applications
[3] Karban, P., Pánek, D., & Doležel, I. (2018). Model of induction brazing of nonmagnetic metals using model order reduction approach. COMPEL-The international journal for computation and mathematics in electrical and electronic engineering, 37(4), 1515-1524, https://doi.org/10.1108/COMPEL-08-2017-0356.

[4] Pánek, D., Orosz, T., Kropík, P., Karban, P., & Doležel, I. (2019, June). Reduced-Order Model Based Temperature Control of Induction Brazing Process. In 2019 Electric Power Quality and Supply Reliability Conference (PQ) & 2019 Symposium on Electrical Engineering and Mechatronics (SEEM) (pp. 1-4). IEEE, https://doi.org/10.1109/PQ.2019.8818256.

[5] Pánek, D., Karban, P., & Doležel, I. (2019). Calibration of Numerical Model of Magnetic Induction Brazing. IEEE Transactions on Magnetics, 55(6), 1-4, https://doi.org/10.1109/TMAG.2019.2897571.

[6] Pánek, D., Orosz, T., Karban, P., & Doležel, I. (2020), “Comparison of simplified techniques for solving selected coupled electroheat problems”, COMPEL – The international journal for computation and mathematics in electrical and electronic engineering, Vol. 39 No. 1, pp. 220-230. https://doi.org/10.1108/COMPEL-06-2019-0244

[7] Orosz, T.; Pánek, D.; Karban, P. FEM Based Preliminary Design Optimization in Case of Large Power Transformers. Appl. Sci. 2020, 10, 1361, https://doi.org/10.3390/app10041361.

## Contact

If you have any questions, do not hesitate to contact us: artap.framework@gmail.com

## License

Ārtap is published under [MIT license](https://en.wikipedia.org/wiki/MIT_License)
