using Test

function parse_input(input_file)
    # evaluate each line
    eval_input = eval.(Meta.parse.(readlines(input_file)))
    # remove nothing items
    return eval_input[map(!, isnothing.(eval_input))]
end

test_input = parse_input("test_input.txt")
input = parse_input("input.txt")

function compare_packets(packet1::Union{Vector, Int64},
                         packet2::Union{Vector, Int64})::Union{Nothing, Bool}
    # recursively compare packets
    if typeof(packet1) == Int64 && typeof(packet2) == Int64
        # both integers, so can compare directly
        if packet1 == packet2
            # does not determine if left side is smaller or not
            return nothing
        else
            # determine if left side is smaller or not
            return packet1 < packet2
        end
    elseif typeof(packet1) == Int64 && typeof(packet2) != Int64
        # packet1 is integer, but packet2 is list, so make packet1 a list
        packet1 = [packet1]
    elseif typeof(packet1) != Int64 && typeof(packet2) == Int64
        # packet2 is integer, but packet1 is list, so make packet2 a list
        packet2 == [packet2]
    end
    to_index = max(length(packet1), length(packet2))
    for i in 1:to_index
        if i > length(packet1)
            # left side ran out of items, items are in order
            return true
        elseif i > length(packet2)
            # right side ran out of items, items are not in order
            return false
        end
        # compare packet1[i] and packet2[i]
        comp = compare_packets(packet1[i], packet2[i])
        if !isnothing(comp)
            return comp
        end
    end
end

function part_one(input)::Int64
    return sum([i*compare_packets(input[2*i-1], input[2*i]) for i in 1:(length(input)÷2)])
end

function part_two(input)::Int64
    # take a copy so that it doesn't affect the input
    input_copy = deepcopy(input)
    push!(input_copy, [[2]], [[6]])
    # sort by comparing packets
    sorted = sort!(input_copy, lt=compare_packets)
    indices = findall(x -> x==[[2]] || x==[[6]], sorted)
    if length(indices) > 2
        throw(error("there should be only two items equal to [[2]] and [[6]]"))
    else
        return prod(indices)
    end
end

# testing cases
Test.@test part_one(test_input) == 13
Test.@test part_two(test_input) == 140

# Part One
println("Part One: ", part_one(input))

# Part Two
println("Part Two: ", part_two(input))