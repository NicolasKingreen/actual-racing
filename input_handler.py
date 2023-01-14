# source: command pattern realisation (https://codereview.stackexchange.com/questions/55365/input-handling-system-using-the-command-pattern)
from abc import ABC, abstractmethod
import pygame

# enums
from input_constants import InputType, Action, State


class ICommand(ABC):

    @abstractmethod
    def execute(self):
        pass

    def get_input_type(self):
        # what's there?
        pass


# theese should be somewhere else I guess
class CarBrakeCommand(ICommand):
    def execute(self, car):
        car.braking = True


class CarResetCommand(ICommand):
    def execute(self, car):
        car.reset()


class InputHandler:

    def __init__(self):
        self.brake_command: ICommand = CarBrakeCommand()
        self.reset_command: ICommand = CarResetCommand()

        self.commands = dict()
        self.commands[pygame.K_SPACE] = self.brake_command
        self.commands[pygame.K_r] = self.reset_command

        self.state_map = dict()
        self.action_map = dict()

    def bind(self, key, command: ICommand):
        self.commands[key] = command

    def generate_input_commands(self, command_queue):
        exit = self.convert_inputs_to_actions()
        if exit:
            return True
        else:
            self.fill_command_queue(command_queue)
            self.action_map.clear()
            return False

    def convert_inputs_to_actions(self):
        # gets asked in game loop event handle / true if game should exit
        # then in game loop update commands get executed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                self.keydown(event)
            elif event.type == pygame.KEYUP:
                self.keyup(event)
        return False

    def fill_command_queue(self, command_queue):
        # command_queue is a mutable list? yeah
        # command_queue comes from game loop
        for key, command in self.commands.items():
            if self.is_held(key) and command.get_input_type() == STATE:
                command_queue.append(command)
            elif self.was_pressed(key) and command.get_input_type() == ACTION:
                command_queue.append(command)
        command_queue.append(self.reset_command)

    def keydown(self, event):
        if self.state_map[event.key] == RELEASED:
            self.action_map[event.key] = EXECUTE
        self.state_map[event.key] = PRESSED

    def keyup(self, event):
        self.state_map[event.key] = RELEASED

    def is_held(self, key):
        return self.state_map[key]

    def was_pressed(self, key):
        return self.action_map[key]


if __name__ == '__main__':
    pass
