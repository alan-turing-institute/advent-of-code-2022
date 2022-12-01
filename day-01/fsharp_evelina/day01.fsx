open System.IO

let testInput = "1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"

let input = 
  //testInput.Split("\n\n")
  File.ReadAllText "day-01/fsharp_evelina/input01.txt"
  |> fun s -> s.Split "\n\n" 

// calories carried by each elf
let elfCalories = 
  input
  |> Array.map (fun elfLoad ->
      elfLoad.Split "\n"
      |> Array.map int
      |> Array.sum)

// part 1
let maxCalories =
  elfCalories
  |> Array.max

// part 2
let top3 = 
  elfCalories
  |> Array.sortDescending
  |> Array.take 3
  |> Array.sum