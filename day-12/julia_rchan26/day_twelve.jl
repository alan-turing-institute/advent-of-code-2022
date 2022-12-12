using Test

function parse_input(file::String)::Matrix{Char}
    # parse input as a Matrix
    vec_of_vec = [only.(x) for x in split.(readlines(file), "")]
    return mapreduce(permutedims, vcat, vec_of_vec)
end

test_input = parse_input("test_input.txt")
input = parse_input("input.txt")

function find_start_end(grid::Matrix{Char};
                        all_possible_starts::Bool=false)::Tuple{Vector{CartesianIndex},CartesianIndex}
    # finds the start and end by identifying 'S' and 'E'
    S_loc = findall(x -> x == 'S', grid)
    E_loc = findall(x -> x == 'E', grid)
    if all_possible_starts
        start_locs = vcat(findall(x -> x == 'S', grid),
            findall(x -> x == 'a', grid))
        return start_locs, E_loc[1]
    else
        return S_loc, E_loc[1]
    end
end

function grid_values(grid::Matrix{Char},
                     start_index::CartesianIndex,
                     end_index::CartesianIndex)::Matrix{Char}
    # converts the 'S' and 'E' to 'a' and 'z' respectively
    # returns a modified deepcopy of the grid
    updated_grid = deepcopy(grid)
    updated_grid[start_index] = updated_grid[start_index] == 'S' ? 'a' : updated_grid[start_index]
    updated_grid[end_index] = updated_grid[end_index] == 'E' ? 'z' : updated_grid[end_index]
    return updated_grid
end

function find_possible_neighbours(point::CartesianIndex,
                                  grid::Matrix{Char})::Vector{CartesianIndex}
    nrow, ncol = size(grid)
    neighbours = CartesianIndex.([(point[1] - 1, point[2]),
        (point[1] + 1, point[2]),
        (point[1], point[2] - 1),
        (point[1], point[2] + 1)])
    # check if still within grid edges
    valid_neighbours = [x for x in neighbours if (1 <= x[1] <= nrow) && (1 <= x[2] <= ncol)]
    # only return neighbours which are at most one higher
    return [x for x in valid_neighbours if (grid[x] - grid[point]) <= 1]
end

function dijkstra(start_index::CartesianIndex,
                  end_index::CartesianIndex,
                  grid::Matrix{Char})::Dict{String,Any}
    visited = falses(size(grid))
    cost = fill(Inf, size(grid))
    cost[start_index] = 0
    updated_grid = grid_values(grid, start_index, end_index)
    while ~all(visited)
        min_cost_unvisited = findall(x -> x == minimum(cost[map(!, visited)]), cost)
        coord = min_cost_unvisited[findfirst(!visited[x] for x in min_cost_unvisited)]
        if coord == end_index
            return Dict("cost" => cost, "cost_to_end" => cost[coord])
        end
        visited[coord] = true
        neighbours = find_possible_neighbours(coord, updated_grid)
        for nb in neighbours
            if ~visited[nb]
                alt = cost[coord] + 1
                if alt < cost[nb]
                    cost[nb] = alt
                end
            end
        end
    end
    return Dict("cost" => cost, "cost_to_end" => cost[coord])
end

function day_twelve(grid::Matrix{Char},
                    part_one::Bool)::Int64
    start_index, end_index = find_start_end(grid, all_possible_starts=~part_one)
    if part_one
        return Int64(dijkstra(start_index[1], end_index, grid)["cost_to_end"])
    else
        println("applying dijkstra to $(length(start_index)) possible start points")
        println("solving with $(Threads.nthreads()) threads!")
        path_lengths = []
        Threads.@threads for start in start_index
            length_to_end = dijkstra(start, end_index, grid)["cost_to_end"]
            println("- thread: $(Threads.threadid()) || start: $(start) || path_length: $(length_to_end)")
            push!(path_lengths, length_to_end)
        end
        return Int64(minimum(path_lengths))
    end
end

# testing cases
Test.@test day_twelve(test_input, true) == 31
Test.@test day_twelve(test_input, false) == 29

# Part One
println("Part One: ", day_twelve(input, true))
println("Part Two: ", day_twelve(input, false))