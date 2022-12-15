(** Day 4

    Copied from lannelin's F# *)

open List

(* Quick module for intervals.
   TODO: check that the lower end is not greater than the upper end
 *)
module Interval =
  struct
    type t = int * int
    let subset (x0, y0) (x1, y1) =
      x0 >= x1 && y0 <= y1
    let within i1 i2 =
      (subset i1 i2) || (subset i2 i1)
    let overlap (x0, y0) (x1, y1) =
      max x0 x1 <= min y0 y1
  end


let debug_input =
  "2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"

let pair_of_list xs = (nth xs 0), (nth xs 1)

let process_line line =
  line
  |> String.split_on_char ','
  |> map (fun assignment ->
         assignment 
         |> String.split_on_char '-'
         |> map int_of_string
         |> pair_of_list)
  |> pair_of_list

let sections = String.split_on_char '\n'debug_input
               |> map process_line

let count_where comparator sections =
  let selected = filter (fun (p1, p2) -> comparator p1 p2) sections in
  length selected

(* Parts 1 and 2 *)

let part1 = count_where Interval.within sections

let part2 = count_where Interval.overlap sections


