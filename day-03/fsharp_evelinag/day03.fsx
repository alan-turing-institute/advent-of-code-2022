open System.IO

let testInput = "vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw".Split "\n"

let input = 
  //testInput
  File.ReadAllLines "day-03/fsharp_evelinag/input03.txt"

let priorities = 
  List.zip 
    (List.append [ 'a'..'z' ] [ 'A'..'Z' ])
    [ 1..52 ] 
  |> dict

let commonItem compartments =
  compartments
  |> Array.map Set
  |> Set.intersectMany
  |> Set.toArray
  |> Array.exactlyOne


let errorItems =
  input
  |> Array.map (fun line ->
      let half = line.Length/2
      [| line.[0..half-1]; line.[half..] |]
      |> commonItem)

let totalPriority = errorItems |> Array.sumBy (fun key -> priorities.[key])

let inputByGroups =
  input
  |> Array.chunkBySize 3

let badges = 
  inputByGroups
  |> Array.map commonItem

let badgePriority = badges |> Array.sumBy (fun key -> priorities.[key])  
