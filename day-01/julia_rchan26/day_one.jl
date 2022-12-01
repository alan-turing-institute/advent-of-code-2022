using Test

test_input = readlines("test_input.txt")
input = readlines("input.txt")

function obtain_elves_calories(input)
    elves_calories = zeros(Int64, count(i->(i==""), input)+1)
    elf = 1
    for line in input
        if line == ""
            elf += 1
        else
            elves_calories[elf] += parse(Int64, line)
        end
    end
    return elves_calories
end

function maximum_calories(input)
    return maximum(obtain_elves_calories(input))
end
    
function sum_top_elves(input, count = 3)
    return sum(sort(obtain_elves_calories(input), rev=true)[1:count])
end

# testing cases
Test.@test maximum_calories(test_input) == 24000
Test.@test sum_top_elves(test_input) == 45000

# Part One
println("Part One: ", maximum_calories(input))

# Part Two
println("Part Two: ", sum_top_elves(input))