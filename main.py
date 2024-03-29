from aztecDiamond import AztecDiamond
from resizeTracker import ResizeTracker
from menuBar import MenuBar
from tkinter import Tk

def main():
    x = 1000
    y = 600
    root = Tk()
    ad = AztecDiamond(x, y)
    tracker = ResizeTracker(ad)
    menubar = MenuBar(root, ad)

    root.geometry(str(x)+"x"+str(y)+"+300+300")
    root.mainloop()

if __name__ == '__main__':
    main()
