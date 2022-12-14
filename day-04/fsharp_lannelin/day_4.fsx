(* Advent of Code - Day 4
assignment - detecting overlaps
*)

let INPUT_FILEPATH = "day-04/fsharp_lannelin/input.txt"

let debugInput: string =
    "2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"

let dayInput: string = (System.IO.File.ReadAllText INPUT_FILEPATH).Trim()

//how many assignment pairs fully have one that fully contains the other?
// e.g. this happens in pairs 6-6,4-6 and 2-8,3-7

// either a is subset of b or b is subset of a
let hasCompleteOverlap (a: Set<'a>) (b: Set<'a>) = Set.isSubset a b || Set.isSubset b a

// any item from a is shared with b
let hasAnyOverlap (a: Set<'a>) (b: Set<'a>) = not (Set.intersect a b).IsEmpty

// expect input of "{s1}-{e1},{s2}-{e2}"
// output array len 2: [ seq(s1..e1)), seq(s2..e2)) ]
let processLine (line: string) =
    line.Split(',') //
    |> Array.map (fun (assignment: string) ->
        assignment.Split('-') // split to [s,e]
        |> Array.map int) // convert each subpart into int
    |> Array.map (fun startEnd -> { startEnd[0] .. startEnd[1] })

let main (input: string) (overlapFn: Set<int> -> Set<int> -> bool) =
    input.Split("\n")
    |> Array.map (fun line ->
        let ranges: Set<int>[] = // get range for each elf as set
            processLine line |> Array.map Set

        overlapFn ranges[0] ranges[1])
    |> Array.map System.Convert.ToInt32
    |> Array.sum


let getAnswer1 (input: string) = main input hasCompleteOverlap

printfn "answer 1 DEBUG: %d ...  should be 2" (getAnswer1 debugInput)
printfn "answer 1: %d" (getAnswer1 dayInput)

let getAnswer2 (input: string) = main input hasAnyOverlap

printfn "answer 2 DEBUG: %d ...  should be 4" (getAnswer2 debugInput)
printfn "answer 2: %d" (getAnswer2 dayInput)
