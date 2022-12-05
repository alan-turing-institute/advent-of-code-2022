use itertools::Itertools;

struct SectionRange {
    start: u32,
    end: u32,
}

impl SectionRange {
    fn new(s: &str) -> Self {
        let (start, end) = s.split_once('-').unwrap();
        Self {
            start: start.parse::<u32>().unwrap(),
            end: end.parse::<u32>().unwrap(),
        }
    }
}

fn overlap_complete(left: &SectionRange, right: &SectionRange) -> bool {
    (left.start >= right.start && left.end <= right.end)
        || (right.start >= left.start && right.end <= left.end)
}

fn overlap_any(left: &SectionRange, right: &SectionRange) -> bool {
    (left.end >= right.start && left.start <= right.start)
        || (right.end >= left.start && right.start <= left.start)
}

fn calculate_overlaps<F>(input: &str, overlap_fn: F) -> u32
where
    F: Fn(&SectionRange, &SectionRange) -> bool,
{
    input
        .lines()
        .map(|line| {
            let (left_range, right_range) =
                line.split(',').map(SectionRange::new).collect_tuple().unwrap();
            overlap_fn(&left_range, &right_range) as u32
        })
        .sum::<u32>()
}

pub fn part_one(input: &str) -> Option<u32> {
    Some(calculate_overlaps(input, overlap_complete))
}

pub fn part_two(input: &str) -> Option<u32> {
    Some(calculate_overlaps(input, overlap_any))
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 4);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 4);
        assert_eq!(part_one(&input), Some(2));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 4);
        assert_eq!(part_two(&input), Some(4));
    }
}
