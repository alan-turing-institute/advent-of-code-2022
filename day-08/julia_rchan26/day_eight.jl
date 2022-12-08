using Test

function parse_input(file::String)
    # parse input as a Matrix
    vec_of_vec = [parse.(Int64, x) for x in split.(readlines(file), "")]
    return mapreduce(permutedims, vcat, vec_of_vec)
end

test_input = parse_input("test_input.txt")
input = parse_input("input.txt")

function bool_matrix(true_mat::Bool, nrow::Int64, ncol::Int64)
    # creates Boolean matrix of size nrow x ncol
    return reshape([true_mat for x in 1:(nrow*ncol)], nrow, ncol)
end

function obtain_surrounding_heights(i::Int64, j::Int64, tree_heights::Matrix)
    # obtains the heights of trees in each direction
    return [reverse(tree_heights[1:(i-1),j]),
            tree_heights[(i+1):end, j],
            reverse(tree_heights[i,1:(j-1)]),
            tree_heights[i,(j+1):end]]
end

function is_visible_direction(value::Int64, vector::Vector)
    # value is height of tree
    # vector is vector of tree heights in certain direction
    return value > maximum(vector)
end

function is_visible(i::Int64, j::Int64, tree_heights::Matrix)
    # determines if tree_heights[i,j] is visible given its surrounding heights
    nrow = size(tree_heights)[1]
    ncol = size(tree_heights)[2]
    if i<1 || i>nrow
        throw(error("i is out of range"))
    elseif j<1 || j>ncol
        throw(error("j is out of range"))
    elseif i==1 || i==nrow || j==1 || j==ncol
        # tree around the edge is visible
        return true 
    else
        heights = obtain_surrounding_heights(i, j, tree_heights)
        return any(is_visible_direction.(tree_heights[i,j], heights))
    end
end

function part_one(tree_heights::Matrix)
    nrow = size(tree_heights)[1]
    ncol = size(tree_heights)[2]
    # initialise matrix with trues (1) (surrounding edges are visible)
    visibility_mat = bool_matrix(true, nrow, ncol)
    for i ∈ 2:(nrow-1)
        for j ∈ 2:(ncol-1)
            visibility_mat[i,j] = is_visible(i, j, tree_heights)
        end
    end
    return sum(visibility_mat)
end

function viewing_distance_direction(value::Int64, vector::Vector)
    # value is height of tree
    # vector is vector of tree heights in certain direction
    index = findfirst(x->x >= value, vector)
    if isnothing(index)
        # current tree height is larger than any tree in this direction
        # so can see to the edge
        return length(vector)
    else
        return index
    end
end

function part_two(tree_heights::Matrix)
    nrow = size(tree_heights)[1]
    ncol = size(tree_heights)[2]
    # initialise matrix with zeros
    scenic_scores = zeros(Int64, nrow, ncol)
    for i ∈ 1:nrow
        for j ∈ 1:ncol
            heights = obtain_surrounding_heights(i, j, tree_heights)
            scenic_scores[i,j] = prod(viewing_distance_direction.(tree_heights[i,j], heights))
        end
    end
    return maximum(scenic_scores)
end

# testing is_visible
Test.@test is_visible(2, 2, test_input) == true
Test.@test is_visible(2, 3, test_input) == true
Test.@test is_visible(2, 4, test_input) == false
Test.@test is_visible(3, 2, test_input) == true
Test.@test is_visible(3, 3, test_input) == false
Test.@test is_visible(3, 4, test_input) == true
Test.@test is_visible(4, 2, test_input) == false
Test.@test is_visible(4, 3, test_input) == true
Test.@test is_visible(4, 4, test_input) == false

# testing cases
Test.@test part_one(test_input) == 21
Test.@test part_two(test_input) == 8

# Part One
println("Part One: ", part_one(input))

# Part Two
println("Part Two: ", part_two(input))