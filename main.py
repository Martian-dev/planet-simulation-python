import pygame
import math
pygame.init()

# WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Planet Simulation")
WIDTH, HEIGHT = WIN.get_size()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1 AU = 100 pixels !! not anymore
    TIMESTEP = 3600*24  # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x_coord = self.x * self.SCALE + WIDTH / 2
        y_coord = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for points in self.orbit:
                x, y = points
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, WHITE, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x_coord, y_coord), self.radius)

    def gravity(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        theta = math.atan2(distance_y, distance_x)
        force = self.G * self.mass * other.mass / distance ** 2
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_positions(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.gravity(planet)
            total_fx += fx
            total_fy += fy

        acceleration_x = total_fx / self.mass
        acceleration_y = total_fy / self.mass

        self.x_vel += acceleration_x * self.TIMESTEP
        self.y_vel += acceleration_y * self.TIMESTEP

        # sx = self.x_vel * self.TIMESTEP - 0.5 * acceleration_x * self.TIMESTEP ** 2
        # sy = self.y_vel * self.TIMESTEP - 0.5 * acceleration_y * self.TIMESTEP ** 2

        sx = self.x_vel * self.TIMESTEP
        sy = self.y_vel * self.TIMESTEP

        self.x += sx
        self.y += sy
        # self.x = self.x_vel * self.TIMESTEP
        # self.y = self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892e30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30e23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685e24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742e24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39e23)
    mars.y_vel = 24.077 * 1000

    planets = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_positions(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
