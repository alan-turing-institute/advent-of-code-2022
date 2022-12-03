fn halve(input: &str) -> (&str, &str) {
    (&input[..input.len() / 2], &input[input.len() / 2..])
}

fn find_common(left: Vec<u8>, right: Vec<u8>) -> u8 {
    // Returns the common u8 of two Vecs, which must be sorted

    println!("{:?}", left);
    println!("{:?}", right);

    let mut l = 0;
    let mut r = 0;

    loop {
        if left[l] < right[r] {
            l += 1;
        } else if left[l] > right[r] {
            r += 1;
        } else {
            break;
        }
    }
    left[l]
}

fn find_common_vec(left: Vec<u8>, right: Vec<u8>) -> Vec<u8> {
    let mut result: Vec<u8> = Vec::new();

    let mut l = 0;
    let mut r = 0;

    loop {
        if l == left.len() || r == right.len() {
            break;
        }

        if left[l] < right[r] {
            l += 1;
        } else if left[l] > right[r] {
            r += 1;
        } else {
            result.push(left[l]);
            l += 1;
            r += 1;
        }
    }

    result
}

fn find_common_three(one: Vec<u8>, two: Vec<u8>, three: Vec<u8>) -> u8 {
    // Returns the common u8 of three Vecs, which must be sorted

    find_common_vec(find_common_vec(one, two), three)[0]
}

fn score(item: u8) -> u8 {
    match item {
        // A to Z
        65u8..=90u8 => item - 38,
        // a to z
        97u8..=122u8 => item - 96,
        _ => panic!("unknown char"),
    }
}

pub fn part_one(input: &str) -> Option<u32> {
    Some(
        input
            .split("\n")
            .map(|item| {
                let (left, right) = halve(item);

                let mut left_vec = Vec::from(left);
                let mut right_vec = Vec::from(right);

                left_vec.sort_unstable();
                right_vec.sort_unstable();

                let common = find_common(left_vec, right_vec);

                let the_score = score(common);

                the_score as u32
            })
            .sum(),
    )
}

pub fn part_two(input: &str) -> Option<u32> {
    let x = String::from(input).split("\n").collect::<Vec<&str>>().chunks(3).map(|item|{
        println!("item: {:?}", item);

        let mut one = Vec::from(item[0]);
        let mut two = Vec::from(item[1]);
        let mut three = Vec::from(item[2]);
        one.sort_unstable();
        two.sort_unstable();
        three.sort_unstable();
        score(find_common_three(one, two, three)) as u32
    }).sum();
    return Some(x);

    // let a = input.split("\n").collect::<Vec<&str>>().chunks(3);
    // println!("{:?}",a);
    return None;
    Some(
        input
            .split("\n")
            // .collect::<Vec<char>>()
            // .chunks(3)
            .map(|item| {
                let (left, right) = halve(item);

                let mut left_vec = Vec::from(left);
                let mut right_vec = Vec::from(right);

                left_vec.sort_unstable();
                right_vec.sort_unstable();

                let common = find_common(left_vec, right_vec);

                let the_score = score(common);

                the_score as u32
            })
            .sum(),
    )
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 3);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_find_common_vec() {
        // These vecs hold their ascii codes
        assert_eq!(
            find_common_vec(Vec::from("abc"), Vec::from("bcde")),
            Vec::from("bc")
        );
    }

    #[test]
    fn test_find_common_three() {
        // These vecs hold their ascii codes
        let mut one = Vec::from("vJrwpWtwJgWrhcsFMMfFFhFp");
        let mut two = Vec::from("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL");
        let mut three = Vec::from("PmmdzqPrVvPwwTWBwg");

        one.sort_unstable();
        two.sort_unstable();
        three.sort_unstable();

        assert_eq!(find_common_three(one, two, three), 'r' as u8);
    }

    #[test]
    fn test_score() {
        let input = Vec::from("Aa");
        assert_eq!(score('a' as u8), 1);
        assert_eq!(score('z' as u8), 26);
        assert_eq!(score('A' as u8), 27);
        assert_eq!(score('Z' as u8), 52);
    }

    #[test]
    fn test_find_common() {
        let input = "abcedefg";

        let (left, right) = halve(input);

        // These vecs hold their ascii codes
        let mut left_vec = Vec::from(left);
        let mut right_vec = Vec::from(right);

        left_vec.sort_unstable();
        right_vec.sort_unstable();

        assert_eq!(find_common(left_vec, right_vec), 'e' as u8);
    }

    #[test]
    fn test_halve() {
        let input = "abcdef";
        // halve(input);
        assert_eq!(halve(&input), ("abc", "def"));
    }

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 3);
        assert_eq!(part_one(&input), Some(157));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 3);
        assert_eq!(part_two(&input), Some(70));
    }
}
