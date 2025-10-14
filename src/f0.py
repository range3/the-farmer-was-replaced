def move_to(x, y):
	world_size = get_world_size()
	def move_axis(target, current, pos_dir, neg_dir):
		d = (target - current) % world_size
		if d > world_size / 2:
			d = world_size - d
			dir = neg_dir
		else:
			dir = pos_dir
		for _ in range(d):
			move(dir)
	
	move_axis(x, get_pos_x(), East, West)
	move_axis(y, get_pos_y(), North, South)

def zigzag(width, height, callback):
	for _ in range(height):
		if get_pos_y() % 2 == 0:
			d = East
		else:
			d = West
		for _ in range(width-1):
			callback()
			move(d)
		callback()
		move(North)

def add_water_if_needed(threshold = 0.75):
	if get_water() < threshold:
		use_item(Items.Water)

def prepare_soil(x, y, width, height):
	move_to(x, y)
	def till_if_needed():
		if get_ground_type() != Grounds.Soil:
			till()
	zigzag(width, height, till_if_needed)

def prepare_checked_soil(x, y, width, height):
	move_to(x, y)
	def till_if_needed():
		if (get_pos_x() + get_pos_y()) % 2 == 0:
			if get_ground_type() != Grounds.Soil:
				till()
		else:
			if get_ground_type() != Grounds.Grassland:
				till()
	zigzag(width, height, till_if_needed)


def till_to(ground_type):
	if get_ground_type() != ground_type:
		till()

def till_to_soil():
	till_to(Grounds.Soil)

def till_to_grassland():
	till_to(Grounds.Grassland)

def harvest_if_ready():
	if can_harvest():
		return harvest()
	return False

world_size = get_world_size()
def idx(x, y):
	return x + y * world_size

def xy(idx):
	return (idx % world_size, idx // world_size)

def fill_2d_grid(size, value):
	grid = []
	for _ in range(size):
		row = []
		for _ in range(size):
			row.append(value)
		grid.append(row)
	return grid

def quick_sort(arr, comp):
	if len(arr) <= 1:
		return arr

	pivot = arr[len(arr) // 2]
	left = []
	for x in arr:
		if comp(x, pivot) < 0:
			left.append(x)
	right = []
	for x in arr:
		if comp(x, pivot) > 0:
			right.append(x)
	
	res = []
	for x in quick_sort(left, comp):
		res.append(x)
	for x in arr:
		if comp(x, pivot) == 0:
			res.append(x)
	for x in quick_sort(right, comp):
		res.append(x)
	return res
