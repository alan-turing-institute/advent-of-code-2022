use hashbrown::HashSet;
use itertools::Itertools;

fn read_grid(input: &str) -> Vec<Vec<u32>> {
    input
        .lines()
        .map(|line| line.chars().map(|c| c.to_digit(10).unwrap()).collect_vec())
        .collect_vec()
}

#[derive(Copy, Clone, Hash, PartialEq, PartialOrd, Eq, Ord, Debug)]
struct Point {
    x: usize,
    y: usize,
}
impl Point {
    fn new(x: usize, y: usize) -> Self {
        Self { x, y }
    }
}
#[derive(Debug, Clone, Copy)]
enum Direction {
    Right,
    Left,
    Down,
    Up,
    None,
}

#[derive(Debug, Clone, Copy)]
struct Line {
    start: Point,
    current: Option<Point>,
    end: Point,
    direction: Direction,
    length: usize,
}

impl Line {
    fn new(start: &Point, end: &Point) -> Self {
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
            start: *start,
            current: Some(*start),
            end: *end,
            direction,
            length,
        }
    }
    fn length(&self) -> usize {
        self.length
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

fn score_line(grid: &[Vec<u32>], mut line: Line, mut visible: HashSet<Point>) -> HashSet<Point> {
    let point = line.next().unwrap();
    let mut current_max: u32 = grid[point.y][point.x];
    for point in line {
        if grid[point.y][point.x] > current_max {
            visible.insert(Point::new(point.x, point.y));
            current_max = grid[point.y][point.x];
        }
    }
    visible
}

fn scenic_score_line(line: &Line, grid: &[Vec<u32>]) -> u32 {
    for (idx, line_point) in line.enumerate().skip(1) {
        if grid[line_point.y][line_point.x] >= grid[line.start.y][line.start.x] {
            return idx as u32;
        }
    }
    line.length() as u32
}

fn scenic_score(point: &Point, grid: &Vec<Vec<u32>>) -> u32 {
    let mut score = 1;
    let lines = [
        Line::new(point, &Point::new(grid.len() - 1, point.y)),
        Line::new(point, &Point::new(0, point.y)),
        Line::new(point, &Point::new(point.x, grid.len() - 1)),
        Line::new(point, &Point::new(point.x, 0)),
    ];
    for line in lines {
        score *= scenic_score_line(&line, grid);
    }
    score
}

pub fn part_one(input: &str) -> Option<u32> {
    let grid = read_grid(input);
    let mut visible: HashSet<Point> = HashSet::new();
    for idx in 1..grid.len() - 1 {
        for line in [
            Line::new(&Point::new(0, idx), &Point::new(grid.len() - 2, idx)),
            Line::new(&Point::new(grid.len() - 1, idx), &Point::new(1, idx)),
            Line::new(&Point::new(idx, 0), &Point::new(idx, grid.len() - 2)),
            Line::new(&Point::new(idx, grid.len() - 1), &Point::new(idx, 1)),
        ] {
            visible = score_line(&grid, line, visible);
        }
    }
    Some(visible.len() as u32 + (grid.len() as u32 - 1) * 4)
}

pub fn part_two(input: &str) -> Option<u32> {
    let grid = read_grid(input);
    (1..grid.len() - 1)
        .cartesian_product(1..grid.len() - 1)
        .map(|(x, y)| scenic_score(&Point::new(x, y), &grid))
        .max()
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 8);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 8);
        assert_eq!(part_one(&input), Some(21));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 8);
        assert_eq!(part_two(&input), Some(8));
    }
}
