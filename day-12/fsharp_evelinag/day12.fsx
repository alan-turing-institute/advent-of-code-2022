open System.IO

let testInput = 
  "Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi".Split "\n"

let elevation = 
  //testInput
  File.ReadAllLines "day-12/fsharp_evelinag/input.txt"
  |> Array.map (fun line -> line |> Seq.toArray)

let vertices = 
  [| for i in 0..elevation.Length-1 do
       for j in 0..elevation.[0].Length-1 -> i,j |]

let startPosition = 
  let x = 
    elevation 
    |> Array.findIndex (fun line -> line |> Array.contains 'S')
  let y = elevation.[x] |> Array.findIndex ((=) 'S')
  x,y
let targetPosition = 
  let x = 
    elevation 
    |> Array.findIndex (fun line -> line |> Array.contains 'E')
  let y = elevation.[x] |> Array.findIndex ((=) 'E')
  x,y
elevation.[fst startPosition].[snd startPosition] <- 'a'
elevation.[fst targetPosition].[snd targetPosition] <- 'z'

// reverse for part 2, to start from target
let possibleMovesRev (elevation: char[][]) (x,y) =
  let value = elevation.[x].[y] |> int
  // extract neighbouring locations where value <= elevation + 1
  [|
    if x > 0 then 
      if int elevation.[x-1].[y] + 1 >= value then yield x-1, y
    if x < elevation.Length-1 then
      if int elevation.[x+1].[y] + 1 >= value then yield x+1, y
    if y > 0 then
      if int elevation.[x].[y-1] + 1 >= value then yield x, y-1
    if y < elevation.[0].Length-1 then
      if int elevation .[x].[y+1] + 1 >= value then yield x, y+1
  |]  

let breadthFirstSearch startPosition getNeighbours isTarget =
  let q = System.Collections.Generic.Queue<int*int>()
  let explored = 
    vertices 
    |> Array.map (fun x -> x, false) 
    |> dict 
    |> System.Collections.Generic.Dictionary
  explored.[startPosition] <- true
  let parent : System.Collections.Generic.Dictionary<int*int, (int*int) option> = 
    vertices
    |> Array.map (fun x -> x, None) 
    |> dict 
    |> System.Collections.Generic.Dictionary

  q.Enqueue(startPosition)

  let rec bfsStep () =
    if q.Count = 0 then ()

    let v = q.Dequeue()
    if isTarget v then
      v
    else
      for w in getNeighbours v do
        if not explored.[w] then
          explored.[w] <- true
          parent.[w] <- Some v
          q.Enqueue(w)
      bfsStep()

  // reconstruct the path
  let rec getPath v acc =
    match v with
    | None -> failwith "Path not found."
    | Some(u) when u = startPosition -> u::acc
    | Some(u) -> getPath parent.[u] (u::acc)

  let target = bfsStep()
  getPath (Some target) []

// Search from target to start
let path1 = breadthFirstSearch targetPosition (possibleMovesRev elevation) ((=) startPosition)
path1.Length - 1 

let path2 = breadthFirstSearch targetPosition (possibleMovesRev elevation) (fun (x,y) -> elevation.[x].[y] = 'a')
path2.Length - 1
