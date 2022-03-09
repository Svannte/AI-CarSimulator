import pygame
import math

CAR_SIZE_X = 60 / 2
CAR_SIZE_Y = 60 / 2

BORDER_COLOR = (255, 255, 255, 255)


def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


TRACK = scale_image(pygame.image.load("map.png"), 0.5)

RED_CAR1 = pygame.image.load('imgs/red-car.png')
RED_CAR = pygame.transform.scale(RED_CAR1, (CAR_SIZE_X, CAR_SIZE_Y))
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("idk")


def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)


def draw(win, imagess, player_carr):
    for img, pos in imagess:
        win.blit(img, pos)

    player_carr.draw(win)
    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)

    if keys[pygame.K_d]:
        player_car.rotate(right=True)

    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()

    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


class Car:
    IMG = RED_CAR

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 270
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        self.center = [int(self.x) + CAR_SIZE_X / 2, int(self.y) + CAR_SIZE_Y / 2]
        horizontal = math.sin(radians) * self.vel
        vertical = math.cos(radians) * self.vel

        self.x -= horizontal
        self.y -= vertical

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def collide(self):
        length = 0.5 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length,
                    self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length,
                     self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length,
                       self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length,
                        self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]

        self.corners = [left_top, right_top, left_bottom, right_bottom]

        for point in self.corners:

            if TRACK.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                print("collision!")
                Car.bounce(self)
                break

    def bounce(self):
        self.vel = self.vel * 0.1
        self.move()


class PlayerCar(Car):
    IMG = RED_CAR
    START_POS = (415, 460)


if __name__ == '__main__':

    run = True

    clock = pygame.time.Clock()
    FPS = 60

    images = [(TRACK, (0, 0))]
    player_car = PlayerCar(4, 4)

    while run:
        clock.tick(FPS)

        draw(WIN, images, player_car)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        move_player(player_car)

        player_car.collide()

    pygame.quit()
