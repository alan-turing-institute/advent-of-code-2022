using Test

test_input = readlines("test_input.txt")
input = readlines("input.txt")

function priority(char)
    if islowercase(char)
        return Int(char) + 1 - Int('a')
    else
        return Int(char) + 27 - Int('A')
    end
end

function part_one(input) 
    sum = 0
    for item in input
        n = length(item)
        first = item[1:(n÷2)]
        second = item[((n÷2)+1):n]
        common_letter = only(filter(x -> x ∈ split(second, ""), split(first, ""))[1])
        sum += priority(common_letter)
    end
    return sum
end

function obtain_groups(input)
    groups = Any[]
    for g in 1:(length(input)÷3)
        append!(groups, [input[(3*(g-1)+1):(3*g)]])
    end
    return groups
end

function part_two(input)
    sum = 0
    for group in obtain_groups(input)
        priorities = [map(c -> priority(only(c)), split(rucksack, ""))
            for rucksack in group]
        intersection = intersect(priorities[1], priorities[2], priorities[3])
        sum += intersection[1]
    end
    return sum
end

# testing cases
Test.@test part_one(test_input) == 157
Test.@test part_two(test_input) == 70

# Part One
println("Part One: ", part_one(input))

# Part Two
println("Part Two: ", part_two(input))