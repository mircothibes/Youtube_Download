import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))

from app.gui import run

if __name__ == "__main__":
    run()
