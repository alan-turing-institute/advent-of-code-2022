use std::collections::HashSet;

pub fn part_one(input: &str) -> Option<usize> {
    Some(nr_chars_starter_marker(input, 4))
}

pub fn part_two(input: &str) -> Option<usize> {
    Some(nr_chars_starter_marker(input, 14))
}

fn unique_chars(window: &str) -> usize {
    let set: HashSet<char> = window.chars().collect();
    return set.len();
}

fn nr_chars_starter_marker(input: &str, marker_size: usize) -> usize {
    let mut start = 0;
    loop {
        if unique_chars(&input[start..start + marker_size]) == marker_size {
            break;
        }
        start += 1;
    }
    return start + marker_size;
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
        assert_eq!(part_one(&input), Some(11));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 6);
        assert_eq!(part_two(&input), Some(26));
    }
}
