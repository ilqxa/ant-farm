from blocks.app import App

from src.buildings.processors import BuildingsController
from src.management.core import GlobalEnvironment

if __name__ == '__main__':
    ge = GlobalEnvironment()
    
    blocks = (
        BuildingsController(ge=ge),
    )
    
    App(blocks).run()