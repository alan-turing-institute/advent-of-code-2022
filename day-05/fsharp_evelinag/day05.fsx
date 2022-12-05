open System.IO

let testInput = "    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2".Split "\n"

// each position is a stack - use a list, 
// head of the list is the top of the stack

let input = 
  //testInput
  File.ReadAllLines "day-05/fsharp_evelinag/input.txt"

let description = 
  input
  |> Array.takeWhile (fun line -> line <> "")

let nPositions = 
  description.[description.Length-1].Split(" ", System.StringSplitOptions.RemoveEmptyEntries) 
  |> Array.last
  |> int

// parse the moves
let moves =
  input
  |> Array.skipWhile (fun line -> not (line.StartsWith "move"))
  |> Array.map (fun line -> 
      line.Split " "
      |> fun items -> int items.[1], int items.[3], int items.[5])

// parse the positions
let cratePositions () =
  let crateDescription = description.[..description.Length-2]
  let cp = Array.init nPositions (fun _ -> new System.Collections.Stack())
  for horizontal in 0..nPositions-1 do
    for vertical in crateDescription.Length-1..-1..0 do
      let value = crateDescription.[vertical].[horizontal * 4 + 1] 
      if value <> ' ' then
        cp.[horizontal].Push(value)
  cp

// peek at the top crates
let topCrates (crates : System.Collections.Stack []) = 
  crates
  |> Array.map (fun x -> string (x.Peek()))
  |> String.concat ""

// -------------- part 1 ---------------

let cratePositions1 = cratePositions()

// mutates the cratePositions!
let execute1 (count, fromPosition, toPosition) =
  for _ in 1 .. count do
    let crate = cratePositions1.[fromPosition-1].Pop()
    cratePositions1.[toPosition-1].Push(crate)

moves
|> Array.iter execute1

topCrates cratePositions1

// ----------------- part 2 -------------

let cratePositions2 = cratePositions()

let execute2 (count, fromPosition, toPosition) =
  let crates = 
    [ for _ in 1..count -> cratePositions2.[fromPosition-1].Pop() ]
    |> List.rev
  crates 
  |> List.iter (fun c -> cratePositions2.[toPosition-1].Push(c))

moves
|> Array.iter execute2

topCrates cratePositions2