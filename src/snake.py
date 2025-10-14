import f0


def init():
	f0.move_to(0, 0)
	change_hat(Hats.Dinosaur_Hat)

def move_and_reset_if_blocked(direction):
	if not move(direction):
		change_hat(Hats.Dinosaur_Hat)
		move(direction)

def naive_solver(width, height):
	while True:
		move_and_reset_if_blocked(East)
		for row in range(height-1):
			if row % 2 == 0:
				d = East
			else:
				d = West
			for _ in range(width-2):
				move_and_reset_if_blocked(d)
			
			move_and_reset_if_blocked(North)
		
		for _ in range(width-1):
			move_and_reset_if_blocked(West)
		for _ in range(height-1):
			move_and_reset_if_blocked(South)
	
