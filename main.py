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
character_color = (200, 197, 20)
ball_color = (255, 0, 0)
ground_color = (0, 0, 0)
font = pygame.font.Font(None, 36)  # Choose a font and size
character_radius = 20
ball_radius = 25
character_x = width // 2
character_y = height - character_radius
character_speed = 5
balls = []
# red, yellow, blue, green, purple
ball_color = [(192, 43, 43), (240, 171, 15), (8, 154, 204), (114, 194, 37), (180, 87, 202)]
init_ball_y_height = 250
ball_vertical_speed = 3
# ball_horizonal_speed = 3
gravity = 2


class Character:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

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
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.horizontal_speed * self.toward
        self.y += self.vertical_speed
        #detect ball collision with ground
        if self.y + self.radius >= height:
            self.y = height - self.radius  # Adjust y position to be exactly on the ground
            self.vertical_speed = -self.vertical_speed  # Reverse vertical speed

running = True
character = Character(character_x, character_y, character_radius, character_color)

while running:
    window.fill(background_color)
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 10 / 100.0
    text_surface = font.render(f"Time: {elapsed_time}", True, (0, 0, 0))  # Render the text
    window.blit(text_surface, (10, 10))  # Adjust the position as needed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and character.x > character_radius:
        character.x -= character_speed
    if keys[pygame.K_RIGHT] and character.x < width - character_radius:
        character.x += character_speed

    # Create new balls randomly with certian probability
    if random.randint(0, 100) < 2:
        ball_x = random.choice([0, 600])
        ball_y = random.choice([0, 20, 40])
        color_index = random.randint(0, 4)
        if ball_x == 0:
            toward = 1
        else:
            toward = -1
        ball_horizonal_speed = random.randint(1, 3)
        ball = Ball(ball_x, ball_y, ball_radius, ball_color[color_index], ball_vertical_speed, ball_horizonal_speed, toward)
        balls.append(ball)

    for ball in balls:
        ball.move()
        if ball.y + ball.radius > height:
            balls.remove(ball)
        if (
            ball.y + ball.radius > character.y - character.radius
            and character.x - character.radius < ball.x < character.x + character.radius
        ):
            running = False

        ball.draw()

    character.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()