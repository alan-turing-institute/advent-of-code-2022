using Test
using DelimitedFiles

test_input = readdlm("test_input.txt")
input = readdlm("input.txt")

function part_one(input, interesting_cycles::Vector{Int64})
    signal_strengths = Vector{Int64}()
    cycle_lengths = [x == "addx" ? 2 : 1 for x in input[:,1]]
    cycle_length_cumsum = cumsum(cycle_lengths)
    for target_cycle in interesting_cycles
        index = findfirst(i -> i>=target_cycle, cycle_length_cumsum)-1
        value = sum([x for x in input[1:index,2] if x!=""])+1
        push!(signal_strengths, target_cycle * value)
    end
    return sum(signal_strengths), signal_strengths
end

function part_two(input; ncol::Int64 = 40)
    cycle_lengths = [x == "addx" ? 2 : 1 for x in input[:,1]]
    grid = reshape([' ' for i in 1:sum(cycle_lengths)],
                    sum(cycle_lengths)÷ncol, ncol)
    grid_i = grid_j = 1
    value = 1
    # indices in Julia start from 1
    # so value gives the start index rather than middle index
    sprite_position = value:(value+2) 
    for i in eachindex(cycle_lengths)
        for _ in 1:cycle_lengths[i]
            # fill in grid depending on if current index is in sprite
            grid[grid_i, grid_j] = grid_j in sprite_position ? '#' : '.'
            grid_j += 1
            if grid_j > ncol
                # move to next line in grid
                grid_i += 1
                grid_j = 1
            end
        end
        if input[i,1] == "addx"
            # update value and sprite position
            value += input[i,2]
            sprite_position = value:(value+2) 
        end
    end
    # concatenate characters in each row
    CRT_drawing = [join(grid[i,:]) for i in 1:size(grid)[1]]
    return CRT_drawing 
end

# testing cases for Part One
test_part_one = part_one(test_input, [20, 60, 100, 140, 180, 220])
Test.@test test_part_one[1] == 13140
Test.@test test_part_one[2] == [420, 1140, 1800, 2940, 2880, 3960]

# testing cases for Part Two
test_part_two = part_two(test_input)
Test.@test test_part_two[1] == "##..##..##..##..##..##..##..##..##..##.."
Test.@test test_part_two[2] == "###...###...###...###...###...###...###."
Test.@test test_part_two[3] == "####....####....####....####....####...."
Test.@test test_part_two[4] == "#####.....#####.....#####.....#####....."
Test.@test test_part_two[5] == "######......######......######......####"
Test.@test test_part_two[6] == "#######.......#######.......#######....."

# Part One
println("Part One: ", part_one(input, [20, 60, 100, 140, 180, 220])[1])

# Part Two
part_two_solution = part_two(input)
println("Part Two:")
for row in part_two_solution
    println(row)
end