use std::ops::Sub;
use hashbrown::HashSet;
use itertools::Itertools;

// Smaller dimensions ok for test cases
// const WIDTH: usize = 50;
// const HEIGHT: usize = 20;
// const POINT_OFFSET: Point = Point{x: 480, y: 0};

// Minimal dimensions for inputs
const WIDTH: usize = 330;
const HEIGHT: usize = 170;
const OFFSET: Point = Point { x: 335, y: 0 };

#[derive(Copy, Clone, Hash, PartialEq, PartialOrd, Eq, Ord, Debug)]
pub struct Point {
    pub x: usize,
    pub y: usize,
}
impl Point {
    pub fn new(x: usize, y: usize) -> Self {
        Self { x, y }
    }
    pub fn offet(&self, offset: &Point) -> Point {
        *self - *offset
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

#[derive(Debug, Clone, Copy)]
pub enum Direction {
    Right,
    Left,
    Down,
    Up,
    None,
}

#[derive(Debug, Clone, Copy)]
pub struct Line {
    _start: Point,
    current: Option<Point>,
    end: Point,
    direction: Direction,
    _length: usize,
}

impl From<(&str, &str)> for Point {
    fn from(tuple: (&str, &str)) -> Self {
        Point::new(
            tuple.0.parse::<usize>().unwrap(),
            tuple.1.parse::<usize>().unwrap(),
        )
    }
}

impl Line {
    pub fn new(start: &Point, end: &Point) -> Self {
        let (direction, length) = if start.x == end.x && start.y < end.y {
            (Direction::Down, end.y - start.y)
        } else if start.x == end.x && start.y > end.y {
            (Direction::Up, start.y - end.y)
        } else if start.x < end.x && start.y == end.y {
            (Direction::Right, end.x - start.x)
        } else if start.x > end.x && start.y == end.y {
            (Direction::Left, start.x - end.x)
        } else if start == end {
            (Direction::None, 0)
        } else {
            panic!("Diagonal!")
        };
        Self {
            _start: *start,
            current: Some(*start),
            end: *end,
            direction,
            _length: length,
        }
    }
}

impl Iterator for Line {
    type Item = Point;
    fn next(&mut self) -> Option<Self::Item> {
        let current = self.current;
        if let Some(ref point) = self.current {
            self.current = match self.direction {
                Direction::Right if point.x < self.end.x => Some(Point::new(point.x + 1, point.y)),
                Direction::Right => None,
                Direction::Left if point.x > self.end.x => Some(Point::new(point.x - 1, point.y)),
                Direction::Left => None,
                Direction::Down if point.y < self.end.y => Some(Point::new(point.x, point.y + 1)),
                Direction::Down => None,
                Direction::Up if point.y > self.end.y => Some(Point::new(point.x, point.y - 1)),
                Direction::Up => None,
                Direction::None => None,
            };
            current
        } else {
            None
        }
    }
}

fn grid_to_string(grid: &[[char; WIDTH]; HEIGHT]) -> String {
    grid.iter()
        .map(|row| {
            let row_as_string = row.map(|c| {
                if c == '#' {
                    '#'
                } else if c == '+' {
                    '+'
                } else {
                    '.'
                }
            });
            row_as_string.iter().collect::<String>()
        })
        .collect_vec()
        .iter()
        .join("\n")
}

fn read_input(input: &str) -> [[char; WIDTH]; HEIGHT] {
    let mut grid = [['.'; WIDTH]; HEIGHT];
    input.lines().for_each(|line| {
        let points_on_lines = line.split(" -> ").collect_vec();
        points_on_lines
            .into_iter()
            .tuple_windows()
            .for_each(|(start_str, end_str)| {
                let start = Point::from(start_str.split_once(',').unwrap()).offet(&OFFSET);
                let end = Point::from(end_str.split_once(',').unwrap()).offet(&OFFSET);
                let point_line = Line::new(&start, &end);
                point_line.into_iter().for_each(|point| {
                    grid[point.y][point.x] = '#';
                })
            })
    });
    grid
}

fn get_next_point(point: Point, grid: &[[char; WIDTH]; HEIGHT]) -> Option<Point> {
    match grid[point.y + 1][point.x] {
        _ if grid[point.y + 1][point.x] == '.' => Some(Point::new(point.x, point.y + 1)),
        _ if grid[point.y + 1][point.x - 1] == '.' => Some(Point::new(point.x - 1, point.y + 1)),
        _ if grid[point.y + 1][point.x + 1] == '.' => Some(Point::new(point.x + 1, point.y + 1)),
        _ => None,
    }
}

fn new_grain() -> Point {
    Point::new(500, 0).offet(&OFFSET)
}

#[derive(PartialEq, Eq)]
enum Part {
    One,
    Two,
}

fn update_grid(current: Option<&Point>, next_point: &Point, grid: &mut [[char; WIDTH]; HEIGHT]) {
    if let Some(point) = current {
        grid[point.y][point.x] = '.';
    }
    grid[next_point.y][next_point.x] = '+';
}

fn run(grid: &mut [[char; WIDTH]; HEIGHT], part: Part) -> Option<usize> {
    let mut sand_pile = HashSet::<Point>::new();
    let mut current = new_grain();
    update_grid(None, &current, grid);
    loop {
        if let Some(next_point) = get_next_point(current, grid) {
            if part == Part::One && current.y == HEIGHT - 2 {
                break;
            }
            update_grid(Some(&current), &next_point, grid);
            current = next_point;
        } else {
            sand_pile.insert(current);
            if part == Part::Two && current == new_grain() {
                break;
            }
            current = new_grain();
        }
    }
    println!("{}\n", grid_to_string(grid));
    Some(sand_pile.len())
}

pub fn part_one(input: &str) -> Option<usize> {
    // Load grid
    let mut grid = read_input(input);
    // Run simulation
    run(&mut grid, Part::One)
}

pub fn part_two(input: &str) -> Option<usize> {
    // Load grid
    let mut grid = read_input(input);
    // Get max y
    let max_y = grid
        .iter()
        .enumerate()
        .map(|(idx, row)| (idx, row.iter().map(|x| *x == '#').any(|x| x)))
        .filter(|(_, b)| *b)
        .last()
        .unwrap()
        .0
        + 2;
    // Add line for floor
    Line::new(&Point::new(0, max_y), &Point::new(WIDTH - 1, max_y))
        .into_iter()
        .for_each(|point| grid[point.y][point.x] = '#');
    // Run simulation
    run(&mut grid, Part::Two)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 14);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 14);
        assert_eq!(part_one(&input), Some(24));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 14);
        assert_eq!(part_two(&input), Some(93));
    }
}
