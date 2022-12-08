open System.IO


let testInput = 
  "30373
25512
65332
33549
35390".Split "\n"

let input = File.ReadAllLines "day-08/fsharp_evelinag/input.txt"

let grid = 
  testInput 
  //input
  |> Array.map (fun line -> 
      line |> Seq.map (string >> int) |> Array.ofSeq)

let size = grid.Length

let isVisible row column =
  let fromTop = [ for i in 0..row-1 -> grid.[i].[column]] |> List.max
  let fromBottom = [ for i in row+1..size-1 -> grid.[i].[column]] |> List.max
  let fromLeft = [ for i in 0..column-1 -> grid.[row].[i]] |> List.max
  let fromRight = [ for i in column+1..size-1 -> grid.[row].[i]] |> List.max

  let tree = grid.[row].[column]

  if tree > fromTop || tree > fromBottom || tree > fromLeft || tree > fromRight then
    1
  else 
    0

let visibleInterior =
  [ for i in 1..size-2 do
    for j in 1..size-2 ->
      isVisible i j ]
  |> List.sum

let visibleExterior = (size-1)*4

let visibleTotal = visibleInterior + visibleExterior

let countVisible maxHeight (treeHeights: int list)  =
  ((false, []), treeHeights)
  ||> List.fold (fun (finished, heights) h -> 
        if finished then (finished,  heights) else 
            if h < maxHeight then
              (false, h::heights)
            else
              (true, h::heights)) 
  |> snd
  |> List.length


let viewingDistance row column =
  let tree = grid.[row].[column]

  let fromTop = [ for i in row-1..-1..0 -> grid.[i].[column]] |> countVisible tree
  let fromBottom = [ for i in row+1..size-1 -> grid.[i].[column]] |> countVisible tree
  let fromLeft = [ for i in column-1..-1..0 -> grid.[row].[i]] |> countVisible tree
  let fromRight = [ for i in column+1..size-1 -> grid.[row].[i]] |> countVisible tree

  fromTop * fromBottom * fromLeft * fromRight

let maxScenicScore =
  [ for i in 1..size-2 do
    for j in 1..size-2 ->
      viewingDistance i j ]
  |> List.max
