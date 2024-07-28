import pygame
import random

pygame.init()
width = 600
height = 300
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Attack on Balls")
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

background_color = (250, 240, 230)
ball_color = (255, 0, 0)
ground_color = (0, 0, 0)
font = pygame.font.Font(None, 36)
ball_radius = 25
character_speed = 5
balls = []
# red, yellow, blue, green, purple
ball_color = [(192, 43, 43), (240, 171, 15), (8, 154, 204), (114, 194, 37), (180, 87, 202)]
init_ball_y_height = 250
ball_vertical_speed = 3
gravity = 0.15

# Load and scale SVG images
def load_and_scale(file_path, scale_factor):
    img = pygame.image.load(file_path)
    new_size = (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor))
    return pygame.transform.scale(img, new_size)

scale_factor = 0.5  # Adjust this value to make the character smaller or larger
svg_idle = load_and_scale("character/front_facing.svg", scale_factor)
svg_left = load_and_scale("character/toward_left.svg", scale_factor)
svg_right = load_and_scale("character/toward_right.svg", scale_factor)

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "idle"
        self.svg_idle = svg_idle
        self.svg_left = svg_left
        self.svg_right = svg_right
        self.width = self.svg_idle.get_width()
        self.height = self.svg_idle.get_height()

    def draw(self):
        if self.state == "idle":
            svg = self.svg_idle
        elif self.state == "left":
            svg = self.svg_left
        else:  # right
            svg = self.svg_right
        window.blit(svg, (self.x - self.width // 2, self.y - self.height))

    def update_state(self, keys):
        if keys[pygame.K_LEFT]:
            self.state = "left"
        elif keys[pygame.K_RIGHT]:
            self.state = "right"
        else:
            self.state = "idle"

class Ball:
    def __init__(self, x, y, radius, color, vertical_speed, horizontal_speed, toward):
        self.x = x
        self.y = y
        self.radius = radius+random.randint(-5, 15)
        self.color = color
        self.vertical_speed = vertical_speed
        self.horizontal_speed = horizontal_speed
        self.toward = toward

    def draw(self):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.horizontal_speed * self.toward
        self.vertical_speed += gravity
        self.y += self.vertical_speed
        if self.y + self.radius >= height:
            self.y = height - self.radius
            self.vertical_speed = -self.vertical_speed

# Initialize character at the bottom of the screen
character_x = width // 2
character_y = height  # We'll adjust this in the Character initialization

running = True
character = Character(character_x, character_y)

while running:
    game_over = False
    if not game_over:
        window.fill(background_color)
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 10 / 100.0
        text_surface = font.render(f"Time: {elapsed_time:.2f}", True, (0, 0, 0))
        window.blit(text_surface, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    character.update_state(keys)
    if keys[pygame.K_LEFT] and character.x > character.width // 2:
        character.x -= character_speed
    if keys[pygame.K_RIGHT] and character.x < width - character.width // 2:
        character.x += character_speed

    if random.randrange(0, 100) < 1.5:
        ball_x = random.choice([0, 600])
        ball_y = random.choice([0, 20, 40])
        color_index = random.randint(0, 4)
        toward = 1 if ball_x == 0 else -1
        ball_horizonal_speed = random.randint(1, 3)
        ball = Ball(ball_x, ball_y, ball_radius, ball_color[color_index], ball_vertical_speed, ball_horizonal_speed, toward)
        balls.append(ball)
        
    for ball in balls:
        ball.move()
        if ball.y + ball.radius > height:
            balls.remove(ball)
        if (
            ball.y + ball.radius > character.y - character.height
            and character.x - character.width // 2 < ball.x < character.x + character.width // 2
        ):
            game_over = True
            break
        ball.draw()

    if game_over:
        game_over_text = font.render(f"Time: {elapsed_time:.2f}", True, (0, 0, 0))
        text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
        
        frosted_glass_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        frosted_glass_surface.fill((255, 255, 255, 128))
        pygame.draw.rect(frosted_glass_surface, (0, 0, 0, 0), text_rect, border_radius=10)
        
        window.blit(frosted_glass_surface, (0, 0))
        window.blit(game_over_text, text_rect)
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    running = False
                    waiting = False

    character.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()