open System.IO


let testInput = 
  "R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2".Split "\n"

let moves = 
  //testInput
  File.ReadAllLines "day-09/fsharp_evelinag/input.txt"
  |> Array.map (fun x -> x.Split " " |> fun xs -> xs.[0], int xs.[1])

let moveTail (xh, yh) (xt, yt) =
  if ((xh - xt)*(xh - xt)) + ((yh - yt)*(yh - yt)) > 2 then
    // move the tail in the direction of the head
    let xt' = 
      if (xh = xt) then xt
      else xt + sign (xh - xt)
    let yt' = 
      if (yh = yt) then yt
      else yt + sign (yh - yt)
    xt', yt'
  else
    xt, yt  

let rec propagateMove (visitedKnots: (int*int) list) futureKnots =
  match futureKnots with
  | [] -> visitedKnots
  | k::ks ->
    let newPosition = moveTail visitedKnots.Head k
    propagateMove (newPosition::visitedKnots) futureKnots.Tail

let rec moveRope (visited: (int*int) list) (knots : (int*int) list) (direction, steps) =
  if steps = 0 then
    //plotGrid grid
    //printfn "----------"
    knots, visited
  else
    let headRow, headColumn = knots.Head
    let headPosition = 
      match direction with
      | "L" -> headRow, headColumn-1
      | "R" -> headRow, headColumn+1
      | "U" -> headRow + 1, headColumn
      | "D" -> headRow - 1, headColumn
    let knots' = propagateMove [headPosition] knots.Tail
    let tailVisited = knots'.Head
    moveRope (tailVisited::visited) (List.rev knots') (direction, steps - 1)

let countVisitedByTail ropeLength = 
  let initialPosition: ((int*int) list)*((int*int) list) = List.init ropeLength (fun _ -> (0,0)), []
  moves
  |> Array.fold (fun (positions, visited) m -> moveRope visited positions m) initialPosition
  |> snd
  |> List.distinct
  |> List.length

let part1 = countVisitedByTail 2  
let part2 = countVisitedByTail 10