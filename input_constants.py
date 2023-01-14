from enum import Enum


class InputType(Enum):
    ACTION = 1
    STATE = 2
    RANGE = 3


class Action(Enum):
    EXECUTE = True
    STOP = False


class State(Enum):
    PRESSED = True
    RELEASED = False


if __name__ == "__main__":

    print("InputType Enum:")
    for input_type in InputType:
        print(f"\t{input_type.name} = {input_type.value}")

    print("Other Enum examples:")
    print(Action.EXECUTE)
    print(State.PRESSED)
