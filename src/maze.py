import f0

def init(ofs_x, ofs_y, size):
	f0.move_to(ofs_x, ofs_y)
	harvest()
	plant(Entities.Bush)
	n_substance = size * num_unlocked(Unlocks.Mazes)
	use_item(Items.Weird_Substance, n_substance)

def harvest_if_found():
	if get_entity_type() == Entities.Treasure:
		harvest()
		return True
	return False

def solve():
	directions = [North, East, South, West]
	prev_dir = 0

	while harvest_if_found() == False:
		for turn in [-1, 0, 1, 2]:
			cur_dir = (prev_dir + turn) % 4
			dir = directions[cur_dir]
			if move(dir):
				prev_dir = cur_dir
				break
