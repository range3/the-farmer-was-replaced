import f0
import c
import parallel

pumpkin_set = set()
def init(ofs_x, ofs_y, width, height):
	def iter():
		harvest()
		f0.till_to_soil()
		plant(Entities.Pumpkin)
		pumpkin_set.add((get_pos_x(), get_pos_y()))

	f0.move_to(ofs_x, ofs_y)
	f0.zigzag(width, height, iter)

def check_and_replant():
	global pumpkin_set
	new_set = set()
	for px, py in pumpkin_set:
		f0.move_to(px, py)
		if not can_harvest():
			new_set.add((px, py))
			if get_entity_type() != Entities.Pumpkin:
				plant(Entities.Pumpkin)
	pumpkin_set = new_set
	return len(pumpkin_set) == 0

def run():
	def drone_task(_):
		for _ in range(c.WORLD_SIZE):
			harvest()
			if get_ground_type() != Grounds.Soil:
				till()
			plant(Entities.Pumpkin)
			if get_water() < 0.5:
				use_item(Items.Water)
			move(East)

		for _ in range(c.WORLD_SIZE):
			while get_entity_type() != Entities.Pumpkin:
				plant(Entities.Pumpkin)
				use_item(Items.Fertilizer)
			move(East)

	parallel.for_all(drone_task)
	harvest()
	
