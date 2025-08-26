from gestures import GestureTracking
from controller import Controller
import threading

controller = Controller()

X_COORD = 0
Y_COORD = 0
IS_PINCHING = False
IS_SECONDARY_PINCHING = False

def update_coords(x, y, isPinching, isSecondaryPinching):
    global X_COORD, Y_COORD, IS_PINCHING, IS_SECONDARY_PINCHING
    X_COORD = x
    Y_COORD = y
    IS_PINCHING = isPinching
    IS_SECONDARY_PINCHING = isSecondaryPinching

def move_mouse():
    while True:
        controller.move_cursor(X_COORD, Y_COORD)
        if IS_PINCHING:
            controller.mouseDown()
        else:
            controller.mouseUp()

        if IS_SECONDARY_PINCHING:
            controller.rightClickDown()
        else:
            controller.rightClickUp()

def main():
    gestures = GestureTracking(update_coords)
    t1 = threading.Thread(target=gestures.run)
    t2 = threading.Thread(target=move_mouse)

    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    main()