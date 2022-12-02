// Rock, Paper, Scissors -> 0, 1, 2 for columns and rows
const PAYOFF_MATRIX: [[u32; 3]; 3] = [[3, 0, 6], [6, 3, 0], [0, 6, 3]];

#[derive(Clone, Copy)]
enum Strategy {
    Rock,
    Paper,
    Scissors,
}

impl Strategy {
    fn to_idx(self) -> usize {
        match self {
            Strategy::Rock => 0,
            Strategy::Paper => 1,
            Strategy::Scissors => 2,
        }
    }
}

fn decode_opponent(encoded_char: char) -> Strategy {
    match encoded_char {
        'A' => Strategy::Rock,
        'B' => Strategy::Paper,
        'C' => Strategy::Scissors,
        _ => panic!("Invalid strategy char."),
    }
}

fn decode_part1(_left: &Strategy, encoded_char: char) -> Strategy {
    match encoded_char {
        'X' => Strategy::Rock,
        'Y' => Strategy::Paper,
        'Z' => Strategy::Scissors,
        _ => panic!("Invalid strategy char."),
    }
}

fn decode_part2(left: &Strategy, encoded_char: char) -> Strategy {
    match encoded_char {
        'X' => match left {
            Strategy::Rock => Strategy::Scissors,
            Strategy::Paper => Strategy::Rock,
            Strategy::Scissors => Strategy::Paper,
        },
        'Y' => *left,
        'Z' => match left {
            Strategy::Rock => Strategy::Paper,
            Strategy::Paper => Strategy::Scissors,
            Strategy::Scissors => Strategy::Rock,
        },
        _ => panic!("Invalid strategy char."),
    }
}

fn play_game(input: &str, decode_fn: &dyn Fn(&Strategy, char) -> Strategy) -> u32 {
    input
        .lines()
        .map(|line| {
            let left_strategy = decode_opponent(line.chars().next().unwrap());
            let right_strategy = decode_fn(&left_strategy, line.chars().rev().next().unwrap());
            (left_strategy, right_strategy)
        })
        .map(|(left, right)| {
            let right_idx = right.to_idx();
            let payoff = PAYOFF_MATRIX[right_idx][left.to_idx()];
            payoff + right_idx as u32 + 1
        })
        .sum()
}

pub fn part_one(input: &str) -> Option<u32> {
    Some(play_game(input, &decode_part1))
}

pub fn part_two(input: &str) -> Option<u32> {
    Some(play_game(input, &decode_part2))
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 2);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 2);
        assert_eq!(part_one(&input), Some(15));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 2);
        assert_eq!(part_two(&input), Some(12));
    }
}
