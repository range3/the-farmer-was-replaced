import c

def wait_all():
	while num_drones() > 1:
		pass

def for_all(fn):
	for y in range(c.MAX_DRONES - 1, 0, -1):
		def _fn():
			for _ in range(y):
				move(North)
			fn(y)
		spawn_drone(_fn)
	fn(0)
	wait_all()
