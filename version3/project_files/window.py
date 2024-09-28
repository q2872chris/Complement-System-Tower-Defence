import pyglet as py
from pyglet.window import key
from project_files import gui, sprites

class Window(py.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        py.gl.glClearColor(0, 0.7, 1, 1)
        self.set_location(340, 50)
        # py.clock.schedule(self.update)
        self.batch = py.graphics.Batch()
        image1 = py.image.load("test.png")
        image1.width = 80
        image1.height = 80
        image1.anchor_x = -10
        image1.anchor_y = -10
        image2 = py.image.SolidColorImagePattern((0, 255, 0, 255)).create_image(100, 100)
        image3 = py.image.SolidColorImagePattern((0, 0, 255, 255)).create_image(100, 100)
        self.button1 = gui.button1(100, 100, image1,
                                   image2, image3, batch=self.batch)

        image5 = py.image.SolidColorImagePattern((255, 255, 255, 255)).create_image(30, 30)
        sprite = sprites.ImageSprite(800, 50, image5, self.batch)


        self.slider = gui.Scroller(sprite, 0, 600)


    def on_key_press(self, symbol, modifiers):
        match symbol:
            case key.ESCAPE:
                self.close()
            case _:
                pass

    def update(self, dt):
        pass

    def on_draw(self):
        self.clear()
        self.push_handlers(self.button1)
        self.push_handlers(self.slider)
        self.batch.draw()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass



