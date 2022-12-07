using Test

test_input = readlines("test_input.txt")
input = readlines("input.txt")

function find_dir_sizes(input)
    paths = []
    sizes = Dict{String,Int64}()
    for line ∈ input
        if startswith(line, "\$ cd ..")
            # move back a directory
            pop!(paths)
        elseif startswith(line, "\$ cd ")
            # append the next directory
            directory = split(line, "\$ cd ")[2]
            if directory == "/"
                push!(paths, "~")
            else
                push!(paths, "$(last(paths))/$(directory)")
            end
        elseif isdigit(line[1])
            # add size of file to all paths
            size = parse(Int64, split(line, " ")[1])
            mergewith!(+, sizes, Dict(path => size for path ∈ paths))
        end
    end
    return sizes
end

function part_one(input)
    sizes = find_dir_sizes(input)
    return sum(filter(x -> x <= 100000, collect(values(sizes))))
end

function part_two(input)
    sizes = find_dir_sizes(input)
    total_space = 70000000
    required = 30000000
    unused = total_space-sizes["~"]
    return minimum(filter(x -> x > required-unused, collect(values(sizes))))
end

# testing find_dir_sizes
test_input_sizes = find_dir_sizes(test_input)
Test.@test test_input_sizes["~"] == 48381165
Test.@test test_input_sizes["~/d"] == 24933642
Test.@test test_input_sizes["~/a"] == 94853
Test.@test test_input_sizes["~/a/e"] == 584

# testing cases
Test.@test part_one(test_input) == 95437
Test.@test part_two(test_input) == 24933642

# Part One
println("Part One: ", part_one(input))

# Part Two
println("Part Two: ", part_two(input))