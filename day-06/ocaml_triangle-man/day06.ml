(** Day 6

    The tune's my own invention *)

let example = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
              |> String.to_seq
              |> Array.of_seq

let input = In_channel.input_all (In_channel.open_text "input.txt")
            |> String.to_seq
            |> Array.of_seq

(** Advance a window by one.

    A window is a pair (start_idx, end_idx), where the endpoints are inclusive.
    
    Given a window into array arr, consisting of unique values, return a new
    window which

    (a) ends at end_idx + 1; and
    (b) consists of unique values.
 *)
                       
let advance_window arr (start_idx, end_idx) =
  let next = arr.(end_idx + 1) in 
  let rec find_duplicate idx =
    if arr.(idx) = next
    then
      idx + 1
    else if idx = start_idx
    then 
      idx
else
  find_duplicate (idx - 1) in
  (find_duplicate end_idx), end_idx + 1

(** Make an infinite list of advancing windows, and return the first one whose
    length is len *)
let find_subsequence_of_uniques n arr =
  Seq.unfold (fun w -> Some (w, advance_window arr w)) (0, 0)
  |> Seq.find (fun (s, e) -> e - s = n)
  |> Option.get

(* -------------------------------------------------------------------------- *)

let main () =
  begin
    print_endline (Int.to_string (snd @@ find_subsequence_of_uniques 4 input));
    print_endline (Int.to_string (snd @@ find_subsequence_of_uniques 14 input))
  end
  
let () = main ()
