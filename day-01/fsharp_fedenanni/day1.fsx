open System.IO
open System

// first Part

let data = File.ReadAllText("input.txt")

let splitText = data.Split "\n\n"

let sumData =
    splitText |> Array.map (fun i -> i.Split("\n") |> Array.map int |> Array.sum)

let max = sumData |> Array.max

// second Part

let sortedData = sumData |> Array.sortDescending

let sumNum = sortedData[0] + sortedData[1] + sortedData[2]

Console.WriteLine sumNum
