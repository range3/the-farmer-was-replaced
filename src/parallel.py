import c

def wait_all():
	while num_drones() > 1:
		pass

def for_all(fn):
	for y in range(c.WORLD_SIZE - 1, 0, -1):
		def _fn():
			for _ in range(y):
				move(North)
			fn(y)
		spawn_drone(_fn)
	fn(0)
	wait_all()

def for_all_ret(fn):
	handles = []
	for y in range(c.WORLD_SIZE - 1, 0, -1):
		def _fn():
			for _ in range(y):
				move(North)
			return fn(y)
		handles.append(spawn_drone(_fn))

	result = [fn(0)]
	for i in range(len(handles) - 1, -1, -1):
		result.append(wait_for(handles[i]))
	return result
