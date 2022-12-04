using Test

test_input = split.(readlines("test_input.txt"), ",")
input = split.(readlines("input.txt"), ",")

range_contained(r1, r2) = (r1[begin] ∈ r2) && (r1[end] ∈ r2)
part_one_cond(r1, r2) = range_contained(r1, r2) || range_contained(r2, r1)
part_two_cond(r1, r2) = length(intersect(Set(r1), Set(r2))) > 0

function day_four(input, part::Function)
    sum = 0
    for row in eachrow(input)
        e1 = parse.(Int64, split(row[1][1], "-"))
        elf_1_range = e1[1]:e1[2]
        e2 = parse.(Int64, split(row[1][2], "-"))
        elf_2_range = e2[1]:e2[2]
        if part(elf_1_range, elf_2_range)
            sum += 1
        end
    end
    return sum
end

# tesing cases
Test.@test day_four(test_input, part_one_cond) == 2
Test.@test day_four(test_input, part_two_cond) == 4

# Part One
println("Part One: ", day_four(input, part_one_cond))

# Part Two
println("Part Two: ", day_four(input, part_two_cond))