import math

import pygame

# The gravitational constant G
G = 6.67428e-11

# Distance between sun and earth
AU = 1000 * 149.6e6

# Assumed scale: 100 pixels = 1AU
SCALE = 250 / AU

MIN = 60
HOUR = 60 * MIN
# 1 year ~= 6.08 seconds
TIME_PER_FRAME = 24 * HOUR

SIMULATOR_WIDTH = 800
SIMULATOR_HEIGHT = 800

BG_COLOR = (5, 0, 20)
LINE_COLOR = (255, 255, 255)


class Astro:
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

    def calc_attraction_x_y(self, astro):
        distance = self.calc_distance(astro)
        distance_x = self.calc_distance_x(astro)
        distance_y = self.calc_distance_y(astro)
        attraction = G * self.mass * astro.mass / distance ** 2

        tangent = math.atan2(distance_y, distance_x)
        attraction_x = math.cos(tangent) * attraction
        attraction_y = math.sin(tangent) * attraction
        return attraction_x, attraction_y

    def calc_distance(self, astro):
        distance_x = self.calc_distance_x(astro)
        distance_y = self.calc_distance_y(astro)
        return math.sqrt(distance_x ** 2 + distance_y ** 2)

    def calc_distance_x(self, astro):
        return astro.x - self.x

    def calc_distance_y(self, astro):
        return astro.y - self.y


class Planet(Astro):
    def __init__(self, x, y, radius, color, mass, velocity_y):
        self.orbit = []
        self.velocity_x = 0
        self.velocity_y = velocity_y
        Astro.__init__(self, x, y, radius, color, mass)

    def update_position(self, astros):
        attraction_x = 0
        attraction_y = 0

        for astro in astros:
            if self != astro:
                att_x, att_y = self.calc_attraction_x_y(astro)
                attraction_x += att_x
                attraction_y += att_y

        self.velocity_x += attraction_x / self.mass * TIME_PER_FRAME
        self.velocity_y += attraction_y / self.mass * TIME_PER_FRAME
        self.x += self.velocity_x * TIME_PER_FRAME
        self.y += self.velocity_y * TIME_PER_FRAME
        self.orbit.append((self.x, self.y))


def main():
    sun = Astro(0, 0, 30, (242, 131, 32), 1.98892 * 10 ** 30)
    astros = [
        sun,
        Planet(
            0.387 * AU, 0, 8, (89, 88, 86), 3.30 * 10 ** 23, -47.4 * 1000,
        ),
        Planet(
            -1 * AU, 0, 16, (66, 107, 143), 5.9742 * 10 ** 24, 29.783 * 1000,
        ),
        Planet(
            -1.524 * AU, 0, 12, (218, 189, 157), 6.39 * 10 ** 23, 24.077 * 1000,
        ),
        Planet(
            0.723 * AU, 0, 14, (135, 138, 141), 4.8685 * 10 ** 24, -35.02 * 1000,
        ),
    ]

    pygame.init()
    c = pygame.time.Clock()
    w = pygame.display.set_mode((SIMULATOR_WIDTH, SIMULATOR_HEIGHT))

    while True:
        c.tick(60)
        w.fill(BG_COLOR)

        for astro in astros:
            if astro != sun:
                astro.update_position(astros)
                if len(astro.orbit) > 2:
                    points = []
                    for (x, y) in astro.orbit:
                        points.append(fix_scale(x, y))
                    pygame.draw.lines(w, LINE_COLOR, False, points, 2)

            pygame.draw.circle(w, astro.color, fix_scale(astro.x, astro.y), astro.radius)

        pygame.display.update()


def fix_scale(x, y):
    fx = x * SCALE + SIMULATOR_WIDTH / 2
    fy = y * SCALE + SIMULATOR_HEIGHT / 2
    return fx, fy


if __name__ == "__main__":
    main()
