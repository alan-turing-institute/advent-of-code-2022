import copy
import itertools
import time


def parse_input(filename):
    """
    Create:
    - dictionary with valve flow rate and tunnels from each chamber
    - list of chambers with non-zero flow rate valves
    """
    with open(filename) as f:
        lines = f.read().splitlines()
    valves = {}
    non_zero_valves = []
    for line in lines:
        part1, part2 = line.split(";")
        valve_name = part1.split(" has")[0].split(" ")[-1]
        valve_rate = int(part1.split("=")[-1])
        if "valves" in part2:
            tunnels = part2.split(" valves ")[-1].split(", ")
        else:
            tunnels = part2.split(" valve ")[-1].split(", ")
        valves[valve_name] = {}
        valves[valve_name]["rate"] = valve_rate
        valves[valve_name]["tunnels"] = tunnels
        if valve_rate != 0:
            non_zero_valves.append(valve_name)
    return valves, non_zero_valves


def find_shortest_path(v1, v2, valves):
    """
    Find shortest path between 2 valves.
    """
    stack = [(v1,0,[])]
    shortest = 100
    while len(stack) != 0:
        v, dist, visited = stack.pop()
        if v == v2:
            shortest = min(shortest, dist)
        for child in valves[v]["tunnels"]:
            if child not in visited:
                stack.append((child, dist+1, visited+[v]))
    return shortest


def construct_graph(valve_names, valves):
    """
    Construct graph with shortest distances between named valves.
    Use to get graph of paths between all chambers with non-zero 
    valves + start chamber.
    """
    graph = {name:{} for name in valve_names}
    for v1, v2 in itertools.combinations(valve_names, 2):
        dist = find_shortest_path(v1, v2, valves)
        graph[v1][v2] = dist
        graph[v2][v1] = dist
    return graph


def get_max_pressure(n_steps, graph, all_valves):
    """
    Depth First Serch. Get max pressure one can release 
    given `n_steps` and graph.

    `all_valves`: dictionary of valve flow rates
    `graph`: distances between chambers to explore
    """

    # track: (chamber name/steps renaming/indicator of valves open so far/total_pressure)
    # add 1 to `n_steps` for initial move into chamber AA (the start pos) 
    stack = [("AA", n_steps+1, {valve:0 for i,valve in enumerate(list(graph.keys()))} , 0)] 
    max_pressure = 0

    while len(stack) != 0:

        # move into new chamber
        chamber, steps_remaining, is_open, tot_pressure = stack.pop()
        
        # open valve and update data
        is_open[chamber] = 1
        steps_remaining -= 1
        tot_pressure += (all_valves[chamber]["rate"] * steps_remaining)
        
        # move to another chamber (if have enough moves left & the valve there isn't open yet)
        for child, dist in graph[chamber].items():
            if steps_remaining - dist > 0 and is_open[child] == 0:
                stack.append((child, steps_remaining-dist, copy.deepcopy(is_open), tot_pressure))
            else:
                max_pressure = max(tot_pressure, max_pressure)
            
    return max_pressure


# PARSE INPUT =========================================================================================
all_valves, non_zero_valves = parse_input("input16.txt")


# PART 1:  ============================================================================================
# what is max pressure that can accumulate in 30 steps?

start_time = time.time()

# construct graph of distances between all non-0 valve chambers & start chamber
graph = construct_graph(non_zero_valves + ["AA"], all_valves)

# run all possible orders of opening those valves - return the best
max_pressure = get_max_pressure(30, graph, all_valves)
print("Part 1:", max_pressure)

seconds = time.time() - start_time
print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))


# PART 2 ===============================================================================================
# there are now 2 agents (you+elephant), starting in the same chamber with 26 minutes each
# - what is max pressure that can be released with both opening valves?
# !!!! THIS CODE TAKES 3 HOURS TO COMPLETE !!!!

start_time = time.time()

max_pressure = 0
# create all possible partitions of chambers between the two agents 
# construct graphs and get max pressure for each separately, then sum
splits = [v for a in range(len(non_zero_valves)) for v in itertools.combinations(non_zero_valves, a)]
for i in range(len(splits)//2 + 1):
    v1 = list(itertools.chain(splits[i]))
    v2 = [e for e in non_zero_valves if e not in splits[i]]
    
    # NOTE: we create all possible splits above but only look at even splits 
    # (this is 7/8 chamber split since there are 15 non-zero valves)
    if len(v1) != 7:
        continue
    
    graph1 = construct_graph(v1 + ["AA"], all_valves)
    graph2 = construct_graph(v2 + ["AA"], all_valves)
    pressure1 = get_max_pressure(26, graph1, all_valves)
    pressure2 = get_max_pressure(26, graph2, all_valves)
    max_pressure = max(max_pressure, pressure1 + pressure2)
    
    # check intermediate results and time take so far
    print(v1, v2)
    print(max_pressure)
    seconds = time.time() - start_time
    print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))

print("Part 2:", max_pressure)

seconds = time.time() - start_time
print('Time Taken:', time.strftime("%H:%M:%S", time.gmtime(seconds)))
