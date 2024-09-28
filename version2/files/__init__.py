from pyglet import app
from files import engine
from files.data import window_data as win

def start_engine(x=900, y=600, name="(Pyglet) Complement System Tower Defence",
                 resizable=False, fullscreen=False):
    win.initialise(x, y)
    engine.window(x, y, name, resizable=resizable, fullscreen=fullscreen)
    app.run()


# eventually add group sprite calculator
