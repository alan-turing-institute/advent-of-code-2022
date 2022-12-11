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
    monkeys = Dict()
    for i in indices
        monkey_number = parse(Int64, split(split(lines[i], "Monkey ")[2], ":")[1])
        items = parse.(Int64, split(split(lines[i+1], "Starting items: ")[2], ", "))
        operation_line = split(split(lines[i+2], "Operation: new = old ")[2], " ")
        operation = Operation(operation_line[1], operation_line[2])
        test_div = parse(Int64, split(lines[i+3], "Test: divisible by ")[2])
        true_to = parse(Int64, split(lines[i+4], "If true: throw to monkey ")[2])
        false_to = parse(Int64, split(lines[i+5], "If false: throw to monkey ")[2])
        m = Monkey(items, 0, operation, test_div, true_to, false_to)
        mergewith!(+, monkeys, Dict(monkey_number => m))
    end
    return monkeys
end

function perform_rounds(monkeys::Dict{Int64, Monkey}, n_rounds::Int64, part_one::Bool)::Dict{Int64, Monkey}
    for _ in 1:n_rounds
        # compute lowest common multiplier if doing Part Two
        if ~part_one
            val = lcm([monkeys[i].test_div for i in eachindex(monkeys)])
        end
        for i in sort(collect(keys(monkeys)))
            # determine how many items the monkey will inspect this round
            monkeys[i].items_inspected += length(monkeys[i].items)
            # performing operation on the items
            # obtaining the magnitude to multiply or add
            if monkeys[i].operation.mag == "old"
                mag = monkeys[i].items
            else
                m = parse(Int64, monkeys[i].operation.mag)
                mag = repeat([m], length(monkeys[i].items))
            end
            # perform multiplication or addition to worry levels
            if monkeys[i].operation.op == "*"
                monkeys[i].items = monkeys[i].items .* mag
            elseif monkeys[i].operation.op == "+"
                monkeys[i].items = monkeys[i].items .+ mag
            end
            # worry management!!!
            if part_one
                monkeys[i].items = monkeys[i].items .÷ 3
            else
                monkeys[i].items = monkeys[i].items .% val
            end
            # perform test on each item to see where to throw
            for j in eachindex(monkeys[i].items)
                if mod(monkeys[i].items[j], monkeys[i].test_div) == 0
                    push!(monkeys[monkeys[i].true_to].items, monkeys[i].items[j])
                else
                    push!(monkeys[monkeys[i].false_to].items, monkeys[i].items[j])
                end
            end
            # empty items
            monkeys[i].items = Vector{Int64}[]
        end
    end
    return monkeys
end

function day_eleven(input_file::String, n_rounds::Int64, part_one::Bool)::Int64
    monkeys = parse_input(input_file)
    monkeys = perform_rounds(monkeys, n_rounds, part_one)
    items_inspected = [monkeys[i].items_inspected for i in collect(keys(monkeys))]
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