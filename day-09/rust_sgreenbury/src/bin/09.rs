use advent_of_code::helpers::wait;
use hashbrown::HashSet;
use itertools::Itertools;
use std::{fmt::Display, hash::Hash, ops::Sub};

#[derive(Clone, Copy, Debug, Hash, PartialEq, Eq)]
enum Direction {
    Up,
    Down,
    Right,
    Left,
    UpRight,
    DownRight,
    UpLeft,
    DownLeft,
    None,
}

fn read_instructions(input: &str) -> Vec<Direction> {
    input
        .lines()
        .fold(Vec::<Direction>::new(), |mut acc, line| {
            let (direction, repeats) = line.split_once(' ').unwrap();
            let direction = match direction {
                "U" => Direction::Up,
                "D" => Direction::Down,
                "R" => Direction::Right,
                "L" => Direction::Left,
                _ => panic!("Unknown direction."),
            };
            acc.extend(std::iter::repeat(direction).take(repeats.parse().unwrap()));
            acc
        })
}

#[derive(Copy, Clone, Hash, PartialEq, PartialOrd, Eq, Ord, Debug)]
struct Point {
    x: i32,
    y: i32,
}
impl Point {
    fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }
    fn update(&mut self, direction: Direction) {
        match direction {
            Direction::Up => self.y += 1,
            Direction::Down => self.y -= 1,
            Direction::Left => self.x -= 1,
            Direction::Right => self.x += 1,
            Direction::None => (),
            Direction::UpRight => {
                self.x += 1;
                self.y += 1
            }
            Direction::DownRight => {
                self.x += 1;
                self.y -= 1
            }
            Direction::DownLeft => {
                self.x -= 1;
                self.y -= 1
            }
            Direction::UpLeft => {
                self.x -= 1;
                self.y += 1
            }
        }
    }
    fn next_direction(&self, other: &Point) -> Direction {
        match *other - *self {
            Point { x, y } if x.abs() < 2 && y.abs() < 2 => Direction::None,
            Point { x, y } if x == -2 && y == 0 => Direction::Left,
            Point { x, y } if x == 2 && y == 0 => Direction::Right,
            Point { x, y } if x == 0 && y == 2 => Direction::Up,
            Point { x, y } if x == 0 && y == -2 => Direction::Down,
            Point { x, y } if (x >= 1 && y == 2) || (x == 2 && y >= 1) => Direction::UpRight,
            Point { x, y } if (x == 2 && y <= -1) || (x >= 1 && y == -2) => Direction::DownRight,
            Point { x, y } if (x == -2 && y <= -1) || (x <= -1 && y == -2) => Direction::DownLeft,
            Point { x, y } if (x == -2 && y >= 1) || (x <= -1 && y == 2) => Direction::UpLeft,
            _ => panic!("Gap too big!"),
        }
    }
}
impl Sub for Point {
    type Output = Self;
    fn sub(self, other: Self) -> Self {
        Self {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

impl Display for Point {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "({}, {})", self.x, self.y)?;
        Ok(())
    }
}

fn print_knots(knots: &[Point]) {
    let max_x = knots.iter().map(|knot| knot.x).max().unwrap();
    let min_x = knots.iter().map(|knot| knot.x).min().unwrap();
    let max_y = knots.iter().map(|knot| knot.y).max().unwrap();
    let min_y = knots.iter().map(|knot| knot.y).min().unwrap();
    let buffer = 4;
    let width = (max_x - min_x + 1 + buffer) as usize;
    let height = (max_y - min_y + 1 + buffer) as usize;
    let mut grid = vec![vec!['.'; width]; height];
    for (i, knot) in knots.iter().enumerate() {
        grid[(knot.y - min_y + buffer / 2) as usize][(knot.x - min_x + buffer / 2) as usize] =
            char::from_digit(i as u32, 10).unwrap();
    }
    for y in 0..grid.len() {
        for x in 0..grid[y].len() {
            print!("{}", grid[grid.len() - y - 1][x]);
        }
        println!();
    }
    println!();
}

pub fn part_one(input: &str) -> Option<usize> {
    let mut visited = HashSet::<Point>::new();
    let head = Point::new(0, 0);
    let tail = Point::new(0, 0);
    visited.insert(tail);
    Some(
        read_instructions(input)
            .iter()
            .fold(
                (visited, head, tail),
                |(mut visited, mut head, mut tail), instruction| {
                    head.update(*instruction);
                    tail.update(tail.next_direction(&head));
                    visited.insert(tail);
                    (visited, head, tail)
                },
            )
            .0
            .len(),
    )
}

const STEP_THROUGH: bool = false;

pub fn part_two(input: &str) -> Option<usize> {
    let mut visited: HashSet<Point> = HashSet::new();
    let mut knots = [Point::new(0, 0); 10];
    for instruction in read_instructions(input) {
        knots[0].update(instruction);
        for (head_idx, tail_idx) in (0..10usize).into_iter().tuple_windows() {
            knots[tail_idx].update(knots[tail_idx].next_direction(&knots[head_idx]));
        }
        if STEP_THROUGH {
            print_knots(&knots);
            wait();
        }
        visited.insert(*knots.last().unwrap());
    }
    Some(visited.len())
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 9);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 9);
        assert_eq!(part_one(&input), Some(13));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 9);
        assert_eq!(part_two(&input), Some(1));
    }
}
