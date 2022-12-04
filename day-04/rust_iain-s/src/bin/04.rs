fn map_some_thing(input: &str, func: fn((u32, u32), (u32, u32)) -> bool) -> Option<u32> {
    Some(
        input
            .split("\n")
            .map(|line| {
                if line != "" {
                    let (l, r) = line.split_once(",").unwrap();
                    let (left, right) = (l.split_once("-").unwrap(), r.split_once("-").unwrap());

                    // There must be a better way to cast a tuple of strs...
                    if one_funcs_the_other(
                        func,
                        (left.0.parse().unwrap(), left.1.parse().unwrap()),
                        (right.0.parse().unwrap(), right.1.parse().unwrap()),
                    ) {
                        return 1;
                    }
                }
                0
            })
            .sum(),
    )
}

pub fn part_one(input: &str) -> Option<u32> {
    map_some_thing(input, left_contains_right)
}

pub fn part_two(input: &str) -> Option<u32> {
    map_some_thing(input, left_overlaps_right)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 4);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

fn left_overlaps_right(left: (u32, u32), right: (u32, u32)) -> bool {
    left.0 <= right.0 && left.1 >= right.0
}

fn left_contains_right(left: (u32, u32), right: (u32, u32)) -> bool {
    // Does left contain right?
    left.0 <= right.0 && left.1 >= right.1
}

fn one_funcs_the_other(
    func: fn((u32, u32), (u32, u32)) -> bool,
    left: (u32, u32),
    right: (u32, u32),
) -> bool {
    // Does either left or right func the other?
    func(left, right) || func(right, left)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_left_overlaps_right() {
        assert!(left_overlaps_right((2, 3), (3, 4)));
        assert!(left_overlaps_right((2, 2), (2, 3)));
    }

    #[test]
    fn test_one_contains_the_other() {
        assert_eq!(
            one_funcs_the_other(left_contains_right, (6, 6), (6, 6)),
            true
        );
        assert_eq!(
            one_funcs_the_other(left_contains_right, (2, 5), (3, 4)),
            true
        );
        assert_eq!(
            one_funcs_the_other(left_contains_right, (0, 1), (2, 3)),
            false
        );
    }

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
