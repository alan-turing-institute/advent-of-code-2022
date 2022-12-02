using DelimitedFiles
using Test
test_input = DelimitedFiles.readdlm("test_input.txt")
input = DelimitedFiles.readdlm("input.txt")

opponent_dict = Dict("A" => "R",
    "B" => "P",
    "C" => "S")
you_dict = Dict("X" => "R",
    "Y" => "P",
    "Z" => "S")

function outcome_points(opponent, you)
    # determine the number of points obtained from outcome
    opponent_choice = opponent_dict[opponent]
    you_choice = you_dict[you]
    if opponent_choice == you_choice
        return 3
    end
    if opponent_choice == "R"
        if you_choice == "P"
            return 6
        elseif you_choice == "S"
            return 0
        end
    elseif opponent_choice == "P"
        if you_choice == "R"
            return 0
        elseif you_choice == "S"
            return 6
        end
    elseif opponent_choice == "S"
        if you_choice == "R"
            return 6
        elseif you_choice == "P"
            return 0
        end
    end
end

function shape_select_points(shape)
    # determine the number of points obtained by shape choice
    if shape == "R"
        return 1
    elseif shape == "P"
        return 2
    elseif shape == "S"
        return 3
    else
        throw(error("shape is not 'R', 'P', or 'S'"))
    end
end

function part_one(input)
    points = 0
    for row in eachrow(input)
        points += outcome_points(row[1], row[2])
        points += shape_select_points(you_dict[row[2]])
    end
    return points
end

function decide_shape(opponent_choice, require)
    opponent_shape = opponent_dict[opponent_choice]
    if require == "draw"
        return opponent_shape
    elseif require == "win"
        if opponent_shape == "R"
            return "P"
        elseif opponent_shape == "P"
            return "S"
        elseif opponent_shape == "S"
            return "R"
        end
    elseif require == "loss"
        if opponent_shape == "R"
            return "S"
        elseif opponent_shape == "P"
            return "R"
        elseif opponent_shape == "S"
            return "P"
        end
    else
        throw(error("require is not 'win', 'draw' or 'loss'"))
    end
end

function part_two(input)
    points = 0
    for row in eachrow(input)
        # determine the number of points obtained from outcome
        if row[2] == "X"
            require = "loss"
            points += 0
        elseif row[2] == "Y"
            require = "draw"
            points += 3
        elseif row[2] == "Z"
            require = "win"
            points += 6
        end
        # determine shape to use and number of points obtained by shape choice
        shape_to_use = decide_shape(row[1], require)
        points += shape_select_points(shape_to_use)
    end
    return points
end

# testing cases
Test.@test part_one(test_input) == 15
Test.@test part_two(test_input) == 12

# Part One
println("Part One: ", part_one(input))

# Part Two
println("Part Two: ", part_two(input))