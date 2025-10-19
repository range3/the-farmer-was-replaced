import c

def move_to_x(goal_x, current_x = get_pos_x()):
	dx = (goal_x - current_x + c.HALF_WORLD_SIZE) % c.WORLD_SIZE - c.HALF_WORLD_SIZE

	for _ in range(dx):
		move(East)
	for _ in range(-dx):
		move(West)

def move_to_y(goal_y, current_y = get_pos_y()):
	dy = (goal_y - current_y + c.HALF_WORLD_SIZE) % c.WORLD_SIZE - c.HALF_WORLD_SIZE

	for _ in range(dy):
		move(North)
	for _ in range(-dy):
		move(South)

def move_to(goal_x, goal_y, current_x = get_pos_x(), current_y = get_pos_y()):
	move_to_x(goal_x, current_x)
	move_to_y(goal_y, current_y)

def move_to_pos(goal_pos, current_pos = (get_pos_x(), get_pos_y())):
	goal_x, goal_y = goal_pos
	current_x, current_y = current_pos
	move_to(goal_x, goal_y, current_x, current_y)
