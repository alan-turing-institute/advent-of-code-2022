

open System.IO

let exampleInput = "A Y
B X
C Z"

let parseInput x =
  match x with
  | "X" | "A" -> 0
  | "Y" | "B" -> 1
  | "Z" | "C" -> 2

let input = 
  //exampleInput.Split "\n"
  File.ReadAllLines "day-02/fsharp_evelina/input02.txt"
  |> Array.map (fun s -> 
      let items = s.Split " "
      parseInput items.[0], parseInput items.[1]
) 

let shapeValue x = x + 1

let scoreGame1 (opponent, myself) =
  match (opponent, myself) with
  | x, y when y = (x + 1) % 3 -> 6 + shapeValue myself
  | x, y when x = y -> 3 + shapeValue myself
  | x, y when (y + 1) % 3 = x -> 0 + shapeValue myself

input |> Array.sumBy (fun x -> scoreGame1 x)

let scoreGame2 (opponent, outcome) =
  match (opponent, outcome) with
  | x, 0 -> 0 + shapeValue ((3 + x - 1)%3)
  | x, 1 -> 3 + shapeValue x
  | x, 2 -> 6 + shapeValue ((x + 1)%3)

input |> Array.sumBy (fun x -> scoreGame2 x)
