use advent_of_code::helpers::wait;
use hashbrown::{HashMap, HashSet};
use itertools::Itertools;
use lazy_static::lazy_static;
use std::{
    collections::VecDeque,
    hash::{Hash, Hasher},
    ops::{Add, Sub},
};

// Comment for verbose output
const VERBOSE: bool = false;
// Uncomment for stepped verbose ouput
// const VERBOSE: bool = true;

lazy_static! {
    // Sides
    static ref BOTTOM: Vec<Point3D>= vec![
        Point3D::new(0, 0, 0),
        Point3D::new(1, 0, 0),
        Point3D::new(0, 1, 0),
        Point3D::new(1, 1, 0),
    ];
    static ref TOP: Vec<Point3D> = vec![
        Point3D::new(0, 0, 1),
        Point3D::new(1, 0, 1),
        Point3D::new(0, 1, 1),
        Point3D::new(1, 1, 1),
    ];
    static ref LEFT: Vec<Point3D> = vec![
        Point3D::new(0, 0, 0),
        Point3D::new(0, 1, 0),
        Point3D::new(0, 0, 1),
        Point3D::new(0, 1, 1),
    ];
    static ref RIGHT: Vec<Point3D> = vec![
        Point3D::new(1, 0, 0),
        Point3D::new(1, 1, 0),
        Point3D::new(1, 0, 1),
        Point3D::new(1, 1, 1),
    ];
    static ref BACK: Vec<Point3D> = vec![
        Point3D::new(0, 0, 0),
        Point3D::new(1, 0, 0),
        Point3D::new(0, 0, 1),
        Point3D::new(1, 0, 1),
    ];
    static ref FRONT: Vec<Point3D> = vec![
        Point3D::new(0, 1, 0),
        Point3D::new(1, 1, 0),
        Point3D::new(0, 1, 1),
        Point3D::new(1, 1, 1),
    ];
    static ref NEIGHBOURS: Vec<Point3D> = vec![
        Point3D::new(1, 0, 0),
        Point3D::new(-1, 0, 0),
        Point3D::new(0, 1, 0),
        Point3D::new(0, -1, 0),
        Point3D::new(0, 0, 1),
        Point3D::new(0, 0, -1),
    ];
    static ref SIDE_TYPES: Vec<SideType> = vec![
            SideType::Left,
            SideType::Right,
            SideType::Bottom,
            SideType::Top,
            SideType::Back,
            SideType::Front,
        ];
}

impl Add for Point3D {
    type Output = Self;
    fn add(self, other: Self) -> Self {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
            z: self.z + other.z,
        }
    }
}

impl Sub for Point3D {
    type Output = Self;
    fn sub(self, other: Self) -> Self {
        Self {
            x: self.x - other.x,
            y: self.y - other.y,
            z: self.z - other.z,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
enum SideType {
    Bottom,
    Top,
    Left,
    Right,
    Back,
    Front,
}
#[derive(Debug, Clone, Copy, Hash, PartialEq, PartialOrd, Eq, Ord)]
struct Point3D {
    x: i8,
    y: i8,
    z: i8,
}

impl Point3D {
    fn new(x: i8, y: i8, z: i8) -> Point3D {
        Self { x, y, z }
    }
    fn neighbours(&self) -> &[Point3D] {
        &NEIGHBOURS
    }
}

#[derive(Debug, Clone, PartialOrd, Ord)]
struct Side {
    anchor: Point3D,
    side_type: SideType,
}

impl Side {
    fn new(anchor: Point3D, side_type: SideType) -> Self {
        Self { anchor, side_type }
    }
}

impl PartialEq for Side {
    fn eq(&self, other: &Self) -> bool {
        (self.anchor + Point3D::new(1, 0, 0) == other.anchor
            && self.side_type == SideType::Right
            && other.side_type == SideType::Left)
            || (self.anchor - Point3D::new(1, 0, 0) == other.anchor
                && self.side_type == SideType::Left
                && other.side_type == SideType::Right)
            || (self.anchor + Point3D::new(0, 0, 1) == other.anchor
                && self.side_type == SideType::Top
                && other.side_type == SideType::Bottom)
            || (self.anchor - Point3D::new(0, 0, 1) == other.anchor
                && self.side_type == SideType::Bottom
                && other.side_type == SideType::Top)
            || (self.anchor + Point3D::new(0, 1, 0) == other.anchor
                && self.side_type == SideType::Front
                && other.side_type == SideType::Back)
            || (self.anchor - Point3D::new(0, 1, 0) == other.anchor
                && self.side_type == SideType::Back
                && other.side_type == SideType::Front)
            || (self.anchor == other.anchor && self.side_type == other.side_type)
    }
}
impl Eq for Side {}

impl Hash for Side {
    fn hash<H: Hasher>(&self, state: &mut H) {
        match self.side_type {
            SideType::Right => {
                SideType::Left.hash(state);
                (self.anchor + Point3D::new(1, 0, 0)).hash(state);
                self.side_type.hash(state);
                self.anchor.hash(state);
            }
            SideType::Left => {
                self.side_type.hash(state);
                self.anchor.hash(state);
                SideType::Right.hash(state);
                (self.anchor - Point3D::new(1, 0, 0)).hash(state)
            }
            SideType::Top => {
                SideType::Bottom.hash(state);
                (self.anchor + Point3D::new(0, 0, 1)).hash(state);
                self.side_type.hash(state);
                self.anchor.hash(state);
            }
            SideType::Bottom => {
                self.side_type.hash(state);
                self.anchor.hash(state);
                SideType::Top.hash(state);
                (self.anchor - Point3D::new(0, 0, 1)).hash(state)
            }
            SideType::Front => {
                SideType::Back.hash(state);
                (self.anchor + Point3D::new(0, 1, 0)).hash(state);
                self.side_type.hash(state);
                self.anchor.hash(state)
            }
            SideType::Back => {
                self.side_type.hash(state);
                self.anchor.hash(state);
                SideType::Front.hash(state);
                (self.anchor - Point3D::new(0, 1, 0)).hash(state)
            }
        }
    }
}

fn read_points(input: &str) -> Vec<Point3D> {
    input
        .lines()
        .map(|line| {
            let mut it = line.split(',');
            let (x, y, z) = (
                it.next().unwrap().parse().unwrap(),
                it.next().unwrap().parse().unwrap(),
                it.next().unwrap().parse().unwrap(),
            );
            Point3D::new(x, y, z)
        })
        .collect_vec()
}

fn get_surface_sides(points: &[Point3D]) -> HashSet<Side> {
    let mut sides = HashMap::<Side, usize>::new();
    for point in points {
        for &side_type in SIDE_TYPES.iter() {
            *sides.entry(Side::new(*point, side_type)).or_insert(0) += 1;
        }
    }
    HashSet::<Side>::from_iter(sides.iter().filter(|(_, &v)| v < 2).map(|(k, _)| k.clone()))
}

fn get_start(surface_sides: &HashSet<Side>) -> Point3D {
    surface_sides
        .iter()
        .max_by(|left, right| right.anchor.cmp(&left.anchor))
        .unwrap()
        .anchor
}

fn update_queue(
    current_point: &Point3D,
    queue: &mut VecDeque<Point3D>,
    queue_hash_set: &mut HashSet<Point3D>,
    points_hash_set: &HashSet<Point3D>,
    visited: &HashSet<Point3D>,
    surface_sides_hash_set_fixed: &HashSet<Side>,
    adjacent_side: bool,
) {
    // Look over all neighbour points of current point
    for neighbour in current_point.neighbours() {
        // Translate neighbour to coordinates from current point
        let translated_neighbour = *current_point + *neighbour;
        if VERBOSE {
            println!("Point: {:?}", current_point);
            println!("Neighbour: {:?}", neighbour);
            println!("Translated: {:?}", translated_neighbour);
            println!("Adjacent: {:?}", adjacent_side);
            println!("Queue: {:?}", queue);
            wait();
        }
        // If filled or neighbour already visited, skip
        if points_hash_set.contains(&translated_neighbour)
            || visited.contains(&translated_neighbour)
            || queue_hash_set.contains(&translated_neighbour)
        {
            continue;
        }
        // Check whether any sides are surface sides of rocks
        for &side_type in SIDE_TYPES.iter() {
            // If neighbour has a side that is surface and not already in queue, add
            if surface_sides_hash_set_fixed.contains(&Side::new(translated_neighbour, side_type))
                && !queue_hash_set.contains(&translated_neighbour)
            {
                queue.push_back(translated_neighbour);
                queue_hash_set.insert(translated_neighbour);
            }
        }
        // Recurse once to explore neighbours of translated neighbour to cover points
        // between points adjacent to surface sides
        if adjacent_side {
            update_queue(
                &translated_neighbour,
                queue,
                queue_hash_set,
                points_hash_set,
                visited,
                surface_sides_hash_set_fixed,
                false,
            );
        }
    }
}

pub fn part_one(input: &str) -> Option<usize> {
    // Read points
    let points = read_points(input);
    // Get sides that only occur once
    let surface_sides = get_surface_sides(&points);
    Some(surface_sides.len())
}

pub fn part_two(input: &str) -> Option<usize> {
    // Set-up
    let points = read_points(input);
    let surface_sides = get_surface_sides(&points);
    let points_hash_set = HashSet::from_iter(points.into_iter());
    let mut surface_sides_remaining = surface_sides.clone();

    // Get a starting point: pick side with largest anchor coords
    let start = get_start(&surface_sides);

    // Make data structures for search
    let mut queue: VecDeque<Point3D> = VecDeque::new();
    let mut queue_hash_set: HashSet<Point3D> = HashSet::new();
    let mut visited: HashSet<Point3D> = HashSet::new();
    queue.push_front(start);

    // Iterate over points
    while let Some(current_point) = queue.pop_front() {
        queue_hash_set.remove(&current_point);

        // If already explored, continue
        if visited.contains(&current_point) {
            continue;
        }
        // If any sides are surfaces ones, remove
        for &side_type in SIDE_TYPES.iter() {
            surface_sides_remaining.remove(&Side::new(current_point, side_type));
        }
        // Add to list of points checked
        visited.insert(current_point);

        // Update queue with neighbours of current point
        update_queue(
            &current_point,
            &mut queue,
            &mut queue_hash_set,
            &points_hash_set,
            &visited,
            &surface_sides,
            true,
        );
    }
    // Return the number of sides discovered
    Some(surface_sides.len() - surface_sides_remaining.len())
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 18);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use std::collections::hash_map::DefaultHasher;

    use super::*;

    #[test]
    fn test_sides() {
        let left = Side::new(Point3D::new(1, 0, 0), SideType::Left);
        let right = Side::new(Point3D::new(0, 0, 0), SideType::Right);
        let bottom = Side::new(Point3D::new(0, 0, 1), SideType::Bottom);
        let top = Side::new(Point3D::new(0, 0, 0), SideType::Top);
        let back = Side::new(Point3D::new(0, 1, 0), SideType::Back);
        let front = Side::new(Point3D::new(0, 0, 0), SideType::Front);

        assert_eq!(left, right);
        assert_eq!(back, front);
        assert_eq!(bottom, top);

        for (a, b) in [(left, right), (bottom, top), (front, back)] {
            let mut hasher1 = DefaultHasher::new();
            let mut hasher2 = DefaultHasher::new();
            a.hash(&mut hasher1);
            b.hash(&mut hasher2);
            assert_eq!(hasher1.finish(), hasher2.finish());
        }
    }

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 18);
        assert_eq!(part_one(&input), Some(64));
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 18);
        assert_eq!(part_two(&input), Some(58));
    }
}
