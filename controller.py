import pyautogui as pag 

class Controller:
    def __init__(self):
        pag.FAILSAFE = False  # Disable the fail-safe feature
        self.isClicking = False
        self.isRightClicking = False

    def move_cursor(self, x, y):
        screenWidth, screenHeight = pag.size()
        pag.moveTo(((1 - x) * screenWidth), y * screenHeight)
    
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
    