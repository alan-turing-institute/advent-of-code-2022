open System.IO

let testInput = "Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"

type Monkey = {
    Id : int
    Operation : int64 -> int64
    Divisor : int64
    IfTrue : int
    IfFalse : int
    }  

let readMonkeys ()= 
  //testInput
  File.ReadAllText "day-11/fsharp_evelinag/input.txt"
  |> fun s -> s.Split "\n\n"
  |> Array.map (fun m ->
      let lines = m.Split "\n"
      {  
        Id = lines.[0].Split([|' ';':'|]) |> fun xs -> xs.[1] |> int
        Operation = 
          let expr = lines.[2].Split ':' |> fun xs -> xs.[1].Trim().Split ' '
          match expr.[3] with
          | "+" -> fun x -> x + if expr.[4] = "old" then x else int64 expr.[4]
          | "*" -> fun x -> x * if expr.[4] = "old" then x else int64 expr.[4]
        Divisor = lines.[3].Split("by") |> fun xs -> xs.[1] |> int64
        IfTrue = lines.[4].Split " " |> fun xs -> xs.[xs.Length-1] |> int
        IfFalse = lines.[5].Split " " |> fun xs -> xs.[xs.Length-1] |> int
      }, 
      lines.[1].Split(':') |> fun xs -> xs.[1].Split "," |> Array.map int64 )
  |> Array.unzip

// -------

// Euclidean algorithm to find the greatest common divisor 
let rec gcd a b =
    if b = 0L then a
    else gcd b (a % b)    

// least common multiple
let lcm a b =
  (a * b) / (gcd a b) 


let runMonkeyBusiness rounds divideWorry =
  let monkeys, monkeyItems = readMonkeys()

  // we're only interested if the worry levels are divisible by the relevant monkey-divisors,
  // it's okay to take worry values modulo LCM
  let worryLCM = 
    monkeys 
    |> Array.map (fun m -> m.Divisor)
    |> Array.fold lcm 1L

  let inspected = Array.init monkeys.Length (fun _ -> 0L)

  let playRound i monkeyIdx =
    let m = monkeys.[monkeyIdx]
    let items = monkeyItems.[monkeyIdx]
    monkeyItems.[monkeyIdx] <- [||]
    inspected.[monkeyIdx] <- inspected.[monkeyIdx] + int64 items.Length

    for item in items do
      let worryLevel = (m.Operation item)/(if divideWorry then 3L else 1L) |> fun w -> w % worryLCM
      let nextMonkey = if worryLevel % m.Divisor = 0L then m.IfTrue else m.IfFalse
      monkeyItems.[nextMonkey] <- Array.append monkeyItems.[nextMonkey] [| worryLevel |]

  for i in 1..rounds do
    for m in 0..monkeys.Length-1 do
      playRound i m // mutates monkeyItems
     
  printfn "%A" inspected   
  inspected |> Array.sortDescending |> fun xs -> xs.[0] * xs.[1]

runMonkeyBusiness 20 true
runMonkeyBusiness 10000 false

