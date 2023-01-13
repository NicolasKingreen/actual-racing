import pygame
import os


from asset_pool import AssetPool
from car import Car


WIN_SIZE = 1920, 1280
WIN_WIDTH, WIN_HEIGHT = WIN_SIZE
TARGET_FPS = 0


class Application:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Racing Game")
        self.screen = pygame.display.set_mode(WIN_SIZE, pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
        self.is_running = False

        self.car = Car(pygame.Vector2(WIN_WIDTH/2, WIN_HEIGHT/2))

    def run(self):
        self.is_running = True
        while self.is_running:

            frame_time_ms = self.clock.tick(TARGET_FPS)
            frame_time_s = frame_time_ms / 1000.
            print(f"\nFPS: {int(self.clock.get_fps())}")

            self._handle_events()
            self._update_states(frame_time_s)
            self._draw_graphics()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()
                elif event.key == pygame.K_w:
                    self.car.input_vector.y = 1
                elif event.key == pygame.K_s:
                    self.car.input_vector.y = -1
                elif event.key == pygame.K_a:
                    self.car.input_vector.x = 1
                elif event.key == pygame.K_d:
                    self.car.input_vector.x = -1
                elif event.key == pygame.K_SPACE:
                    self.car.braking = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_w, pygame.K_s]:
                    self.car.input_vector.y = 0
                elif event.key in [pygame.K_a, pygame.K_d]:
                    self.car.input_vector.x = 0
                elif event.key == pygame.K_SPACE:
                    self.car.braking = False

    def _update_states(self, frame_time_s):
        self.car.update(frame_time_s)

    def _draw_graphics(self):
        self.screen.fill((45, 191, 10))
        self.car.draw(self.screen)
        pygame.display.update()

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    Application().run()
