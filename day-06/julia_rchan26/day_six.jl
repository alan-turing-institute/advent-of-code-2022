using Test

test_input = readlines("test_input.txt")
input = readlines("input.txt")[1]

function decode_signal(input, n_unique)    
    position = n_unique-1
    unique = 0
    while (unique != n_unique)
        position += 1
        unique = length(Set(input[(position-n_unique+1):position]))
    end
    return position, input[(position-n_unique+1):position]
end

# testing cases for Part One
Test.@test decode_signal(test_input[1], 4) == (7, "jpqm")
Test.@test decode_signal(test_input[2], 4) == (5, "vwbj")
Test.@test decode_signal(test_input[3], 4) == (6, "pdvj")
Test.@test decode_signal(test_input[4], 4) == (10, "rfnt")
Test.@test decode_signal(test_input[5], 4) == (11, "zqfr")

# testing cases for Part Two
Test.@test decode_signal(test_input[1], 14) == (19, "qmgbljsphdztnv")
Test.@test decode_signal(test_input[2], 14) == (23, "vbhsrlpgdmjqwf")
Test.@test decode_signal(test_input[3], 14) == (23, "ldpwncqszvftbr")
Test.@test decode_signal(test_input[4], 14) == (29, "wmzdfjlvtqnbhc")
Test.@test decode_signal(test_input[5], 14) == (26, "jwzlrfnpqdbhtm")

# Part One
println("Part One: ", decode_signal(input, 4))

# Part Two
println("Part Two: ", decode_signal(input, 14))