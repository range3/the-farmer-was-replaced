import f0
import c
import parallel

PETALS_SIZE = c.PETALS_MAX - c.PETALS_MIN + 1
def run():
	
	def plant_and_15(y):
		petals_row = []
		for _ in range(PETALS_SIZE):
			petals_row.append([])

		for x in range(c.WORLD_SIZE):
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Sunflower)
			if get_water() < 0.5:
				use_item(Items.Water)
			petals_row[c.PETALS_MAX - measure()].append(x)
			move(East)
		
		for i in range(len(petals_row[0])):
			f0.move_to(petals_row[0][i], y)
			while not can_harvest():
				pass
			harvest()
		
		return petals_row
	
	f0.move_to(0, 0)
	petals = parallel.for_all_ret(plant_and_15)

	for i in range(1, PETALS_SIZE):
		def harvest_i(y):
			for j in range(len(petals[y][i])):
				f0.move_to(petals[y][i][j], y)
				while not can_harvest():
					pass
				harvest()
		
		parallel.for_all(harvest_i)
