using Test

struct Operation
    operation::String
    # String magnitude as it could be "old"
    # e.g. when theoperation is old*old
    magnitude::String
end

mutable struct Monkey
    items::Vector{Int64}
    items_inspected::Int64
    operation::Operation
    test_div::Int64
    true_monkey::Int64
    false_monkey::Int64
end

function parse_input(input_file::String)::Dict{Int64, Monkey}
    # returns a dictionary where keys are monkey index and values are Monkey structs
    lines = readlines(input_file)
    indices = filter(i -> startswith(lines[i], "Monkey "), eachindex(lines))
    monkey_dict = Dict()
    for i in indices
        monkey_number = parse(Int64, split(split(lines[i], "Monkey ")[2], ":")[1])
        items = parse.(Int64, split(split(lines[i+1], "Starting items: ")[2], ", "))
        operation_line = split(split(lines[i+2], "Operation: new = old ")[2], " ")
        operation = Operation(operation_line[1], operation_line[2])
        test_div = parse(Int64, split(lines[i+3], "Test: divisible by ")[2])
        true_monkey = parse(Int64, split(lines[i+4], "If true: throw to monkey ")[2])
        false_monkey = parse(Int64, split(lines[i+5], "If false: throw to monkey ")[2])
        m = Monkey(items, 0, operation, test_div, true_monkey, false_monkey)
        mergewith!(+, monkey_dict, Dict(monkey_number => m))
    end
    return monkey_dict
end

function perform_rounds(monkey_dict::Dict{Int64, Monkey}, n_rounds::Int64, part_one::Bool)::Dict{Int64, Monkey}
    for _ in 1:n_rounds
        # compute lowest common multiplier if doing Part Two
        if ~part_one
            val = lcm([monkey_dict[i].test_div for i in eachindex(monkey_dict)])
        end
        for i in sort(collect(keys(monkey_dict)))
            # determine how many items the monkey will inspect this round
            monkey_dict[i].items_inspected += length(monkey_dict[i].items)
            # performing operation on the items
            # obtaining the magnitude to multiply or add
            if monkey_dict[i].operation.magnitude == "old"
                mag = monkey_dict[i].items
            else
                m = parse(Int64, monkey_dict[i].operation.magnitude)
                mag = repeat([m], length(monkey_dict[i].items))
            end
            # perform multiplication or addition to worry levels
            if monkey_dict[i].operation.operation == "*"
                monkey_dict[i].items = monkey_dict[i].items .* mag
            elseif monkey_dict[i].operation.operation == "+"
                monkey_dict[i].items = monkey_dict[i].items .+ mag
            end
            # worry management!!!
            if part_one
                monkey_dict[i].items = monkey_dict[i].items .÷ 3
            else
                monkey_dict[i].items = monkey_dict[i].items .% val
            end
            # perform test on each item to see where to throw
            for j in eachindex(monkey_dict[i].items)
                if mod(monkey_dict[i].items[j], monkey_dict[i].test_div) == 0
                    push!(monkey_dict[monkey_dict[i].true_monkey].items, monkey_dict[i].items[j])
                else
                    push!(monkey_dict[monkey_dict[i].false_monkey].items, monkey_dict[i].items[j])
                end
            end
            # empty items
            monkey_dict[i].items = Vector{Int64}[]
        end
    end
    return monkey_dict
end

function day_eleven(input_file::String, n_rounds::Int64, part_one::Bool)::Int64
    monkey_dict = parse_input(input_file)
    monkey_dict = perform_rounds(monkey_dict, n_rounds, part_one)
    items_inspected = [monkey_dict[i].items_inspected for i in collect(keys(monkey_dict))]
    # multiply items inspected by two most active monkeys to obtain monkey business level
    return prod(sort(items_inspected)[(end-1):end])
end

# testing cases
Test.@test day_eleven("test_input.txt", 20, true) == 10605
Test.@test day_eleven("test_input.txt", 10000, false) == 2713310158

# Part One
println("Part One: ", day_eleven("input.txt", 20, true))

# Part Two
println("Part Two: ", day_eleven("input.txt", 10000, false))
