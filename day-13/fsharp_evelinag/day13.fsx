open System.IO

let testInput = 
  "[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"

type Packet = 
  | Value of int
  | ValueList of Packet list

let rec toString (p:Packet) =
  match p with
  | Value(x) -> string x
  | ValueList(xs) -> "[" + (xs |> List.map toString |> String.concat ",") + "]"


let parsePacket (str: string) =
  let mutable idx = 0 // position in the string

  let rec parseNumber acc =
    let symbol = str.[idx]
    match symbol with
    | x when x >= '0' && x <= '9' -> 
        idx <- idx + 1
        parseNumber (x::acc)
    | _ -> 
        acc 
        |> List.rev 
        |> List.map string 
        |> String.concat "" 
        |> int
        |> Value

  let rec parseList (contents: Packet list) =
    if idx = str.Length then 
      contents
    else
      let symbol = str.[idx]
      idx <- idx + 1
      match symbol with
      | ']' -> contents |> List.rev
      | '[' -> 
          let inner = parseList []
          parseList [ValueList(inner)]
      | ',' -> List.append contents (parseList [])
      | x when x >= '0' && x <= '9' -> 
        let n = parseNumber [x]
        parseList (n :: contents)

  let result = parseList []
  if toString result.[0] <> str then
    printfn $"expected: {str}\nparsed: {result.[0]}\n\n"
  result.[0] // it's all wrapped in a list


let packets = 
  //testInput
  File.ReadAllText "day-13/fsharp_evelinag/input.txt"
  |> fun text -> text.Split "\n\n"
  |> Array.map (fun pair ->
      pair.Split "\n" |> fun xs -> parsePacket xs.[0], parsePacket xs.[1])

let rec isRightOrder packet1 packet2 =
  match packet1, packet2 with
  | Value(p1), Value(p2) when p1 = p2 -> None
  | Value(p1), Value(p2) when p1 < p2 -> Some true
  | Value(p1), Value(p2) when p1 > p2 -> Some false
  | ValueList(p1), ValueList(p2) ->
      let rec compareLists l1 l2 =
        match l1, l2 with
        | [], [] -> None
        | [], x::xs -> Some true
        | x::xs, [] -> Some false
        | x::xs, y::ys ->
            match isRightOrder x y with
            | Some(value) -> Some(value)
            | None -> compareLists xs ys
      compareLists p1 p2
  | ValueList(p1), Value(p2) -> isRightOrder packet1 (ValueList [packet2])
  | Value(p1), ValueList(p2) -> isRightOrder (ValueList [packet1]) packet2



let part1 = 
  packets
  |> Array.mapi (fun idx (p1, p2) -> 
    match isRightOrder p1 p2 with
    | Some(true) ->  
      idx + 1 
    | Some(false) | None -> 0)
  |> Array.sum

let specialPackets = [| parsePacket "[[2]]"; parsePacket "[[6]]" |]  

let part2packets = 
  packets
  |> Array.collect (fun (p1, p2) -> [|p1; p2|])
  |> Array.append specialPackets

let sorted =
  part2packets
  |> Array.sortWith (fun p1 p2 -> 
      match isRightOrder p1 p2 with
      | Some(true) -> -1
      | Some(false) -> 1
      | None -> 0)

let part2 =
  specialPackets
  |> Array.map (fun p ->
      sorted |> Array.findIndex ((=) p))
  |> fun is -> (is.[0]+1) * (is.[1]+1)   

