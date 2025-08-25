from gestures import GestureTracking
from controller import Controller

controller = Controller()


def gestures_position_handler(x, y, isPinching, isSecondaryPinching):
    controller.move_cursor(x, y)
    if isPinching:
        controller.mouseDown()
    else:
        controller.mouseUp()
    
    if isSecondaryPinching:
        controller.rightClickDown()
    else:
        controller.rightClickUp()

def main():
    gestures = GestureTracking(gestures_position_handler)
    gestures.run(False)


if __name__ == "__main__":
    main()