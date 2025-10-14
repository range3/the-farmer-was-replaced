import f0

petals_map = {}


PETALS_MAX = 15
PETALS_MIN = 7
PETALS_SIZE = PETALS_MAX - PETALS_MIN + 1

petals = []


def init(ofs_x, ofs_y, width, height):
	global petals

	petals = []
	for _ in range(PETALS_SIZE):
		petals.append([])

	global petals_map
	def process_iter():
		harvest()
		f0.till_to_soil()
		plant(Entities.Sunflower)
		# petals_map[(get_pos_x(), get_pos_y())] = measure()
		petals[measure() - PETALS_MIN].append((get_pos_x(), get_pos_y()))

		p

	f0.move_to(ofs_x, ofs_y)
	f0.zigzag(width, height, process_iter)

def harvest_all():
	global petals_map

	petals_list = []
	for pos in petals_map:
		x, y = pos
		petals_list.append((x, y, petals_map[pos]))
	
	def comp(a, b):
		return (b[2] - a[2]) * 100 + (a[0] - b[0]) * 10 + (a[1] - b[1])

	petals_list = f0.quick_sort(petals_list, comp)

	for item in petals_list:
		x, y, petal_count = item
		# quick_print(petal_count, x)
		f0.move_to(x, y)
		# if not can_harvest():
		# 	use_item(Items.Fertilizer)
		harvest()
		# plant(Entities.Sunflower)
		# petals_map[(x, y)] = measure()
