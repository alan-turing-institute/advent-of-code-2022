open System.IO

let testInput = 
  //"mjqjpqmgbljsphdztnvjfqwrcgsmlb"
  //"nppdvjthqldpwncqszvftbrmjlhg"
  //"nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
  "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"

let input = 
  //testInput
  File.ReadAllText "day-06/fsharp_evelinag/input.txt"

let isMarker (window: char[]) =
  window.Length = (window |> Array.distinct |> Array.length)  

let idxStart windowSize = 
  input
  |> Seq.windowed windowSize
  |> Seq.findIndex isMarker
  |> fun i -> i + windowSize // to account for the first few characters that are not a window + get the first character index

let packetIdx = idxStart 4
let messageIdx = idxStart 14
