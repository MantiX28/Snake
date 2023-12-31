from __future__ import annotations
import pygame
import time
import random

pygame.init()
pygame.font.init()


class Snake:
	def __init__(self) -> None:		
		self.direction: str = DIRECTIONS['UP']
		self.parts: list[Part] = [Part(SCREEN_WIDTH/2 - Part.WIDTH/2, SCREEN_HEIGHT/2 - Part.HEIGHT/2, self.direction,YELLOW)]
		self.last_color = WHITE
		
		self.add_part()
		self.add_part()

		self._kd_time = time.time()

	@property
	def first_part(self) -> Part:
		return self.parts[0]
	
	@property
	def last_part(self) -> Part:
		return self.parts[-1] 

	def add_part(self) -> None:
		if (dir := self.last_part.direction) == 'u':
			new_part = Part(self.last_part.x, self.last_part.y + Part.HEIGHT, dir, self.last_color)
		if dir == 'r':
			new_part = Part(self.last_part.x - Part.WIDTH, self.last_part.y, dir, self.last_color)
		if dir == 'l':
			new_part = Part(self.last_part.x + Part.WIDTH, self.last_part.y, dir, self.last_color)
		if dir == 'd':
			new_part = Part(self.last_part.x, self.last_part.y - Part.HEIGHT, dir, self.last_color)
		for move in self.last_part.moves:
			new_part.moves.append(move)
		self.parts.append(new_part)

		if self.last_color is RED:
			self.last_color = WHITE
		else:
			self.last_color = RED
		
		if hasattr(self, "food"):
			del self.food
			del self.food_timer
			self._reset_time()

	def draw_parts(self) -> None:
		if hasattr(self, "food"):
			pygame.draw.rect(GAME_WINDOW, RED, self.food)

		for part in self.parts[::-1]:			
			pygame.draw.rect(GAME_WINDOW, part.color, part)

	def draw_lenght(self):
		GAME_WINDOW.blit(pygame.font.SysFont("comicsans",25).render(str(len(self.parts)),1, WHITE), (10,10))
	
	def collision_check(self) -> bool:
		# check if snake eats food
		if hasattr(self, 'food'):
			if self.first_part.colliderect(self.food):
				self.add_part()
		
		# check if snake hits itself
		for part1 in self.parts:
			for part2 in self.parts:
				if part1 is not part2:
					if part1.colliderect(part2):
						return False
		
		# check if snake hits the sides
		if self.first_part.y <= 0 and self.direction == 'u':
			return False
		if self.first_part.y + Part.HEIGHT >= SCREEN_HEIGHT and self.direction == 'd':
			return False
		if self.first_part.x <= 0 and self.direction == 'l':
			return False
		if self.first_part.x + Part.WIDTH >= SCREEN_WIDTH and self.direction == 'r':
			return False
		
		return True
		
	def move(self, p_move) -> None:		
		if time.time() - self._kd_time >= 0.1:
			self._kd_time = time.time()
			if p_move == pygame.K_UP and self.direction not in [DIRECTIONS['UP'], DIRECTIONS['DOWN']]:
				self.direction = DIRECTIONS['UP']
			if p_move == pygame.K_RIGHT and self.direction not in [DIRECTIONS['RIGTH'], DIRECTIONS['LEFT']]:
				self.direction = DIRECTIONS['RIGTH']
			if p_move == pygame.K_DOWN and self.direction not in [DIRECTIONS['UP'], DIRECTIONS['DOWN']]:
				self.direction = DIRECTIONS['DOWN']
			if p_move == pygame.K_LEFT and self.direction not in [DIRECTIONS['RIGTH'], DIRECTIONS['LEFT']]:
				self.direction = DIRECTIONS['LEFT']
		
			for part in self.parts:
				part.moves.append((self.direction, self.first_part.x, self.first_part.y))
		
	def handle_movement(self):
		for part in self.parts:
			if part.moves:
				if part.x == part.moves[0][1] and part.y == part.moves[0][2]:
					part.direction = part.moves[0][0]
					part.moves.pop(0)
			if part.direction is DIRECTIONS['UP']:
				part.y -= Part.HEIGHT
			if part.direction is DIRECTIONS['RIGTH']:
				part.x += Part.WIDTH
			if part.direction is DIRECTIONS['DOWN']:
				part.y += Part.HEIGHT
			if part.direction is DIRECTIONS['LEFT']:
				part.x -= Part.WIDTH
				
	def _reset_time(self) -> None:
		del self.g_time

	def check_food(self) -> None:
		if not hasattr(self, "food"):
			if not hasattr(self, "g_time"):
				self.g_time = time.time()
			if not hasattr(self, "cooldown"):
				self.cooldown = 1
			if time.time() - self.g_time >= self.cooldown:				
				if self.direction in ['u', 'd']:
					min_x = self.first_part.x
					max_x = self.first_part.x + Part.WIDTH
					if self.direction == 'u':
						min_y = self.first_part.y
						max_y = self.last_part.y + Part.HEIGHT
					else:
						min_y = self.last_part.y
						max_y = self.first_part.y + Part.HEIGHT

				if self.direction in ['r', 'l']:
					min_y = self.first_part.y
					max_y = self.first_part.y + Part.HEIGHT
					if self.direction == 'r':
						min_x = self.last_part.x
						max_x = self.first_part.x + Part.WIDTH
					else:
						min_x = self.first_part.x 
						max_x = self.last_part.x + Part.WIDTH
				
				while True:
					random.seed()
					food_x = random.randint(0, SCREEN_WIDTH - FOOD_WIDTH)
					if food_x + FOOD_WIDTH < min_x or food_x > max_x:
						break
				
				while True:
					random.seed()
					food_y = random.randint(0, SCREEN_HEIGHT - FOOD_HEIGHT)
					if food_y + FOOD_HEIGHT < min_y or food_y > max_y:
						break
				
				self.food = pygame.Rect(food_x, food_y, FOOD_WIDTH, FOOD_HEIGHT)
				self.food_timer = time.time()
		
		if hasattr(self, "food") and time.time() - self.food_timer >= 10:
			del self.food
			del self.food_timer
			self._reset_time()

	def reset_game(self) -> None:
		self.__init__()
		if hasattr(self, "food"):
			del self.food
			del self.food_timer
		self._reset_time()

	@staticmethod
	def lose() -> None:
		font = pygame.font.SysFont("comicsans",30)
		text = font.render("YOU LOST!", 1, WHITE)
		GAME_WINDOW.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
		pygame.display.update()
		pygame.time.delay(5000)



class Part(pygame.Rect):
	WIDTH, HEIGHT = 10, 10
	def __init__(self, left: float, top: float, direction: str, color: tuple[int, int, int]) -> None:
		super().__init__(left, top, Part.WIDTH, Part.HEIGHT)
		self.moves: list[tuple[str, int, int]] = list()
		self.direction = direction
		self.color = color

	

SCREEN_WIDTH, SCREEN_HEIGHT = 350,350
GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("SNAKE GAME")

DIRECTIONS: dict[str, str] = {	
	"UP"    :  'u', 
	"RIGTH" :  'r',
	"DOWN"  :  'd',
	"LEFT"  :  'l'
}

FOOD_WIDTH, FOOD_HEIGHT = 20,20

GAME_FPS = 10
BLACK = (0,0,0)
WHITE = (230, 227, 227)
RED = (255,0,0)
YELLOW = (209, 206, 6)

mysnake = Snake()

def draw():
	GAME_WINDOW.fill(BLACK)
	mysnake.draw_parts()
	mysnake.draw_lenght()
	
	pygame.display.update()
	

def main():
	game_runs = True
	clock = pygame.time.Clock()
	while game_runs:
		clock.tick(GAME_FPS)
				
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				game_runs = False				

			if event.type == pygame.KEYDOWN:
				mysnake.move(event.key)
		
		if not mysnake.collision_check():
			mysnake.lose()
			break

		mysnake.handle_movement()		
		mysnake.check_food()

		draw()

	pygame.quit()

if __name__ == "__main__":
	main()
