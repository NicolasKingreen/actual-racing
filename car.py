import pygame
from pygame.math import Vector2
from math import pi, exp, e
from pygame.surface import Surface


from asset_pool import AssetPool


class Car:
    def __init__(self, position: Vector2):
        self.position = position

        self.facing_direction = Vector2(0, -1)  # faces up
        self.angle = 0  # TODO: take it from facing direction vector
        self.velocity = 0

        self.max_velocity = 500
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

    def update(self, frame_time_s):
        # print(self.position, round(self.velocity, 2), self.angle, self.facing_direction, self.input_vector)
        print(f"Velocity: {self.velocity:.2f} px/s, Braking: {self.braking}, Turn speed: {self.turn_speed:.2f} deg/s")

        # turn speed depends on current car velocity
        if self.velocity >= 0:
            self.turn_speed = max(self.min_turn_speed, (self.max_turn_speed * (exp(self.velocity / self.max_velocity) - 1) / (e-1)))
        else:
            self.turn_speed = max(self.min_turn_speed, (self.max_turn_speed * (exp(self.velocity / self.min_velocity) - 1) / (e-1)))

        # acceleration and breaks
        if self.braking:
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

        # clipping speed
        if self.velocity > self.max_velocity and self.input_vector.y == 1:
            self.velocity = self.max_velocity
        elif self.velocity < self.min_velocity and self.input_vector.y == -1:
            self.velocity = self.min_velocity

        # turning
        if self.input_vector.x and self.velocity != 0:
            if self.velocity >= 0:
                turn_direction = self.input_vector.x
            elif self.velocity < 0:
                turn_direction = -self.input_vector.x
            delta_angle = turn_direction * self.turn_speed * frame_time_s
            self.facing_direction.rotate_ip(-delta_angle)
            self.angle += delta_angle

        # moving coordinates
        if self.velocity:
            self.position += self.facing_direction * self.velocity * frame_time_s
            self.rect.center = self.position

    def draw(self, surface: Surface):
        sprite = AssetPool.get_sprite(self.sprite_path)
        sprite = pygame.transform.scale(sprite, [d * 4 for d in [self.sprite_rect.width, self.sprite_rect.height]])
        self.rect = sprite.get_rect(center=self.position)
        sprite = pygame.transform.rotate(sprite, self.angle)
        self.rect = sprite.get_rect(center=self.position)
        surface.blit(sprite, self.rect)
        # debug
        # pygame.draw.circle(surface, (255, 0, 0), self.position, 15, 1)
        # pygame.draw.line(surface, (255, 0, 0), self.position, self.position + self.facing_direction * 20)

