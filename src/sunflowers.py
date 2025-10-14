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
