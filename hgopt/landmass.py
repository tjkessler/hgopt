from parameter import Parameter
from colony import Colony
from utils import calc_cdf_vals, calc_fitness

from bisect import bisect
from random import random
from typing import Callable, Union
from warnings import warn


class Landmass:

    def __init__(self, colony_size: int, objective_fn: Callable[[list], float],
                 obj_fn_args: dict = {}, n_init_colonies: int = 1,
                 max_col_age: int = 8):

        if not callable(objective_fn):
            raise ReferenceError('Supplied objective function is not callable')
        self._obj_fn = objective_fn
        self._obj_fn_args = obj_fn_args
        self._colony_size = colony_size
        self._colonies = []
        self._n_init_colonies = n_init_colonies
        self._params = []
        self._max_col_age = max_col_age

    def add_param(self, min_val: Union[int, float], max_val: Union[int, float],
                  restrict: bool = True):

        if len(self._colonies) > 0:
            raise RuntimeError(
                'Cannot add another parameter after colony initialization'
            )
        self._params.append(Parameter(min_val, max_val, restrict))

    def initlialize(self):

        if len(self._colonies) > 0:
            warn('initialize() called again: re-creating colonies',
                 RuntimeWarning)
        if len(self._params) == 0:
            raise RuntimeError(
                'Cannot create colonies without any parameters'
            )

        self._colonies = [Colony(self._colony_size, self._params)
                          for _ in range(self._n_init_colonies)]

    def search(self, col_decay: float = 1.0):

        if len(self._colonies) == 0:
            raise RuntimeError('Cannot search without colony initialization')

        new_cols = []
        n_orphans = 0
        all_fitness = []

        for col in self._colonies:

            hunter_locs = col.hunt()
            if len(hunter_locs) == 1:
                n_orphans += col._pop_size
                continue

            hunter_fitness_vals = [calc_fitness(self._obj_fn(loc))
                                   for loc in hunter_locs]
            all_fitness.extend(hunter_fitness_vals)
            cdf_vals = calc_cdf_vals(hunter_fitness_vals)

            new_col_sizes = [1 for _ in range(len(hunter_locs))]
            for _ in range(col._pop_size - len(hunter_locs)):
                new_col_sizes[bisect(cdf_vals, random())] += 1

            new_col_age = col._age + col_decay
            if new_col_age > self._max_col_age:
                new_col_age = 1.0
            for idx, size in enumerate(new_col_sizes):
                new_cols.append(Colony(size, self._params, hunter_locs[idx],
                                       new_col_age))

        if n_orphans > 0:
            cdf_vals = calc_cdf_vals(all_fitness)
            for _ in range(n_orphans):
                new_cols[bisect(cdf_vals, random())]._pop_size += 1

        self._colonies = new_cols
