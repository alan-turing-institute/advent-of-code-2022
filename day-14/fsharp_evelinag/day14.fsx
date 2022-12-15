open System.IO

let testInput =
  "498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9".Split "\n"

let linePoints =
  //testInput
  File.ReadAllLines "day-14/fsharp_evelinag/input.txt"
  |> Array.map (fun line ->
    line.Split " -> " 
    |> Array.map (fun coordinates -> 
        coordinates.Split "," |> fun xs -> int xs.[0], int xs.[1]))

let width = 1000
let maxY = linePoints |> Array.concat |> Array.maxBy snd |> snd 
let height = maxY |> (+) 5

let source = 500,0

// grid is an array of column vectors
let initGrid () = 
  Array.init width (fun _ -> Array.init (height+2) (fun _ -> '.'))

let drawMap hasFloor =
  let grid = initGrid()
  grid.[fst source].[snd source] <- '+'
  linePoints
  |> Array.collect (fun line ->
      line
      |> Array.pairwise )
  |> Array.distinct
  |> Array.iter (fun ((x1,y1), (x2,y2)) -> 
        for i1 in (min x1 x2) .. (max x1 x2) do
          for i2 in (min y1 y2) .. (max y1 y2) do
              grid.[i1].[i2] <- '#')
  if hasFloor then
    for x in 0..width-1 do
      grid.[x].[maxY + 2] <- '#'
  grid                

let printSection (xmin, xmax) (ymin, ymax) (grid: char[][]) = 
  for y in ymin..ymax do
    for x in xmin..xmax do
      printf $"{grid.[x].[y]}"
    printf "\n"

let runSimulation hasFloor = 

  let grid = drawMap hasFloor

  let rec simulateUnit (x, y) hasFloor =
    if not hasFloor && y = maxY + 1  then 
      printfn "finished"
      true 
    else
      match grid.[x].[y+1] with
      | '.' -> simulateUnit (x, y+1) hasFloor
      | _ -> // down is blocked
        // try down and left
        match grid.[x-1].[y+1] with
        | '.' -> simulateUnit (x-1, y+1) hasFloor
        | _ -> 
          // try down and right
          match grid.[x+1].[y+1] with
          | '.' -> simulateUnit (x+1, y+1) hasFloor
          | _ -> 
              // no possible moves
              grid.[x].[y] <- 'o'
              if hasFloor && (x,y) = source then 
                true
              else
                false

  let rec simulate count hasFloor =
    let inTheAbyss = simulateUnit source hasFloor
    if inTheAbyss then
      if hasFloor then 
        count + 1, grid
      else 
        count, grid
    else
      simulate (count + 1) hasFloor

  simulate 0 hasFloor

let count, grid = runSimulation true
grid |> printSection (450,550) (0,height)
