
import numpy as np
import math


# https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.shortest_path.html
files = ["level5/level5_example.in"] + ["level5/level5_{}.in".format(i) for i  in range(1,6)]
outfiles = ["level5/level5_ex.out"] + ["level5/level5_{}.out".format(i) for i  in range(1,6)]


def run(fname):
    terrain = []
    countries = []
    country_border_counts = {}
    country_sum_x = {}
    country_sum_y = {}
    country_c = {}

    prices = {}
    with open(fname) as f:
        lines = f.readlines()
        k = int(lines[0].strip())
        for line in lines[1:k+1]:
            ints = [int(x) for x in line.strip().split()]
            if ints[0] in prices:
                if prices[ints[0]] > ints[1]:
                    prices[ints[0]] = ints[1]
            else:
                prices[ints[0]] = ints[1]
        for line in lines[k+2:]:
            terrain.append([int(x) for x in line.strip().split()][::2])
            countries.append([int(x) for x in line.strip().split()][1::2])

    terrain = np.array(terrain)
    countries = np.array(countries)

    adj_set = set()

    country_border_cell = np.zeros((len(terrain), len(terrain[0])))
    for x in range(len(terrain)):
        for y in range(len(terrain[0])):
            is_border = False
            if x == 0 or y == 0 or x == len(terrain) -1 or y == len(terrain[0])-1:
                is_border = True
            else:
                other = [countries[x-1][y], countries[x][y-1], countries[x][y+1], countries[x+1][y]]
                for other_c in other:
                    if other_c != country:
                        is_border = True
                        adj_set.add((country, other_c))
            if is_border:
                country_border_cell[x][y] = 1

            country = countries[x][y]
            if country not in country_sum_x:
                country_sum_x[country] = [x]
            else:
                country_sum_x[country] += [x]
            if country not in country_sum_y:
                country_sum_y[country] = [y]
            else:
                country_sum_y[country] += [y]
    #print(floor())
    #print(country_border_counts)
    max_countries = max(country_sum_x.keys())
    #print(country_sum_x)
    #print(country_sum_y)
    res = [((np.average(country_sum_y[i])), (np.average(country_sum_x[i]))) for i in sorted(country_sum_x.keys())]
    new_centers = []
    for c in sorted(country_sum_x.keys()):
        capital_y, capital_x = res[c]
        capital = (capital_y, capital_x)
        min_dist = 100000000000
        int_capital_x, int_capital_y = math.floor(capital_x), math.floor(capital_y)
        if c == countries[int_capital_x][int_capital_y] and country_border_cell[int_capital_x][int_capital_y] == 0:
            new_centers.append(capital)
            continue
        for x in range(len(terrain)):
            for y in range(len(terrain[0])):
                if countries[x][y] == c and country_border_cell[x, y] == 0:
                    dist = (x-int_capital_x)**2 + (y-int_capital_y)**2
                    if dist < min_dist:
                        min_dist = dist
                        capital = (y,x)
        new_centers.append(capital)
        print("{}, {} -> {}, {}".format(capital_x, capital_y, capital[1], capital[0]))

    n_countries = len(country_sum_x.keys())
    adj = np.identity(n_countries)

    for a,b in adj_set:
        adj[a][b] = 1
        adj[b][a] = 1


    prices_list = []
    for i in range(n_countries):
        if i in prices:
            prices_list.append(prices[i])
        else:
            prices_list.append(np.inf)
    
    prices = np.full((n_countries, n_countries), np.inf)
    for a in range(n_countries):
        prices[a][a] = prices_list[a]
    #prices = np.diag([for x in prices_list])
    print(prices)

    dist = np.full((n_countries, n_countries), np.inf)
    for a in range(n_countries):
        for b in range(n_countries):
            if adj[a][b] == 1:
                dist[a][b] = math.floor(np.linalg.norm(np.array(new_centers[a])- np.array(new_centers[b])))

    print(dist)

    for fail in range(100):
        for a in range(n_countries):
            for b in range(n_countries):
                for c in range(n_countries):
                    prices[b][c] = min(prices[b][c], dist[a][b] + dist[a][c] + prices[c][a])
    print(prices)


    return new_centers

for inf, outf in zip(files, outfiles):
    res = run(inf)
    print(res)
    with open(outf, "w") as f:
        f.write("\n".join([' '.join(' '.join([str(z) for z in y]) for y in x) for x in res]))
