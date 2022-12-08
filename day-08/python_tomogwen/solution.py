
if __name__ == '__main__':
    f = open('input.txt', 'r')
    lines = f.readlines()

    trees = [[int(x) for x in list(line.strip())] for line in lines]
    num_rows, num_cols = len(trees), len(trees[0])
    # from the edges
    num_visible = num_rows*2 + num_cols*2 - 4

    best_scenic_score = 0
    # from inside
    for i in range(1, num_rows-1):
        for j in range(1, num_cols-1):
            visible_up = True
            up_score = 0
            for k in range(i-1, -1, -1):
                # we need just one of the trees to be too tall to make it invisible
                if trees[i][j] <= trees[k][j]:
                    visible_up = False
                    up_score += 1
                    break
                else:
                    up_score += 1

            visible_down = True
            down_score = 0
            for k in range(i+1, num_rows):
                if trees[i][j] <= trees[k][j]:
                    visible_down = False
                    down_score += 1
                    break
                else:
                    down_score += 1

            visible_left = True
            left_score = 0
            for k in range(j-1, -1, -1):
                if trees[i][j] <= trees[i][k]:
                    visible_left = False
                    left_score += 1
                    break
                else:
                    left_score += 1

            visible_right = True
            right_score = 0
            for k in range(j+1, num_cols):
                if trees[i][j] <= trees[i][k]:
                    visible_right = False
                    right_score += 1
                    break
                else:
                    right_score += 1

            # print(i, j, trees[i][j] , visible_up, visible_down, visible_left, visible_right)
            if visible_up or visible_down or visible_left or visible_right:
                num_visible += 1

            # print(i, j, up_score, down_score, left_score, right_score)
            tot_score = up_score*down_score*left_score*right_score
            if tot_score > best_scenic_score:
                best_scenic_score = tot_score

    print(num_visible)
    print(best_scenic_score)

