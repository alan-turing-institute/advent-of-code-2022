(* Advent of Code - Day 3
Badly packed backpacks
*)

let INPUT_FILEPATH = "day-03/fsharp_lannelin/input.txt"

// assumes only a-z and A-Z
let charValue c =
    if System.Char.IsLower c then int (c) - 96 else int (c) - 38



let getAnswer1 (input: string) =
    input.Split("\n")
    |> Array.map (fun (lineString: string) ->
        let dividePoint: int = (lineString.Length / 2)
        (Set(lineString[.. dividePoint - 1]), Set(lineString[dividePoint..]))) // divide into two compartment of type Set

    |> Array.map (fun backpack -> backpack ||> Set.intersect) // get shared

    |> Array.map (fun sharedChars -> Set.fold (fun (accum: int) (item: char) -> (charValue item) + accum) 0 sharedChars)

    |> Array.sum



let debugInput: string =
    "vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"


let dayInput: string = (System.IO.File.ReadAllText INPUT_FILEPATH).Trim()

printfn "answer 1 DEBUG: %d ...  should be 157" (getAnswer1 debugInput)

printfn "answer 1: %d" (getAnswer1 dayInput)

let getAnswer2 (input: string) =
    input.Split("\n")
    |> Array.chunkBySize 3
    |> Array.map (fun (lines: string[]) ->
        Array.fold (fun accum (s: string) -> Set.intersect accum (Set(s)))
             (Set(lines[0])) lines[1..])

    |> Array.map Set.maxElement // take the only element (assume just one)
    |> Array.map char
    |> Array.map charValue
    |> Array.sum


printfn "answer 2 DEBUG: %d ...  should be 70" (getAnswer2 debugInput)
printfn "answer 2: %d" (getAnswer2 dayInput)
