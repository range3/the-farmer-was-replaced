import f0
import tile
import cactus
import maze
import sunflowers
import polycultures
import pumpkins


f0.move_to(0, 0)

def comp_inventory(a, b):
	return a[0] - b[0]

prev_mode = None

while True:
	inventory = [
		(num_items(Items.Hay), Items.Hay),
		(num_items(Items.Wood), Items.Wood),
		(num_items(Items.Carrot), Items.Carrot),
		(num_items(Items.Pumpkin), Items.Pumpkin),
		# (num_items(Items.Power), Items.Power),
		(num_items(Items.Cactus), Items.Cactus),
	]
	inventory = f0.quick_sort(inventory, comp_inventory)
	quick_print(inventory)

	if inventory[0][1] == Items.Hay or inventory[0][1] == Items.Wood:
		if prev_mode != Items.Hay:
			polycultures.init(0, 0, get_world_size(), get_world_size())
		else:
			polycultures.replant(0, 0, get_world_size(), get_world_size())
		prev_mode = Items.Hay
	
	elif inventory[0][1] == Items.Carrot:
		if prev_mode != Items.Carrot:
			polycultures.init_carrot(0, 0, get_world_size(), get_world_size())
		else:
			polycultures.replant_carrot(0, 0, get_world_size(), get_world_size())
		prev_mode = Items.Carrot
	
	elif inventory[0][1] == Items.Pumpkin:
		pumpkins.init(0, 0, get_world_size(), get_world_size())
		while pumpkins.check_and_replant() == False:
			pass
		f0.harvest_if_ready()
		prev_mode = Items.Pumpkin
	
	# elif inventory[0][1] == Items.Power:
	elif num_items(Items.Power) < 1000:
		sunflowers.init(0, 0, get_world_size(), get_world_size())
		sunflowers.harvest_all()
		prev_mode = Items.Power
	
	# elif inventory[0][1] == Items.Cactus:
	else:
		if prev_mode != Items.Cactus:
			cactus.init(0, 0, get_world_size(), get_world_size())
		else:
			cactus.replant(0, 0, get_world_size(), get_world_size())
		cactus.sort(0, 0, get_world_size(), get_world_size())
		prev_mode = Items.Cactus
