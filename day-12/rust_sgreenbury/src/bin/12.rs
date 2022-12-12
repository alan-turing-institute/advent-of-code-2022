use hashbrown::HashSet;
use itertools::Itertools;
use std::{collections::VecDeque, fmt::Display};

#[derive(Clone, Copy, Debug, Hash, PartialEq, Eq)]
enum Direction {
    Up,
    Down,
    Right,
    Left,
}

#[derive(Copy, Clone, Hash, PartialEq, PartialOrd, Eq, Ord, Debug)]
struct Point {
    x: usize,
    y: usize,
}
impl Display for Point {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "({}, {})", self.x, self.y)?;
        Ok(())
    }
}
impl Point {
    fn new(x: usize, y: usize) -> Self {
        Self { x, y }
    }
    fn adjacent(&self, direction: Direction, grid: &[Vec<char>]) -> Option<Point> {
        match direction {
            Direction::Up => {
                if self.y + 1 < grid.len() {
                    Some(Point {
                        y: self.y + 1,
                        ..*self
                    })
                } else {
                    None
                }
            }
            Direction::Down => {
                if self.y > 0 {
                    Some(Point {
                        y: self.y - 1,
                        ..*self
                    })
                } else {
                    None
                }
            }
            Direction::Left => {
                if self.x > 0 {
                    Some(Point {
                        x: self.x - 1,
                        ..*self
                    })
                } else {
                    None
                }
            }
            Direction::Right => {
                if self.x + 1 < grid[self.y].len() {
                    Some(Point {
                        x: self.x + 1,
                        ..*self
                    })
                } else {
                    None
                }
            }
        }
    }
}

fn read_map(input: &str) -> Vec<Vec<char>> {
    input
        .lines()
        .map(|line| line.chars().collect_vec())
        .collect_vec()
}

fn get_source(grid: &[Vec<char>], source_char: char) -> Option<Point> {
    for (y, row) in grid.iter().enumerate() {
        for (x, c) in row.iter().enumerate() {
            if *c == source_char {
                return Some(Point::new(x, y));
            }
        }
    }
    None
}

fn char_to_height(c: char) -> i32 {
    if c == 'S' {
        'a' as i32
    } else if c == 'E' {
        'z' as i32 + 1
    } else {
        c as i32
    }
}

#[derive(Clone, Copy)]
enum WalkType {
    Up,
    Down,
}

fn accessible(neighbour_char: char, point_char: char, walk_type: WalkType) -> bool {
    let point_height = char_to_height(point_char);
    let neighbour_height = char_to_height(neighbour_char);
    match walk_type {
        WalkType::Up => neighbour_height - point_height <= 1,
        WalkType::Down => neighbour_height - point_height >= -1,
    }
}

fn get_path_length(
    grid: &[Vec<char>],
    source_char: char,
    target_char: char,
    walk_type: WalkType,
) -> Option<u32> {
    // Perform BFS for first target from source
    let mut queue = VecDeque::<(Point, u32)>::new();
    let mut visited = HashSet::<Point>::new();
    let mut explored = HashSet::<Point>::new();
    let source_point = get_source(grid, source_char).unwrap();
    queue.push_back((source_point, 0));
    visited.insert(source_point);
    while let Some((current, path_length)) = queue.pop_front() {
        for direction in [
            Direction::Up,
            Direction::Down,
            Direction::Left,
            Direction::Right,
        ] {
            let neighbour = current.adjacent(direction, grid);
            if let Some(neighbour) = neighbour {
                let point_char = grid[current.y][current.x];
                let neighbour_char = grid[neighbour.y][neighbour.x];
                if grid[neighbour.y][neighbour.x] == target_char
                    && accessible(neighbour_char, point_char, walk_type)
                {
                    return Some(path_length + 1);
                } else if !visited.contains(&neighbour)
                    && !explored.contains(&neighbour)
                    && accessible(neighbour_char, point_char, walk_type)
                {
                    queue.push_back((neighbour, path_length + 1));
                    visited.insert(neighbour);
                }
            }
        }
        explored.insert(current);
        visited.remove(&current);
    }
    None
}

pub fn part_one(input: &str) -> Option<u32> {
    get_path_length(&read_map(input), 'S', 'E', WalkType::Up)
}

pub fn part_two(input: &str) -> Option<u32> {
    get_path_length(&read_map(input), 'E', 'a', WalkType::Down)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 12);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 12);
        assert_eq!(part_one(&input), Some(31));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 12);
        assert_eq!(part_two(&input), Some(29));
    }
}
