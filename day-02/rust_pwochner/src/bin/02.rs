use itertools::Itertools;

pub fn part_one(input: &str) -> Option<u32> {
    Some(
        input
            .lines()
            .map(|line| compute_score_part1(line))
            .sum::<u32>(),
    )
}

pub fn part_two(input: &str) -> Option<u32> {
    Some(
        input
            .lines()
            .map(|line| compute_score_part2(line))
            .sum::<u32>(),
    )
}

fn compute_score_part1(round: &str) -> u32 {
    let outcome = match round {
        "A X" => 3 + 1,
        "A Y" => 6 + 2,
        "A Z" => 0 + 3,
        "B X" => 0 + 1,
        "B Y" => 3 + 2,
        "B Z" => 6 + 3,
        "C X" => 6 + 1,
        "C Y" => 0 + 2,
        "C Z" => 3 + 3,
        _ => panic!(),
    };
    return outcome;
}

fn compute_score_part2(round: &str) -> u32 {
    let outcome = match round {
        //1 for Rock, 2 for Paper, and 3 for Scissors
        "A X" => 0 + 3, // Rock + Scissor => Lose
        "A Y" => 3 + 1, // Rock + Rock => Draw
        "A Z" => 6 + 2, // Rock + Paper => Win
        "B X" => 0 + 1, // Paper + Rock => Lose
        "B Y" => 3 + 2, // Paper + Paper => Draw
        "B Z" => 6 + 3, // Paper + Scissors => Scissor Win
        "C X" => 0 + 2, // Scissors + Paper => Lose
        "C Y" => 3 + 3, // Scissors + Scissors => Draw
        "C Z" => 6 + 1, // Scissors + Rock => Win
        _ => panic!(),
    };
    return outcome;
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
