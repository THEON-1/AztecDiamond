from tkinter import Menu

class MenuBar(Menu):
    
    def __init__(self, root, aztecDiamond):
        super().__init__(root)
        self.aztecDiamond = aztecDiamond
        root.config(menu=self)

        self.growLock = False

        self.add_command(label="Grow", command=self.growDiamond)
        self.add_command(label="Color", command=self.toggleColor)
        self.add_command(label="NoBlack", command=self.toggleBlack)
    
    def growDiamond(self):
        if ~self.growLock:
            self.growLock = ~self.growLock
            self.aztecDiamond.grow_and_draw()
            self.aztecDiamond.update()
            self.growLock = ~self.growLock

    def toggleColor(self):
        self.aztecDiamond.direction_colored =  not self.aztecDiamond.direction_colored
        self.aztecDiamond.place()
    
    def toggleBlack(self):
        self.aztecDiamond.black = not self.aztecDiamond.black
        self.aztecDiamond.place()