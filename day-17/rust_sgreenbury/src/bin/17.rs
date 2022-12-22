const WIDTH: usize = 9;
const HEIGHT: usize = 10000;
use advent_of_code::helpers::{wait, Point};
use itertools::Itertools;
use lazy_static::lazy_static;
use std::hash::Hash;
use std::ops::Sub;

// Comment out for non-interactive mode
const VERBOSE: bool = false;
const VVERBOSE: bool = false;

// Uncomment for interactive print mode
// const VERBOSE: bool = true;
// const VVERBOSE: bool = true;

type UPoint = Point<usize>;
type IPoint = Point<i32>;
type GridU8 = [[u8; WIDTH]; HEIGHT];

#[derive(Debug, Clone, Copy)]
enum Direction {
    Left,
    Right,
    Down,
}

fn ipoint_to_upoint(p: IPoint) -> UPoint {
    UPoint::new(p.x.max(0) as usize, p.y.max(0) as usize)
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
enum ShapeType {
    FourByOne,
    OneByFour,
    Cross,
    Bracket,
    Square,
}
#[derive(Debug, PartialEq, Eq, Clone, PartialOrd, Ord)]
struct Shape {
    shape_type: ShapeType,
    location: IPoint,
}

lazy_static! {
    // Points
    static ref FBO_PS: Vec<IPoint> = vec![
        IPoint::new(0, 0),
        IPoint::new(1, 0),
        IPoint::new(2, 0),
        IPoint::new(3, 0)
    ];
    static ref OBF_PS: Vec<IPoint> = vec![
        IPoint::new(0, 0),
        IPoint::new(0, 1),
        IPoint::new(0, 2),
        IPoint::new(0, 3)
    ];
    static ref CROSS_PS: Vec<IPoint> = vec![
        IPoint::new(1, 0),
        IPoint::new(0, 1),
        IPoint::new(1, 1),
        IPoint::new(1, 2),
        IPoint::new(2, 1),
    ];
    static ref BRACKET_PS: Vec<IPoint> = vec![
        IPoint::new(0, 0),
        IPoint::new(1, 0),
        IPoint::new(2, 0),
        IPoint::new(2, 1),
        IPoint::new(2, 2),
    ];
    static ref SQUARE_PS: Vec<IPoint> = vec![
        IPoint::new(0, 0),
        IPoint::new(1, 0),
        IPoint::new(0, 1),
        IPoint::new(1, 1)
    ];

    // Left neighbours
    static ref FBO_LNS: Vec<IPoint> = vec![IPoint::new(-1, 0)];
    static ref OBF_LNS: Vec<IPoint> = vec![
        IPoint::new(-1, 0),
        IPoint::new(-1, 1),
        IPoint::new(-1, 2),
        IPoint::new(-1, 3),
    ];
    static ref CROSS_LNS: Vec<IPoint> = vec![
        IPoint::new(-1, 1),
        IPoint::new(0, 2),
        IPoint::new(0, 0),
    ];
    static ref BRACKET_LNS: Vec<IPoint> = vec![
        IPoint::new(-1, 0),
        IPoint::new(1, 1),
        IPoint::new(1, 2),
    ];
    static ref SQUARE_LNS: Vec<IPoint> = vec![IPoint::new(-1, 0), IPoint::new(-1, 1)];

    // Right neighbours
    static ref FBO_RNS: Vec<IPoint> = vec![IPoint::new(4, 0)];
    static ref OBF_RNS: Vec<IPoint> = vec![
        IPoint::new(1, 0),
        IPoint::new(1, 1),
        IPoint::new(1, 2),
        IPoint::new(1, 3),
    ];
    static ref CROSS_RNS: Vec<IPoint> = vec![
        IPoint::new(3, 1),
        IPoint::new(2, 2),
        IPoint::new(2, 0),
    ];
    static ref BRACKET_RNS: Vec<IPoint> = vec![
        IPoint::new(3, 0),
        IPoint::new(3, 1),
        IPoint::new(3, 2),
    ];
    static ref SQUARE_RNS: Vec<IPoint> = vec![IPoint::new(2, 0), IPoint::new(2, 1)];

    // Bottom neighbours
    static ref FBO_BNS: Vec<IPoint> = vec![
        IPoint::new(0, -1),
        IPoint::new(1, -1),
        IPoint::new(2, -1),
        IPoint::new(3, -1),
    ];
    static ref OBF_BNS: Vec<IPoint> = vec![IPoint::new(0, -1)];
    static ref CROSS_BNS: Vec<IPoint> = vec![
        IPoint::new(1, -1),
        IPoint::new(0, 0),
        IPoint::new(2, 0),
    ];
    static ref BRACKET_BNS: Vec<IPoint> = vec![
        IPoint::new(0, -1),
        IPoint::new(1, -1),
        IPoint::new(2, -1),
    ];
    static ref SQUARE_BNS: Vec<IPoint> = vec![IPoint::new(0, -1), IPoint::new(1, -1)];
}

impl Shape {
    fn height(&self) -> usize {
        match self.shape_type {
            ShapeType::FourByOne => 1,
            ShapeType::OneByFour => 4,
            ShapeType::Cross => 3,
            ShapeType::Bracket => 3,
            ShapeType::Square => 2,
        }
    }
    fn id(&self) -> u8 {
        match self.shape_type {
            ShapeType::FourByOne => 1,
            ShapeType::OneByFour => 2,
            ShapeType::Cross => 3,
            ShapeType::Bracket => 4,
            ShapeType::Square => 5,
        }
    }
    fn new(height: usize, shape_type: ShapeType) -> Self {
        Shape {
            shape_type,
            location: IPoint::new(3, (height + 4).try_into().unwrap()),
        }
    }
    fn points(&self) -> &[IPoint] {
        match self.shape_type {
            ShapeType::FourByOne => &FBO_PS,
            ShapeType::OneByFour => &OBF_PS,
            ShapeType::Cross => &CROSS_PS,
            ShapeType::Bracket => &BRACKET_PS,
            ShapeType::Square => &SQUARE_PS,
        }
    }

    fn right_neighbours(&self) -> &[IPoint] {
        match self.shape_type {
            ShapeType::FourByOne => &FBO_RNS,
            ShapeType::OneByFour => &OBF_RNS,
            ShapeType::Cross => &CROSS_RNS,
            ShapeType::Bracket => &BRACKET_RNS,
            ShapeType::Square => &SQUARE_RNS,
        }
    }
    fn left_neighbours(&self) -> &[IPoint] {
        match self.shape_type {
            ShapeType::FourByOne => &FBO_LNS,
            ShapeType::OneByFour => &OBF_LNS,
            ShapeType::Cross => &CROSS_LNS,
            ShapeType::Bracket => &BRACKET_LNS,
            ShapeType::Square => &SQUARE_LNS,
        }
    }
    fn bottom_neighbours(&self) -> &[IPoint] {
        match self.shape_type {
            ShapeType::FourByOne => &FBO_BNS,
            ShapeType::OneByFour => &OBF_BNS,
            ShapeType::Cross => &CROSS_BNS,
            ShapeType::Bracket => &BRACKET_BNS,
            ShapeType::Square => &SQUARE_BNS,
        }
    }
    fn update_shape(&mut self, direction: &Direction, grid: &mut GridU8) -> bool {
        match direction {
            Direction::Left => {
                for neighbour in self
                    .left_neighbours()
                    .iter()
                    .map(|p| ipoint_to_upoint(*p + self.location))
                {
                    if grid[neighbour.y][neighbour.x] != 0 {
                        return false;
                    }
                }
                self.fill_grid(0, grid);
                self.location = self.location + IPoint::new(-1, 0);
                self.fill_grid(self.id(), grid);
                true
            }
            Direction::Right => {
                for neighbour in self
                    .right_neighbours()
                    .iter()
                    .map(|p| ipoint_to_upoint(*p + self.location))
                {
                    if grid[neighbour.y][neighbour.x] != 0 {
                        return false;
                    }
                }
                self.fill_grid(0, grid);
                self.location = self.location + IPoint::new(1, 0);
                self.fill_grid(self.id(), grid);
                true
            }
            Direction::Down => {
                for neighbour in self
                    .bottom_neighbours()
                    .iter()
                    .map(|p| ipoint_to_upoint(*p + self.location))
                {
                    if grid[neighbour.y][neighbour.x] != 0 {
                        return false;
                    }
                }
                self.fill_grid(0, grid);
                self.location = self.location + IPoint::new(0, -1);
                self.fill_grid(self.id(), grid);
                true
            }
        }
    }

    fn fill_grid(&self, id: u8, grid: &mut GridU8) {
        self.points()
            .iter()
            .map(|p| ipoint_to_upoint(*p + self.location))
            .for_each(|p| grid[p.y][p.x] = id)
    }
    fn next(&self) -> ShapeType {
        match self.shape_type {
            ShapeType::FourByOne => ShapeType::Cross,
            ShapeType::Cross => ShapeType::Bracket,
            ShapeType::Bracket => ShapeType::OneByFour,
            ShapeType::OneByFour => ShapeType::Square,
            ShapeType::Square => ShapeType::FourByOne,
        }
    }
    fn max_height(&self, max: usize) -> usize {
        (self.location.y as usize + self.height() - 1).max(max)
    }
}

// Initialize grid with u8
fn make_grid() -> GridU8 {
    let mut grid = [[0; WIDTH]; HEIGHT];
    (0..WIDTH).for_each(|idx| {
        grid[0][idx] = 8;
    });
    (0..HEIGHT).for_each(|i| {
        grid[i][0] = 7;
        grid[i][WIDTH - 1] = 7;
    });
    grid[0][0] = 9;
    grid[0][WIDTH - 1] = 9;
    grid
}

// Convert u8 grid to string
fn grid_to_string(grid: &GridU8) -> String {
    let max_height = grid
        .iter()
        .enumerate()
        .map(|(idx, row)| {
            if row[1..WIDTH - 1].iter().map(|&value| value != 0).any(|x| x) {
                idx
            } else {
                0
            }
        })
        .max()
        .unwrap();

    grid.iter()
        .enumerate()
        .filter(|(idx, _)| idx < &(max_height + 1))
        .map(|(idx, row)| {
            let row_as_string = row.map(|c| {
                if c == 7 {
                    '|'
                } else if c == 8 {
                    '-'
                } else if c == 9 {
                    '+'
                } else if c == 0 {
                    '.'
                } else {
                    char::from_digit(c as u32, 10).unwrap()
                }
            });
            row_as_string.iter().collect::<String>()
                + &format!("  {:>04}", &(idx).to_string().as_str())
        })
        .rev()
        .collect_vec()
        .iter()
        .join("\n")
}

fn get_repeat<T: std::ops::Sub + Clone + Copy + Eq>(v: &[T], max_size: usize) -> Option<usize>
where
    <T as Sub>::Output: Hash,
    <T as Sub>::Output: Eq,
    <T as Sub>::Output: Clone,
{
    // Find a repeat (cylce) in the series of differences for expanding window size
    let mut cycle_length = 1;
    while cycle_length < max_size.min(v.len() / 2) {
        if v.windows(cycle_length + 1)
            .rev()
            .map(|window| *window.last().unwrap() - *window.first().unwrap())
            .unique()
            .at_most_one()
            .is_ok()
        {
            return Some(cycle_length);
        }
        cycle_length += 1;
    }
    None
}

// Main simulation
fn run_simulation(input: &str, shape_count_max: usize) -> Option<usize> {
    // Make grid
    let mut grid = make_grid();

    // Load jets
    let jets = input
        .trim()
        .chars()
        .collect_vec()
        .into_iter()
        .map(|c| {
            if c == '<' {
                Direction::Left
            } else {
                Direction::Right
            }
        })
        .collect_vec();

    // Max height variable
    let mut max_height: usize = 0;

    // Generate new shape
    let mut shape = Shape::new(max_height, ShapeType::FourByOne);

    // Initialize grid
    shape.fill_grid(0, &mut grid);

    // Cycle idx
    let mut idx = 0;

    // Shapes used
    let mut shape_count = 0;

    // Storing heights at each shape
    let mut heights = Vec::<usize>::new();

    // Run simulation
    let height_at_max = loop {
        idx %= jets.len();
        let direction = &jets[idx];

        let moved = shape.update_shape(direction, &mut grid);
        if VVERBOSE {
            println!("Moved {:?}? {}", direction, moved);
            println!("{}", grid_to_string(&grid));
            wait();
        }
        // Down part
        let moved = shape.update_shape(&Direction::Down, &mut grid);
        if VVERBOSE {
            println!("Moved {:?}? {}", Direction::Down, moved);
            println!("{}", grid_to_string(&grid));
            wait();
        }

        // Handle whether shape moved or stopped
        shape = if !moved {
            shape.fill_grid(shape.id(), &mut grid);
            shape_count += 1;

            if VVERBOSE {
                println!("{}", grid_to_string(&grid));
                println!("{:?}", shape);
                wait();
            }

            max_height = shape.max_height(max_height);
            heights.push(max_height);

            if shape_count == shape_count_max {
                break Some(*heights.last().unwrap());
            }

            // Try to find cycle
            if max_height > HEIGHT - Shape::new(max_height, shape.next()).height() - 2 {
                // Only keep most recent heights to remove burn-in
                if heights.len() > HEIGHT / 2 {
                    // Drop proportion of fron with non-cyclic heights
                    heights.drain(0..HEIGHT / 10);
                }
                // Identify at least one complete repeat of diffs from most recent heights
                // back to a maximum of half the heights
                if let Some(cycle_length) = get_repeat(&heights, HEIGHT / 2) {
                    let cycle_heights = heights
                        .iter()
                        .rev()
                        .take(cycle_length + 1)
                        .rev()
                        .collect_vec();
                    let diffs = cycle_heights
                        .windows(2)
                        .map(|window| *window.last().unwrap() - *window.first().unwrap())
                        .collect_vec();
                    let height_per_cycle = diffs.iter().sum::<usize>();
                    let shapes_remaining = shape_count_max - shape_count;
                    let cycles_remaining = shapes_remaining / cycle_length;
                    let shapes_remainder = shapes_remaining % cycle_length;
                    let total_height = *heights.last().unwrap()
                        + cycles_remaining * height_per_cycle
                        + diffs[..shapes_remainder].iter().sum::<usize>();

                    println!("Cycle length: {}", cycle_length);
                    println!("Current shapes: {}", shape_count);
                    println!("Current height: {}", heights.last().unwrap());
                    println!("Shapes remaining: {}", shapes_remaining);
                    println!("Cycles remaining: {}", cycles_remaining);
                    println!("Shapes remainder: {}", shapes_remainder);
                    println!("Height per cycle: {}", height_per_cycle);
                    break Some(total_height);
                } else {
                    panic!(
                        "No cycle found and height will be too large for grid of height {HEIGHT}!"
                    );
                }
            }
            if VERBOSE || VVERBOSE {
                println!("Height: {}", max_height);
                println!("Shapes stopped: {}", shape_count);
            }
            let new_shape = Shape::new(max_height, shape.next());
            new_shape.fill_grid(new_shape.id(), &mut grid);
            if VERBOSE || VVERBOSE {
                println!("{}", grid_to_string(&grid));
                wait();
            }
            new_shape
        } else {
            shape
        };
        idx += 1;
    };

    height_at_max
}

pub fn part_one(input: &str) -> Option<usize> {
    run_simulation(input, 2022)
}

pub fn part_two(input: &str) -> Option<usize> {
    run_simulation(input, 1000000000000)
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 17);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_repeats() {
        // Test identifying cycle of montonic differences
        let diffs = [0, 2, 9, 4, 5, 6, 4, 5];
        let v: Vec<u64> = (0..2000u64)
            .step_by(5)
            .collect_vec()
            .iter_mut()
            .enumerate()
            .map(|(idx, el)| *el + diffs[idx % diffs.len()])
            .collect_vec();
        let cycle_length = get_repeat(&v, 50);
        assert_eq!(Some(diffs.len()), cycle_length);

        // Single step case
        let v = (0..2000).collect_vec();
        let cycle_length = get_repeat(&v, 500);
        assert_eq!(Some(1), cycle_length);
    }

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 17);
        assert_eq!(part_one(&input), Some(3068));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 17);
        assert_eq!(part_two(&input), Some(1514285714288));
    }
}
