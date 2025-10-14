import f0

def checker_black(x, y):
	return (x + y) % 2 == 0

def init(ofs_x, ofs_y, width, height):
	def iter():
		harvest()
		f0.till_to_grassland()
		if checker_black(get_pos_x(), get_pos_y()):
			plant(Entities.Tree)
	f0.move_to(ofs_x, ofs_y)
	f0.zigzag(width, height, iter)

def replant(ofs_x, ofs_y, width, height):
	def iter():
		f0.harvest_if_ready()
		if checker_black(get_pos_x(), get_pos_y()):
			plant(Entities.Tree)
	f0.move_to(ofs_x, ofs_y)
	f0.zigzag(width, height, iter)


def init_carrot(ofs_x, ofs_y, width, height):
	def iter():
		harvest()
		f0.till_to_soil()
		plant(Entities.Carrot)
	f0.move_to(ofs_x, ofs_y)
	f0.zigzag(width, height, iter)

def replant_carrot(ofs_x, ofs_y, width, height):
	def iter():
		f0.harvest_if_ready()
		plant(Entities.Carrot)
	f0.move_to(ofs_x, ofs_y)
	f0.zigzag(width, height, iter)
