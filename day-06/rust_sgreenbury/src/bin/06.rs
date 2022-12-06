use std::ops::ControlFlow;
use hashbrown::HashMap;

fn start_of_packet_idx(input: &str, window_size: usize) -> Option<usize> {
    match input
        .chars()
        .collect::<Vec<_>>()
        .windows(window_size + 1)
        .enumerate()
        .try_fold(
            // Populate hashmap with chars from first window
            input.chars().take(window_size).fold(
                HashMap::<char, u32>::new(),
                |mut acc, c| {
                    *acc.entry(c).or_insert(0) += 1;
                    acc
                },
            ),
            |mut acc, (idx, window)| {
                // Return if hashmap has same number of keys as window_size
                if acc.len() == window_size {
                    return ControlFlow::Break(idx + window_size);
                }
                // Increment count of last char of window
                *acc.entry(*window.last().unwrap()).or_insert(0) += 1;
                // Decrement count of first char of window
                let first = window.first().unwrap();
                let count = acc.entry(*first).or_insert(0);
                *count -= 1;
                // Remove first char of window if no more within window
                if *count == 0 {
                    acc.remove(first);
                }
                ControlFlow::Continue(acc)
            },
        ) {
        ControlFlow::Break(idx) => Some(idx),
        _ => None
    }
}

pub fn part_one(input: &str) -> Option<usize> {
    start_of_packet_idx(input, 4)
}

pub fn part_two(input: &str) -> Option<usize> {
    start_of_packet_idx(input, 14)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 6);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 6);
        assert_eq!(part_one(&input), Some(7));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 6);
        assert_eq!(part_two(&input), Some(19));
    }
}
