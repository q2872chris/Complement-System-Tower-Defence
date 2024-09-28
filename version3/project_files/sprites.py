import pyglet as py

class ImageSprite:
    def __init__(self, x: int, y: int, image: py.image.AbstractImage,
                 batch: py.graphics.Batch, scale=1):
        self.sprite = py.sprite.Sprite(image, x, y, 0, batch=batch)
        self.sprite.scale = scale

    def __contains__(self, item: tuple[int, int]):
        x, y = item
        sx, sy, sz = self.sprite.position
        w, h = self.sprite.width, self.sprite.height
        return sx < x < sx + w and sy < y < sy + h

    def __getattr__(self, item: str):
        return getattr(self.sprite, item)
