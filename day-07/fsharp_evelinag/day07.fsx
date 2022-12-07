open System.IO

// let terminal = 
//   "$ cd /
// $ ls
// dir a
// 14848514 b.txt
// 8504156 c.dat
// dir d
// $ cd a
// $ ls
// dir e
// 29116 f
// 2557 g
// 62596 h.lst
// $ cd e
// $ ls
// 584 i
// $ cd ..
// $ cd ..
// $ cd d
// $ ls
// 4060174 j
// 8033020 d.log
// 5626152 d.ext
// 7214296 k".Split "\n"

let terminal = File.ReadAllLines "day-07/fsharp_evelinag/input.txt"

type FileSystem = 
  | File of string * int
  | Directory of string * FileSystem list


let mutable idx = 0 // position in the terminal, ugly but makes the parser cleaner

let rec parseInput (dirName: string) (contents: FileSystem list) =

  if idx = terminal.Length then
    Directory(dirName, contents)
  else
    let ts = terminal.[idx].Split " "
    idx <- idx + 1
    match ts.[0] with
    | "$" ->
      // a command
      match ts.[1] with
      | "ls" ->  parseInput dirName [] 
      | "cd" ->
          match ts.[2] with
          | ".." -> Directory(dirName, contents)
          | name -> 
              // parse the contents of the directory
              parseInput dirName ((parseInput name [])::contents)
    | "dir" -> parseInput dirName contents // nothing to do here
    | _ -> 
      // should be a file
      parseInput dirName (File(ts.[1], int ts.[0])::contents)
      
idx <- 1
let filesystem = parseInput "/" []

let rec findSmallDirectories maxSize node =
  match node with
  | File(name, size) -> size,[]  
  | Directory(name, items) -> 
      let sizes, smallOnes =
        items 
        |> List.map (findSmallDirectories maxSize)
        |> List.unzip
      let totalSize = sizes |> List.sum
      let smallOnes' = List.concat smallOnes
      totalSize, (if totalSize <= maxSize then (name, totalSize)::smallOnes' else smallOnes')

      

let totalUsed, smallDirectories = findSmallDirectories 100000 filesystem
let totalSizeOfSmall = 
  smallDirectories
  |> List.sumBy snd


let totalDiskSpace = 70000000
let spaceRequired = 30000000

let spaceAvailable = totalDiskSpace - totalUsed
let spaceToFreeUp = spaceRequired - spaceAvailable

// find the smallest directory with size larger or equal to spaceToFreeUp
let rec findToDelete node =
  match node with
  | File(name, size) -> size,[]  
  | Directory(name, items) -> 
      let sizes, largerOnes =
        items 
        |> List.map (findToDelete)
        |> List.unzip
      let totalSize = sizes |> List.sum
      let largerOnes' = List.concat largerOnes
      totalSize, (if totalSize >= spaceToFreeUp then (name, totalSize)::largerOnes' else largerOnes')

let _, largeEnoughDirectories = findToDelete filesystem
largeEnoughDirectories |> List.minBy snd