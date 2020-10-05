from typing import Union


def calc_cdf_vals(fitness_scores: list) -> list:

    fitness_sum = sum(fitness_scores)
    selection_probs = [score / fitness_sum for score in fitness_scores]
    cdf_vals = []
    cumsum = 0
    for p in selection_probs:
        cumsum += p
        cdf_vals.append(cumsum)
    return cdf_vals


def calc_fitness(obj_fn_val: Union[int, float]) -> float:

    if obj_fn_val >= 0:
        return 1 / (obj_fn_val + 1)
    else:
        return 1 + abs(obj_fn_val)
