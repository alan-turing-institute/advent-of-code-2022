(* Advent of Code - Day 1

(This year I will try to make the solution understandable to 2023 me)

We're given a multiline string input

Each entry (single number on a line) represents the no. of calories for a single item
Each elf/group (collection of lines, delimited by blank line) represents an Elf's backpack of items

We want to find the elf/group with the highest sum

Assumptions:
- input is line separated integers only (with additional blank lines to delimit elves/groups)
*)
[<Literal>]
let INPUT_FILEPATH = "day-01/fsharp_lannelin/input.txt"
[<Literal>]
let ELF_DELIMITER = "\n\n"
[<Literal>]
let ITEM_DELIMITER = "\n"
[<Literal>]
let N_ELVES_PART_2 = 3 // how many elves we care about in part 2

// short input given to us as part of the challenge to dev against
let debugInput: string = "1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"

// split string representing group into individual items
let parseGroup (group: string) =
    let groupArr: string[] = group.Split ITEM_DELIMITER
    Array.map int groupArr

// take a string input, break into elves, and return list of list of calories
let parseInput (input: string)  = 
    // cleanup any leading or trailing space
    let trimmedInput: string = input.Trim()
    let elves: string[] = trimmedInput.Split ELF_DELIMITER
    Array.map parseGroup elves
    

// answer 1 is simply the elf with the most total calories
// sum each group/elf and find the max
let getAnswer1 (input: string) = 
    let elves: int[][]= parseInput input
    Array.max (Array.map Array.sum elves)

let input: string = System.IO.File.ReadAllText INPUT_FILEPATH

printfn "answer 1 DEBUG: %d ...  should be 24000" (getAnswer1 debugInput)
printfn "answer 1: %d" (getAnswer1 input)

// answer 2 is the sum of the top three elves
// sum each group/elf, find the top 3, and sum those
let getAnswer2 (input : string) = 
    let elves: int[][]= parseInput input
    let summedElves = (Array.map Array.sum elves)
    let bigThree =  (Array.sort summedElves)[(summedElves.Length-N_ELVES_PART_2) .. ]
    Array.sum bigThree


printfn "answer 1 DEBUG: %d ...  should be 45000" (getAnswer2 debugInput)
printfn "answer 1: %d" (getAnswer2 input)