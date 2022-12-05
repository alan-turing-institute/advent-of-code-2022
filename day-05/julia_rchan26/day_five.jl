using Test

test_input = readlines("test_input.txt")
input = readlines("input.txt")

function read_input(input)
    # obtaining the stacks
    # stores in a dictionary {1: [A, B, C], 2: [D, E], ...} 
    # where the first elements in the vectors correspond to the top of the stack
    stacks = Dict(name => [] for name in 1:number_of_stacks)
    index_of_stacks_row = findfirst(x -> '1' in x, input)
    stacks_row = input[index_of_stacks_row]
    number_of_stacks = maximum(parse.(Int64, split(filter(isdigit, stacks_row), "")))
    for i in 1:number_of_stacks
        # index of the string which contains the letters for current stack
        index = 4*i-2
        stack = [input[j][index] for j in 1:(index_of_stacks_row-1)]
        # removing any empty strings
        filtered_stack = filter(x -> isletter(x), stack)
        stacks[i] = [stacks[i]; filtered_stack]
    end
    # obtaining the instructions
    instructions = split.(input[index_of_stacks_row+2:end], " ")
    return stacks, instructions
end

function perform_moves(stacks, instructions, part_one)
    for inst in instructions
        num_to_move, from, to = parse.(Int64, inst[[2,4,6]])
        items_to_move = stacks[from][1:num_to_move]
        if part_one
            # CrateMover 9000: moves one at a time and needs reverse
            items_to_move = reverse(items_to_move)
        end
        stacks[to] = [items_to_move; stacks[to]]
        deleteat!(stacks[from], 1:num_to_move)
    end
    return stacks
end

function day_five(input, part_one)
    stacks, instructions = read_input(input)
    updated_stack = perform_moves(stacks, instructions, part_one)
    top_crates = join([updated_stack[i][1] for i in 1:length(updated_stack)])
    return top_crates
end

# testing cases
Test.@test day_five(test_input, true) == "CMZ"
Test.@test day_five(test_input, false) == "MCD"

# Part One
println("Part One: ", day_five(input, true))

# Part Two
println("Part Two: ", day_five(input, false))