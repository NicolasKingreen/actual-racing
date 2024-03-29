import pygame
from pygame.math import Vector2
from math import pi, exp, e
from pygame.surface import Surface


from asset_pool import AssetPool


class Car:
    def __init__(self, position: Vector2):
        self.spawn_position = position
        self.position = Vector2(self.spawn_position)

        self.facing_direction = Vector2(0, -1)  # faces up
        self.angle = 0  # TODO: take it from facing direction vector
        self.velocity = 0

        self.max_velocity = 750
        self.min_velocity = -100
        self.acceleration = 150
        self.friction_acceleration = 120
        self.braking = False
        self.brake_acceleration = 300

        self.min_turn_speed = 15.0
        self.max_turn_speed = 120.0
        self.turn_speed = 0  # deg?  # TODO: fix it raising too fast when max speed in close to min (exp is causing it)

        self.input_vector = Vector2()  # not normalized but every axis is in [-1, 1]

        self.sprite_path = "data/images/car1.png"
        self.sprite_rect = AssetPool.get_sprite(self.sprite_path).get_rect()
        self.rect = AssetPool.get_sprite(self.sprite_path).get_rect(center=self.position)

        # tires
        self.tires_positions = [[], []]

    def reset(self):
        self.position = Vector2(self.spawn_position)
        self.facing_direction = Vector2(0, -1)
        self.angle = 0
        self.velocity = 0
        self.input_vector = Vector2()
        self.rect.center = self.position
        self.tires_positions = [[], []]

    def update(self, frame_time_s):
        # print(self.position, round(self.velocity, 2), self.angle, self.facing_direction, self.input_vector)
        print(f"Velocity: {self.velocity:.2f} px/s, Braking: {self.braking}, Turn speed: {self.turn_speed:.2f} deg/s")

        # turn speed depends on current car velocity
        if self.velocity >= 0:
            self.turn_speed = max(self.min_turn_speed, (self.max_turn_speed * (exp(min((self.velocity + self.max_velocity / 3) / self.max_velocity, 1)) - 1) / (e-1)))
        else:
            self.turn_speed = max(self.min_turn_speed, (self.max_turn_speed * (exp(self.velocity / self.min_velocity) - 1) / (e-1)))

        # acceleration and breaks
        if self.braking:
            # left tire trail
            left_tire_position = self.position - self.facing_direction.rotate(-30) * self.sprite_rect.height * 3.5 / 2
            if left_tire_position not in self.tires_positions[0]:
                self.tires_positions[0].append(left_tire_position)
            # right tire trail
            right_tire_position = self.position - self.facing_direction.rotate(30) * self.sprite_rect.height * 3.5 / 2
            if right_tire_position not in self.tires_positions[1]:
                self.tires_positions[1].append(right_tire_position)
            # moving freely car slows down
            if self.velocity > 0:
                self.velocity -= self.brake_acceleration * frame_time_s
                # TODO: take these clippings out
                if self.velocity < 0:
                    self.velocity = 0
            elif self.velocity < 0:
                self.velocity += self.brake_acceleration * frame_time_s
                if self.velocity > 0:
                    self.velocity = 0
        elif self.input_vector.y:
            self.velocity += self.input_vector.y * self.acceleration * frame_time_s
        else:
            # if w/s are not pressed car eventually stops
            if self.velocity > 0:
                self.velocity -= self.acceleration * frame_time_s
                # TODO: same
                if self.velocity < 0:
                    self.velocity = 0
            elif self.velocity < 0:
                self.velocity += self.friction_acceleration * frame_time_s
                if self.velocity > 0:
                    self.velocity = 0

        # clearing tire trails
        if not self.braking:
            # TODO: save old trails
            if self.tires_positions[0] or self.tires_positions[1]:
                self.tires_positions = [[], []]

        # clipping speed
        if self.velocity > self.max_velocity and self.input_vector.y == 1:
            self.velocity = self.max_velocity
        elif self.velocity < self.min_velocity and self.input_vector.y == -1:
            self.velocity = self.min_velocity

        # turning
        if self.input_vector.x and self.velocity != 0:
            turn_direction = self.input_vector.x
            if self.velocity < 0:
                turn_direction *= -1

            if not self.braking:
                delta_angle = turn_direction * self.turn_speed * frame_time_s
            else:
                delta_angle = turn_direction * self.max_turn_speed * frame_time_s
            self.facing_direction.rotate_ip(-delta_angle)
            self.angle += delta_angle

        # moving coordinates
        if self.velocity:
            self.position += self.facing_direction * self.velocity * frame_time_s
            self.rect.center = self.position

        self.input_vector = Vector2()

    def draw(self, surface: Surface):
        # tire trails
        for tire in [0, 1]:
            for p1, p2 in zip(self.tires_positions[tire][:-1], self.tires_positions[tire][1:]):
                pygame.draw.line(surface, (127, 127, 127), p1, p2, 12)

        # car itself
        sprite = AssetPool.get_sprite(self.sprite_path)
        sprite.set_colorkey((0, 255, 0))
        sprite = pygame.transform.scale(sprite, [d * 4 for d in [self.sprite_rect.width, self.sprite_rect.height]])
        self.rect = sprite.get_rect(center=self.position)
        sprite = pygame.transform.rotate(sprite, self.angle)
        self.rect = sprite.get_rect(center=self.position)
        surface.blit(sprite, self.rect)
        # debug
        # pygame.draw.circle(surface, (255, 0, 0), self.position, 15, 1)
        # pygame.draw.line(surface, (255, 0, 0), self.position, self.position + self.facing_direction * 20)

