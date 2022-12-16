open System.IO
open System.Text.RegularExpressions

let testInput = 
  "Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3".Split "\n"

let sensors, beacons = 
  //testInput
  File.ReadAllLines "day-15/fsharp_evelinag/input.txt"
  |> Array.map (fun line ->
    let xRegex = Regex "x=[-0-9]+"
    let yRegex = Regex "y=[-0-9]+"
    line.Split ":" 
    |> Array.map (fun part -> 
          let xMatch = xRegex.Match part
          let yMatch = yRegex.Match part
          int xMatch.Value.[2..], int yMatch.Value.[2..]
        )
    |> fun xs -> xs.[0], xs.[1])
  |> Array.unzip

let alreadyOccupied = Array.append sensors beacons |> Set

let distance (x1,y1) (x2,y2) = abs(x2 - x1) + abs(y2 - y1)

let beaconDistance = 
  (sensors, beacons)
  ||> Array.zip
  |> Array.map (fun (s, b) -> distance s b)        

// beacons, distances from beacon


let sensorArea =
  (sensors, beaconDistance)
  ||> Array.map2 (fun (x,y) distance ->
        // create intervals that are covered by the sensor
        [| for rowOffset in -distance .. distance ->
            let start = x - (distance - abs(rowOffset)), y + rowOffset
            let finish = x + (distance - abs(rowOffset)), y + rowOffset
            start, finish |]
        )
  |> Array.concat 

// Real: 00:00:22.486, CPU: 00:00:21.559, GC gen0: 2866, gen1: 121, gen2
let rowCoveredSlow (sensorArea : ((int*int)*(int*int))[]) row = 
  let relevantRows = 
    sensorArea
    |> Array.filter (fun (start, finish) -> snd start = row)
  ([], relevantRows) 
  ||> Array.fold (fun covered ((startx,_), (finishx,_)) ->
        let elements = [startx .. finishx] |> List.map (fun x -> x, row)
        List.append elements covered
        )
  |> List.distinct
  |> Set
  |> fun s -> Set.difference s alreadyOccupied
  |> Set.count


let row = 2000000
//rowCoveredSlow sensorArea row

let maxSize = 4000000

let sensorEnvelope = 
  (sensors, beaconDistance)
  ||> Array.zip
  |> Array.collect (fun ((x,y), distance) ->
        [|  for rowOffset in - (distance) .. (distance) do
              yield (x - (distance - abs(rowOffset))) - 1, (y + rowOffset)
              yield (x + (distance - abs(rowOffset))) + 1, (y + rowOffset)
            yield x, y - distance - 1
            yield x, y + distance + 1
        |]
        |> Array.filter (fun (x,y) -> x >= 0 && x <= maxSize && y >= 0 && y <= maxSize)
        |> Array.filter (fun (x, y) -> not (alreadyOccupied.Contains (x,y)))
      )
  |> Array.countBy id
  |> Array.sortByDescending snd

let (sensorX, sensorY), _ = sensorEnvelope.[0]
(int64 sensorX) * 4000000L + (int64 sensorY)
