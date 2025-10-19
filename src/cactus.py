import f0
import parallel
import c
import movement

cactus_map = {}

def _process_cactus_field(ofs_x, ofs_y, width, height, pre_plant_action):
	def process_iter():
		pre_plant_action()
		plant(Entities.Cactus)
		global cactus_map
		x, y = get_pos_x(), get_pos_y()
		cactus_map[(x, y)] = measure()

		if y > ofs_y and cactus_map[(x, y)] < cactus_map[(x, y - 1)]:
			swap(South)
			cactus_map[(x, y)], cactus_map[(x, y - 1)] = cactus_map[(x, y - 1)], cactus_map[(x, y)]
		if y % 2 == 0 and x > ofs_x and cactus_map[(x, y)] < cactus_map[(x - 1, y)]:
			swap(West)
			cactus_map[(x, y)], cactus_map[(x - 1, y)] = cactus_map[(x - 1, y)], cactus_map[(x, y)]
		elif y % 2 == 1 and x < ofs_x + width - 1 and cactus_map[(x, y)] < cactus_map[(x + 1, y)]:
			swap(East)
			cactus_map[(x, y)], cactus_map[(x + 1, y)] = cactus_map[(x + 1, y)], cactus_map[(x, y)]
	
	f0.move_to(ofs_x, ofs_y)
	f0.zigzag(width, height, process_iter)

def init(ofs_x, ofs_y, width, height):
	def pre_plant():
		harvest()
		f0.till_to_soil()
	
	_process_cactus_field(ofs_x, ofs_y, width, height, pre_plant)

def replant(ofs_x, ofs_y, width, height):
	f0.move_to(ofs_x, ofs_y)
	f0.harvest_if_ready()

	def _do_nothing():
		pass

	_process_cactus_field(ofs_x, ofs_y, width, height, _do_nothing)

def sort(ofs_x, ofs_y, width, height):
	move_count = 0
	swap_count = 0

	# East-West sort (rows)
	for h in range(height):
		y = ofs_y + h

		# cocktail sort
		left = 0 
		last_swapped = left
		right = width - 1
		while left < right:
			tmp = -1
			f0.move_to(ofs_x + left, y)
			for i in range(left, right):
				x = ofs_x + i
				x_next = x + 1

				# Heuristic
				if h + 1 < height:
					north_item = cactus_map[(x, y + 1)]
					if cactus_map[(x, y)] > north_item and tmp < north_item:
						swap(North)
						swap_count += 1
						cactus_map[(x, y)], cactus_map[(x, y + 1)] = cactus_map[(x, y + 1)], cactus_map[(x, y)]

				if cactus_map[(x, y)] > cactus_map[(x_next, y)]:
					swap(East)
					swap_count += 1
					cactus_map[(x, y)], cactus_map[(x_next, y)] = cactus_map[(x_next, y)], cactus_map[(x, y)]
					last_swapped = i
				
				tmp = max(tmp, cactus_map[(x, y)])

				if i < right - 1:
					move(East)
					move_count += 1
			
			right = last_swapped
			
			if left >= right:
				break

			f0.move_to(ofs_x + right, y)
			for i in range(right, left, -1):
				x = ofs_x + i
				x_prev = x - 1

				if cactus_map[(x_prev, y)] > cactus_map[(x, y)]:
					swap(West)
					swap_count += 1
					cactus_map[(x_prev, y)], cactus_map[(x, y)] = cactus_map[(x, y)], cactus_map[(x_prev, y)]
					# swapped = True
					last_swapped = i

				if i > left + 1:
					move(West)
					move_count += 1

			left = last_swapped

	# North-South sort (columns)
	for w in range(width):
		x = ofs_x + w
		# cocktail sort
		bottom = 0
		last_swapped = bottom
		top = height - 1
		while bottom < top:
			f0.move_to(x, ofs_y + bottom)
			for i in range(bottom, top):
				y = ofs_y + i
				y_next = y + 1
				if cactus_map[(x, y)] > cactus_map[(x, y_next)]:
					swap(North)
					swap_count += 1
					cactus_map[(x, y)], cactus_map[(x, y_next)] = cactus_map[(x, y_next)], cactus_map[(x, y)]
					last_swapped = i
				
				if i < top - 1:
					move(North)
					move_count += 1
			
			top = last_swapped
			
			if bottom >= top:
				break
			f0.move_to(x, ofs_y + top)
			for i in range(top, bottom, -1):
				y = ofs_y + i
				y_prev = y - 1
				if cactus_map[(x, y_prev)] > cactus_map[(x, y)]:
					swap(South)
					swap_count += 1
					cactus_map[(x, y_prev)], cactus_map[(x, y)] = cactus_map[(x, y)], cactus_map[(x, y_prev)]
					last_swapped = i
				if i > bottom + 1:
					move(South)
					move_count += 1
			bottom = last_swapped

def run():
	movement.move_to(0, 0)

	def _row(y):
		cactus_row = []
		for _ in range(c.WORLD_SIZE):
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Cactus)
			cactus_row.append(measure())
			move(East)

		# East-West cocktail sort
		left = 0 
		last_swapped = left
		right = c.WORLD_SIZE - 1
		x = 0
		while left < right:
			movement.move_to_x(left, x)
			for x in range(left, right):
				x_next = x + 1

				if cactus_row[x] > cactus_row[x_next]:
					swap(East)
					cactus_row[x], cactus_row[x_next] = cactus_row[x_next], cactus_row[x]
					last_swapped = x
				
				if x < right - 1:
					move(East)
			
			right = last_swapped
			
			if left >= right:
				break

			movement.move_to_x(right, x)
			for x in range(right, left, -1):
				x_prev = x - 1

				if cactus_row[x_prev] > cactus_row[x]:
					swap(West)
					cactus_row[x_prev], cactus_row[x] = cactus_row[x], cactus_row[x_prev]
					last_swapped = x

				if x > left + 1:
					move(West)

			left = last_swapped

		return cactus_row
	
	cactus = parallel.for_all_ret(_row)

	def _col(x):
		# North-South cocktail sort
		bottom = 0
		last_swapped = bottom
		top = c.WORLD_SIZE - 1
		y = 0
		while bottom < top:
			movement.move_to_y(bottom, y)
			for y in range(bottom, top):
				y_next = y + 1
				if cactus[y][x] > cactus[y_next][x]:
					swap(North)
					cactus[y][x], cactus[y_next][x] = cactus[y_next][x], cactus[y][x]
					last_swapped = y
				
				if y < top - 1:
					move(North)
			
			top = last_swapped
			
			if bottom >= top:
				break

			movement.move_to_y(top, y)
			for y in range(top, bottom, -1):
				y_prev = y - 1
				if cactus[y_prev][x] > cactus[y][x]:
					swap(South)
					cactus[y_prev][x], cactus[y][x] = cactus[y][x], cactus[y_prev][x]
					last_swapped = y

				if y > bottom + 1:
					move(South)

			bottom = last_swapped
	
	movement.move_to(0, 0)
	for x in range(c.WORLD_SIZE - 1, 0, -1):
		def _fn():
			for _ in range(x):
				move(East)
			_col(x)
		spawn_drone(_fn)
	_col(0)
	parallel.wait_all()
	harvest()
	