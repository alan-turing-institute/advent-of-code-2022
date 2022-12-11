using Test

struct Operation
    op::String
    mag::String
end

mutable struct Monkey
    items::Vector{Int64}
    items_inspected::Int64
    operation::Operation
    test_div::Int64
    true_to::Int64
    false_to::Int64
end

function parse_input(input_file::String)::Dict{Int64, Monkey}
    # returns a dictionary where keys are monkey index and values are Monkey structs
    lines = readlines(input_file)
    indices = filter(i -> startswith(lines[i], "Monkey "), eachindex(lines))
    🐵🐵 = Dict()
    for i in indices
        monkey_number = parse(Int64, split(split(lines[i], "Monkey ")[2], ":")[1])
        items = parse.(Int64, split(split(lines[i+1], "Starting items: ")[2], ", "))
        operation_line = split(split(lines[i+2], "Operation: new = old ")[2], " ")
        operation = Operation(operation_line[1], operation_line[2])
        test_div = parse(Int64, split(lines[i+3], "Test: divisible by ")[2])
        true_to = parse(Int64, split(lines[i+4], "If true: throw to monkey ")[2])
        false_to = parse(Int64, split(lines[i+5], "If false: throw to monkey ")[2])
        m = Monkey(items, 0, operation, test_div, true_to, false_to)
        mergewith!(+, 🐵🐵, Dict(monkey_number => m))
    end
    return 🐵🐵
end

function perform_rounds(🐵🐵::Dict{Int64, Monkey}, n_rounds::Int64, part_one::Bool)::Dict{Int64, Monkey}
    # compute lowest common multiplier if doing Part Two
    if ~part_one
        val = lcm([🐵🐵[i].test_div for i in eachindex(🐵🐵)])
    end
    for _ in 1:n_rounds
        for i in sort(collect(keys(🐵🐵)))
            # determine how many items the monkey will inspect this round
            🐵🐵[i].items_inspected += length(🐵🐵[i].items)
            # performing operation on the items
            # obtaining the magnitude to multiply or add
            if 🐵🐵[i].operation.mag == "old"
                mag = 🐵🐵[i].items
            else
                m = parse(Int64, 🐵🐵[i].operation.mag)
                mag = repeat([m], length(🐵🐵[i].items))
            end
            # perform multiplication or addition to worry levels
            if 🐵🐵[i].operation.op == "*"
                🐵🐵[i].items = 🐵🐵[i].items .* mag
            elseif 🐵🐵[i].operation.op == "+"
                🐵🐵[i].items = 🐵🐵[i].items .+ mag
            end
            # worry management!!!
            if part_one
                🐵🐵[i].items = 🐵🐵[i].items .÷ 3
            else
                🐵🐵[i].items = 🐵🐵[i].items .% val
            end
            # perform test on each item to see where to throw
            for j in eachindex(🐵🐵[i].items)
                if mod(🐵🐵[i].items[j], 🐵🐵[i].test_div) == 0
                    push!(🐵🐵[🐵🐵[i].true_to].items, 🐵🐵[i].items[j])
                else
                    push!(🐵🐵[🐵🐵[i].false_to].items, 🐵🐵[i].items[j])
                end
            end
            # empty items
            🐵🐵[i].items = Vector{Int64}[]
        end
    end
    return 🐵🐵
end

function day_eleven(input_file::String, n_rounds::Int64, part_one::Bool)::Int64
    🐵🐵 = parse_input(input_file)
    🐵🐵 = perform_rounds(🐵🐵, n_rounds, part_one)
    items_inspected = [🐵🐵[i].items_inspected for i in collect(keys(🐵🐵))]
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