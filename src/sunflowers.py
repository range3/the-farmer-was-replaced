import f0

PETALS_MAX = 15
PETALS_MIN = 7
PETALS_SIZE = PETALS_MAX - PETALS_MIN + 1

petals = []

def init(ofs_x, ofs_y, width, height):
	global petals

	petals = []
	for _ in range(PETALS_SIZE):
		petals.append([])

	def process_iter():
		harvest()
		f0.till_to_soil()
		plant(Entities.Sunflower)
		petals[PETALS_MAX - measure()].append((get_pos_x(), get_pos_y()))

	f0.move_to(ofs_x, ofs_y)
	f0.zigzag(width, height, process_iter)

def harvest_all():
	global petals

	for pos_list in petals:
		for (x, y) in pos_list:
			f0.move_to(x, y)
			harvest()

def run_parallel():
	world_size = get_world_size()
	petals = []

	def row_plant():
		petals_row = []
		for x in range(world_size):
			harvest()
			f0.till_to_soil()
			plant(Entities.Sunflower)
			f0.add_water_if_needed(0.5)
			petals_row.append(measure())
			if x < world_size - 1:
				move(East)
		return petals_row
	
	f0.move_to(0, 0)

	handles = []
	last = None
	for _ in range(world_size):
		h = spawn_drone(row_plant)
		if h:
			handles.append(h)
		else:
			last = row_plant()
		move(North)

	for h in handles:
		petals.append(wait_for(h))
	petals.append(last)
	
	for psize in range(PETALS_MAX, PETALS_MIN - 1, -1):
		for y in range(world_size):
			def row_harvest():
				for x in range(world_size):
					if petals[y][x] == psize:
						harvest()
					if x < world_size - 1:
						move(East)
			handle = spawn_drone(row_harvest)
			if handle:
				handles.append(handle)
			else:
				row_harvest()
			move(North)
		for h in handles:
			wait_for(h)
