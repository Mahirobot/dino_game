import random
import time
from sense_hat import SenseHat

sense = SenseHat()

sense.clear()

score_file = '/home/group2/project/scores.txt'

# COLORS
dino = (240, 128, 128)
bg_color = (0, 0, 0)
land_color_1 = (152, 251, 152)
land_color_2 = (205, 133, 63)
rock_color = (119, 34, 153)
tree_color = (34, 134, 34)

deuteranopia_colors = {
'character': (0, 255, 255),
'land_1': (139, 0, 0),
'land_2': (165, 42, 42),
'rock': (128, 128, 128),
'tree': (128, 128, 0)
}



# SETTINGS
character_position = 6
obstacle_position = 7
jump_count = 0
max_jumps = 2
is_jumping = False
obstacle_type = None
land_offset = 0
speed_dino = 0.2
speed_obs = 0.1
game_over = False
score = 0
start_time = 0


def switch_to_colorblind_palette():
	global dino, land_color_1, land_color_2, rock_color, tree_color
	dino = deuteranopia_colors['character']
	land_color_1 = deuteranopia_colors['land_1']
	land_color_2 = deuteranopia_colors['land_2']
	rock_color = deuteranopia_colors['rock']
	tree_color = deuteranopia_colors['tree']
	


def load_scores():
	try:
		with open(score_file, 'r') as f:
			scores = [int(line.strip()) for line in f]
		return sorted(scores, reverse=True)[:3]
	except Exception:
		return []

def save_score(new_score):
	with open(score_file, 'a') as f:
		f.write(f'{new_score}\n')

def update_background():
	temp = sense.get_temperature()
	humidity = sense.get_humidity()
	
	if temp < 5:
		
		return (152, 255, 152)
	elif humidity > 50:
		return (135, 206, 250)
	else:
		return (255, 255, 160)

def start_screen():
	sense.show_message('Press UP to start!', text_colour=(255, 255, 255), scroll_speed=0.07)

def end_screen():
	sense.show_message(f'Game Over! Score: {score}', text_colour=(255, 0, 0), scroll_speed=0.07)
	time.sleep(2)
	start_screen()

def generate_obstacle():
	global obstacle_type
	obstacle_type = random.choice([None, 'rock', 'tree'])


def move_obstacle():
	global obstacle_position
	if obstacle_position > 0:
		obstacle_position -= 1
	else:
		obstacle_position = 6
		generate_obstacle()
	time.sleep(speed_obs)


def display_game():
	bg_color = update_background()
	sense.clear(bg_color)
	for x in range(8):
		if (x + land_offset) % 2 == 0:
			sense.set_pixel(x, 7, land_color_1)
		else:
			sense.set_pixel(x, 7, land_color_2)
	
	sense.set_pixel(1, character_position, dino)
	move_obstacle()
	if obstacle_type == 'rock':
		sense.set_pixel(obstacle_position, 6, rock_color)
	elif obstacle_type == 'tree':
		sense.set_pixel(obstacle_position, 6, tree_color)


def handle_jump():
	global is_jumping, jump_count, character_position
	
	if jump_count< max_jumps:
		is_jumping = True
		jump_count += 1
		for _ in range(3):
			character_position -= 1
			display_game()
			time.sleep(speed_dino)
			
		for _ in range(3):
			character_position += 1
			display_game()
			time.sleep(speed_dino)
		is_jumping = False


def check_collision():
	if obstacle_position == 2:
		if (obstacle_type == 'rock' and character_position == 6) or (obstacle_type == 'tree' and character_position == 6):
			return True
	return False

def increase_speed():
	global speed_dino, speed_obs
	if time.time() - start_time >= 30:
		speed_dino = max(0.1, speed_dino - 0.5)
		speed_obs = max(0.05, speed_obs - 0.05)

def view_scoreboard():
	top_scores = load_scores()
	sense.show_message('Top scores: ', scroll_speed=0.05)
	for item in top_scores:
		sense.show_message(f'{item}', scroll_speed=0.05)

def blink_effect():
	for _ in range(3):
		sense.clear()
		time.sleep(0.2)
		display_game()
		time.sleep(0.2)
def start_game():
	global obstacle_position, land_offset, jump_count, game_over, score, start_time
	obstacle_position = 7
	land_offset = 0
	jump_count = 0
	game_over = False
	score = 0
	start_time = time.time()

	try:
		while not game_over:
			display_game()
			land_offset = (land_offset + 1) % 2
			
			if check_collision():
				
				game_over = True
				blink_effect()
				save_score(score)
				break
				
				
			for event in sense.stick.get_events():
				if event.action == 'pressed':
					if event.direction == 'up':
						if not is_jumping:
							handle_jump()
			
			if character_position == 6:
				jump_count = 0
			
			if increase_speed():
				start_time = time.time()
			
			score = int(time.time() - start_time)
			
			time.sleep(0.5)
	except KeyboardInterrupt:
		sense.clear()
	
			
start_screen()
while True:
	for event in sense.stick.get_events():
			if event.action == 'pressed':
				if event.direction == 'down':
					view_scoreboard()
				elif event.direction == 'up':
					start_game()
				elif event.direction == 'left':
					switch_to_colorblind_palette()
	if game_over:			
		end_screen()


	
