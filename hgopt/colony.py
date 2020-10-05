

class Colony:

    def __init__(self, pop_size: int, params: list, loc: list = None,
                 age: int = 1):

        self._pop_size = pop_size
        self._params = params
        if loc is None:
            self._location = [p.rand_val for p in self._params]
        else:
            self._location = loc
        self._age = age

    def hunt(self, hunter_prop: float = 0.5) -> list:

        return [[p.mutate(self._location[i], 1 / self._age)
                for i, p in enumerate(self._params)]
                for _ in range(max(int(hunter_prop * self._pop_size), 1))]
