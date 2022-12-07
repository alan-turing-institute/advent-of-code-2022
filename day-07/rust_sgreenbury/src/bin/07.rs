use hashbrown::HashMap;

// Line patterns:
// "$ ls", "$ cd DIR_NAME", "$ cd ..", "$ cd /", "dir DIR_NAME", "\d+ FILE_NAME"

fn process_line(
    line: &str,
    mut path: Vec<String>,
    mut sizes: HashMap<String, u32>,
) -> (Vec<String>, HashMap<String, u32>) {
    match line {
        _ if line.starts_with("$ cd ..") => {
            path.pop();
        }
        _ if line.starts_with("$ cd /") => {
            path.clear();
            path.push("/".to_string())
        }
        line if line.starts_with("$ cd") => path.push(line.rsplit_once(' ').unwrap().1.to_string()),
        line if line.chars().next().unwrap().is_numeric() => {
            let (size, _) = line.split_once(' ').unwrap();
            let size = size.parse::<u32>().unwrap();
            // Iterate over path and update sizes
            for level in 0..path.len() {
                let full_path = path[..=level].join("/");
                *sizes.entry(full_path).or_insert(0) += size;
            }
        }
        _ => (),
    }
    (path, sizes)
}

fn process_input(input: &str) -> HashMap<String, u32> {
    input
        .lines()
        .fold(
            (Vec::<String>::new(), HashMap::<String, u32>::new()),
            |(path, sizes), line| process_line(line, path, sizes),
        )
        .1
}

pub fn part_one(input: &str) -> Option<u32> {
    let sizes = process_input(input);
    Some(
        sizes
            .iter()
            .filter(|&(_, value)| *value <= 100000)
            .map(|(_, value)| *value)
            .sum::<u32>(),
    )
}

pub fn part_two(input: &str) -> Option<u32> {
    let sizes = process_input(input);
    let current_total = *sizes.get("/").unwrap();
    sizes
        .get(
            sizes
                .iter()
                .filter(|(_, value)| current_total - *value <= 70000000 - 30000000)
                .min_by(|left, right| left.1.cmp(right.1))
                .map(|(key, _)| key)
                .unwrap(),
        )
        .copied()
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 7);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 7);
        assert_eq!(part_one(&input), Some(95437));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 7);
        assert_eq!(part_two(&input), Some(24933642));
    }
}
