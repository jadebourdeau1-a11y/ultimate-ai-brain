from core import Core

class CoreGUI:
    def __init__(self):
        self.brain = Core()
        self.brain.start()
        print("CoreGUI initialized and AI Brain started!")
