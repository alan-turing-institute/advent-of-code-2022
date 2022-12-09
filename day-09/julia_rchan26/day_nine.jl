using DelimitedFiles
using Test

test_input = readdlm("test_input.txt")
input = readdlm("input.txt")
test_input_part_two = readdlm("test_input_part_two.txt")

function is_touching(H_location::Tuple{Int64, Int64}, T_location::Tuple{Int64, Int64})
    if H_location==T_location
        # H covers T
        return true
    elseif H_location[1]==T_location[1]
        # same row
        if abs(H_location[2]-T_location[2]) > 1
            return false
        else
            return true
        end
    elseif H_location[2]==T_location[2]
        # same column
        if abs(H_location[1]-T_location[1]) > 1
            return false
        else
            return true
        end
    elseif H_location[1]!=T_location[1] && H_location[2]!=T_location[2]
        # not in the same row or column, need to move diagonally
        if abs(H_location[1]-T_location[1]) > 1 || abs(H_location[2]-T_location[2]) > 1
            return false
        else
            return true
        end
    end
end

function move(location::Tuple{Int64, Int64}, move::Char)
    if move == 'R'
        return (location[1]+1, location[2])
    elseif move == 'L'
        return (location[1]-1, location[2])
    elseif move == 'U'
        return (location[1], location[2]+1)
    elseif move == 'D'
        return (location[1], location[2]-1)
    else
        throw(error("unrecognised move instruction"))
    end
end

##### Part One

#=
Notes:
I've left my solution for Part One here even though it does not work for Part Two.
My Part Two solution, however, can be used for both parts.

The only key difference is that my Part One solution updated the tail by using the
move instruction. This works for a rope of length 2, as it can tell you how to move diagonally.
It is not a nice solution though...

Alternatively, you can just update the tail location by looking at the difference
in the x and y coordinates to the head. This makes it easier to extend to 
rope lengths > 2, as we need for Part Two.

I've used Julia's multiple dispatch to have an alternative update_T_location function
which does not use the move instruction.
=#

function obtain_diagonal_moves(move::Char)
    if move == 'U' || move == 'D'
        return ('L', 'R')
    elseif move == 'R' || move == 'L'
        return ('U', 'D')
    else
        throw(error("unrecognised move instruction"))
    end
end

function update_T_location(H_location::Tuple{Int64, Int64}, T_location::Tuple{Int64, Int64}, move_instruction::Char)
    # uses move_instruction
    if ~is_touching(H_location, T_location)
        T_placeholder = move(T_location, move_instruction)
        if H_location[1]!=T_location[1] && H_location[2]!=T_location[2]
            # aren't in same row or column, need to step diagonally
            # obtain the two possible directions to make it diagonal
            # can't just look at previous move as can have cases where moved U then D
            diagonal_moves = obtain_diagonal_moves(move_instruction)
            if is_touching(H_location, move(T_placeholder, diagonal_moves[1]))
                T_placeholder = move(T_placeholder, diagonal_moves[1])
            elseif is_touching(H_location, move(T_placeholder, diagonal_moves[2]))
                T_placeholder = move(T_placeholder, diagonal_moves[2])
            end
        end
        if is_touching(H_location, T_placeholder)
            T_location = T_placeholder
        else
            throw(error("moving current T_location in $(move_instruction) direction,
                    or moving current T_location in a diagonal move"))
        end
    end
    return T_location
end

function part_one(input)
    H_location = T_location = (1,1)
    visited = Vector{Tuple{Int64,Int64}}()
    for i ∈ 1:size(input)[1]
        move_instruction = only(input[i,1])
        for rep ∈ 1:input[i,2]
            H_location = move(H_location, move_instruction)
            # difference is that I updated my T location using the move_instruction
            # rather than just figuring out *how* I needed to update it...
            T_location = update_T_location(H_location, T_location, move_instruction)
            if T_location ∉ visited
                push!(visited, T_location)
            end
        end
    end
    return size(visited)[1]
end

Test.@test part_one(test_input) == 13

##### Part Two

function update_T_location(H_location::Tuple{Int64, Int64}, T_location::Tuple{Int64, Int64})
    # does not use move_instruction
    if ~is_touching(H_location, T_location)
        x_diff = H_location[1] - T_location[1]
        y_diff = H_location[2] - T_location[2]
        if max(abs(x_diff), abs(y_diff)) > 1
            x = x_diff > 0 ? T_location[1]+1 : x_diff < 0 ? T_location[1]-1 : T_location[1]
            y = y_diff > 0 ? T_location[2]+1 : y_diff < 0 ? T_location[2]-1 : T_location[2]
            T_location = (x, y)
        end
    end
    return T_location
end

function part_two(input, rope_length::Int64)
    rope = [(1,1) for _ in 1:rope_length]
    visited = Vector{Tuple{Int64,Int64}}()
    for i ∈ 1:size(input)[1]
        move_instruction = only(input[i,1])
        for rep ∈ 1:input[i,2]
            # update head location
            rope[1] = move(rope[1], move_instruction)
            # update rest of the rope locations
            for r ∈ 2:rope_length
                rope[r] = update_T_location(rope[r-1], rope[r])
            end
            if rope[end] ∉ visited
                push!(visited, rope[end])
            end
        end
    end
    return size(visited)[1]
end

# testing cases
Test.@test part_two(test_input, 2) == 13
Test.@test part_two(test_input_part_two, 10) == 36

# Part One
println("Part One (using part_one): ", part_one(input))
println("Part One (using part_two): ", part_two(input, 2))

# Part Two
println("Part Two: ", part_two(input, 10))