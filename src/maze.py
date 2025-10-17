import f0

def init(size):
	clear()
	plant(Entities.Bush)
	n_substance = size * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, n_substance)

def harvest_if_found():
	if get_entity_type() == Entities.Treasure:
		harvest()
		return True
	return False

def solve_naive():
	directions = [North, East, South, West]
	prev_dir = 0

	while harvest_if_found() == False:
		for turn in [-1, 0, 1, 2]:
			cur_dir = (prev_dir + turn) % 4
			dir = directions[cur_dir]
			if move(dir):
				prev_dir = cur_dir
				break

DIRECTIONS = [North, East, South, West]
def solve():
	goal_x, goal_y = measure()
	visited = set()

	def dfs():
		x = get_pos_x()
		y = get_pos_y()

		if x == goal_x and y == goal_y:
			return True
		
		visited.add((x, y))

		candidates = []
		for d in DIRECTIONS:
			next_x, next_y = get_next_pos(x, y, d)

			if (next_x, next_y) not in visited:
				dist = manhattan_distance(next_x, next_y, goal_x, goal_y)
				candidates.append((dist, d))
		
		candidates = sort_by_distance(candidates)

		for dist, direction in candidates:
			if move(direction):
				if dfs():
					return True
				move(reverse_direction(direction))

		# visited.remove((x, y))
		return False

	if dfs():
		return True
	else:
		print("Failed to solve maze")
		return False

def get_next_pos(x, y, d):
	if d == North:
		return (x, y + 1)
	elif d == East:
		return (x + 1, y)
	elif d == South:
		return (x, y - 1)
	else:
		return (x - 1, y)

def reverse_direction(d):
    if d == North:
        return South
    elif d == South:
        return North
    elif d == East:
        return West
    else:  # West
        return East


def sort_by_distance(items):
	n = len(items)
	for i in range(n-1):
		min_i = i
		for j in range(i+1, n):
			if items[min_i][0] > items[j][0]:
				min_i = j
		if i != min_i:
			items[i], items[min_i] = items[min_i], items[i]
	return items


def manhattan_distance(x1, y1, x2, y2):
	return abs(x1 - x2) + abs(y1 - y2)
