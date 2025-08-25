import pyautogui as pag 

class Controller:
    def __init__(self):
        pag.FAILSAFE = False  # Disable the fail-safe feature
        self.isClicking = False
        self.isRightClicking = False
        self.screenWidth, self.screenHeight = pag.size()

    def move_cursor(self, x, y):
        pag.moveTo(((1 - x) * self.screenWidth), y * self.screenHeight, duration=0.1, tween=pag.linear)

    def mouseDown(self):
        if (self.isClicking):
            return
        pag.mouseDown()
        self.isClicking = True
    
    def mouseUp(self):
        if (not self.isClicking):
            return
        pag.mouseUp()
        self.isClicking = False

    def rightClickDown(self):
        if (self.isRightClicking):
            return
        pag.mouseDown(button='right')
        self.isRightClicking = True
    
    def rightClickUp(self):
        if (not self.isRightClicking):
            return
        pag.mouseUp(button='right')
        self.isRightClicking = False
    