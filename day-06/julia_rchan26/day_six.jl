using Test

test_input = readlines("test_input.txt")
input = readlines("input.txt")[1]

function detect_signal(input, n_unique)    
    position = n_unique
    while (length(Set(input[(position-n_unique+1):position])) != n_unique)
        position += 1
    end
    return position, input[(position-n_unique+1):position]
end

# testing cases for Part One
Test.@test detect_signal(test_input[1], 4) == (7, "jpqm")
Test.@test detect_signal(test_input[2], 4) == (5, "vwbj")
Test.@test detect_signal(test_input[3], 4) == (6, "pdvj")
Test.@test detect_signal(test_input[4], 4) == (10, "rfnt")
Test.@test detect_signal(test_input[5], 4) == (11, "zqfr")

# testing cases for Part Two
Test.@test detect_signal(test_input[1], 14) == (19, "qmgbljsphdztnv")
Test.@test detect_signal(test_input[2], 14) == (23, "vbhsrlpgdmjqwf")
Test.@test detect_signal(test_input[3], 14) == (23, "ldpwncqszvftbr")
Test.@test detect_signal(test_input[4], 14) == (29, "wmzdfjlvtqnbhc")
Test.@test detect_signal(test_input[5], 14) == (26, "jwzlrfnpqdbhtm")

# Part One
println("Part One: ", detect_signal(input, 4))

# Part Two
println("Part Two: ", detect_signal(input, 14))