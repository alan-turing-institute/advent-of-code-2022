open System.IO

let testInput = 
  "2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8".Split "\n"

let input = 
  //testInput
  File.ReadAllLines "day-04/fsharp_evelinag/input.txt"
  |> Array.map (fun line -> 
      line.Split ","
      |> fun items -> 
          let parse (x: string) = x.Split "-" |> fun xs -> int xs.[0], int xs.[1]
          parse items.[0], parse items.[1])  

let contains (x1, x2) (y1, y2) = 
  (x1 <= y1) && (x2 >= y2)

let fullycontained = 
  input
  |> Array.filter (fun (x, y) -> (contains x y) || (contains y x))
  |> Array.length

let overlaps (x1, x2) (y1, y2) = 
  contains (y1, y2) (x1, x2) ||
  ((x1 <= y1) && (y1 <= x2)) || ((x1 <= y2) && (y2 <= x2))  

let overlaping =    
  input
  |> Array.filter (fun (x, y) -> overlaps x y)
  |> Array.length
