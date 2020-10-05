from landmass import Landmass
from matplotlib import pyplot as plt

OPT_SOLS = [
    (5, 9),
    (5, 1),
    (1, 5),
    (9, 5)
]

MEGA_OPT = (5, 5)


def _from_opt_sol(sol, loc):

    return abs(sol[0] - loc[0]) + abs(sol[1] - loc[1])


def opt_fn(integers):

    distances = [_from_opt_sol(o, integers) for o in OPT_SOLS]
    distances.append(
        (abs(MEGA_OPT[0] - integers[0]) / 2) +
        (abs(MEGA_OPT[1] - integers[1]) / 2))
    return min(distances)


def main():

    lm = Landmass(500, opt_fn, n_init_colonies=1, max_col_age=12)
    lm.add_param(0.0, 10.0)
    lm.add_param(0.0, 10.0)
    lm.initlialize()
    col_locs = []
    col_locs.append([c._location for c in lm._colonies])
    pop_sizes = []
    for i in range(200):
        lm.search()
        pop_sizes.extend([c._pop_size for c in lm._colonies])
        col_locs.append([c._location for c in lm._colonies])

    for idx, locs in enumerate(col_locs):
        x_vals = [l[0] for l in locs]
        y_vals = [l[1] for l in locs]
        plt.clf()
        axes = plt.gca()
        axes.set_xlim([0, 10])
        axes.set_ylim([0, 10])
        plt.title('Blue is Food Source, Green is Best Food Source')
        plt.xlabel('East/West')
        plt.ylabel('North/South')
        plt.scatter(x_vals, y_vals, color='red',
                    s=[5 for _ in range(len(x_vals))])
        plt.scatter([o[0] for o in OPT_SOLS], [o[1] for o in OPT_SOLS],
                    color='blue')
        plt.scatter([5], [5], color='green')
        plt.savefig('img/{}'.format(idx))


if __name__ == '__main__':

    main()
