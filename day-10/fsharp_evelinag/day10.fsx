open System.IO

type Instruction =
  | Noop
  | Addx of int

let instructions = 
  //testInput
  File.ReadAllLines "day-10/fsharp_evelinag/input.txt"
  |> Array.map (fun line ->
      if line.StartsWith "noop" then 
        Noop
      else 
        line.Split " " |> fun xs -> Addx (int xs.[1]))
  |> List.ofArray

let recordCycle = 40
let recordInitial = 20

let rec measureSignal x additionInProgress step instructions acc = 
  // record the result
  let acc' = (step, x)::acc
    // if (step - recordInitial) % recordCycle = 0 then 
    //   x*step::acc 
    // else 
    //   acc

  match additionInProgress with
  | Some(n) -> measureSignal (x + n) None (step + 1) instructions acc'
  | None ->
    match instructions with
    | Noop::rest ->
       measureSignal x None (step + 1) rest  acc'
    | Addx(n)::rest ->
       measureSignal x (Some(n)) (step + 1) rest acc'
    | [] -> acc'

let signals = measureSignal 1 None 1 instructions []
let part1 = 
  signals 
  |> List.choose (fun (step, value) -> 
      if (step - recordInitial) % recordCycle = 0  then Some(step * value)
      else None)
  |> List.sum


//---------
// part 2

let width = 40
let height = 6

let screen = Array.init height (fun _ -> Array.init width (fun _ -> '.'))

let printScreen (screen:char[][]) =
  for row in 0 .. height-1 do
    for column in 0..width-1 do
      printf $" {screen.[row].[column]}"
    printfn "\n"

let spriteLookup = signals |> dict

let rec crt position step =
  if position = width * height then position
  else
    // draw a pixel - is sprite visible?
    let row = position/width
    let column = (position - (row*width))%width
    let sprite = spriteLookup.[step]
    if (abs(sprite - column)) <= 1 then
      screen.[row].[column] <- '■'

    // go to next pixel
    crt (position + 1) (step + 1)

crt 0 1
printScreen screen