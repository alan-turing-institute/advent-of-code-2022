use itertools::Itertools;

fn find_first_unique_window(input: &str, length: usize) -> Option<u32> {
    // A sliding window of size n
    for window in input.as_bytes().windows(length).enumerate() {
        // Use Itertools' unique instead of rolling our own
        if window.1.into_iter().unique().collect::<Vec<&u8>>().len() == length {
            // window.0 is the idx of the start of the window
            // but the answer requires the end of it
            return Some((window.0 + length) as u32);
        }
    }
    None
}

pub fn part_one(input: &str) -> Option<u32> {
    find_first_unique_window(input, 4)
}

pub fn part_two(input: &str) -> Option<u32> {
    find_first_unique_window(input, 14)
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
        let mut input = "mjqjpqmgbljsphdztnvjfqwrcgsmlb";
        assert_eq!(part_one(&input), Some(7));

        input = "bvwbjplbgvbhsrlpgdmjqwftvncz";
        assert_eq!(part_one(&input), Some(5));

        input = "nppdvjthqldpwncqszvftbrmjlhg";
        assert_eq!(part_one(&input), Some(6));

        input = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg";
        assert_eq!(part_one(&input), Some(10));

        input = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw";
        assert_eq!(part_one(&input), Some(11));
    }

    #[test]
    fn test_part_two() {
        let mut input = "mjqjpqmgbljsphdztnvjfqwrcgsmlb";
        assert_eq!(part_two(&input), Some(19));

        input = "bvwbjplbgvbhsrlpgdmjqwftvncz";
        assert_eq!(part_two(&input), Some(23));

        input = "nppdvjthqldpwncqszvftbrmjlhg";
        assert_eq!(part_two(&input), Some(23));

        input = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg";
        assert_eq!(part_two(&input), Some(29));

        input = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw";
        assert_eq!(part_two(&input), Some(26));
    }
}
