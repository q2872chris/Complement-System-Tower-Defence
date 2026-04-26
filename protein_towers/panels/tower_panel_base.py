import pyglet as py
from abc import ABC
from drawables import BRect, Line, Label, Button
from globals import game_attrs

g = py.graphics.OrderedGroup


class BaseTowerPanel(ABC):
    batch = game_attrs.batch

    def __init__(self, tower, previous_panel):
        self.mouse = game_attrs.mouse
        self.placed_towers = game_attrs.placed_towers
        self.proteins = game_attrs.proteins
        self.game_attrs = game_attrs
        self.tower = tower
        self.line = Line(200, 0, 200, 600, 4, (200, 0, 200), self.batch, g(4))
        self.side_panel = BRect(0, 0, 200, 470, 5, (70, 0, 0), (200, 0, 200), self.batch, g(7))
        self.top_panel = BRect(0, 470, 199, 130, 5, (0, 0, 0), (200, 0, 200), self.batch, g(8))
        self.tower_name = Label(tower.name, 100, 570, 25, (255, 255, 0, 255),
                                self.batch, g(9))
        self.tower_cost = Label(f"Sell price: £{tower.sell_cost}", 100, 540, 18,
                                (0, 255, 255, 255), self.batch, g(9))
        self.target_button = Button(
            f"Targeting: {tower.target_mode}", 100, 511, 16, 17, (100, 200, 0, 200),
            (120, 220, 0, 255), self.batch, g(9), italic=True, quick_action=self.retarget
        )
        self.pop_count = Label(f"Pop count: {tower.pop_count}", 100, 488, 14,
                               (255, 255, 255, 255), self.batch, g(9))
        self.tower_game_info = Label(tower.game_info, 10, 260, 14, (255, 255, 255, 255), self.batch,
                                     g(8), anchor_x="left", anchor_y="top", multiline=True)
        self.tower_info = Label(tower.info, 10, 460, 13, (255, 255, 255, 255), self.batch,
                                g(8), anchor_x="left", anchor_y="top", multiline=True)
        self.tower_info.hide()
        self.info_button = Button(
            "Protein Info", 100, 30, 18, 20, (0, 0, 200, 200), (0, 0, 240, 255), self.batch, g(8),
            off_action=self.info_button_off, on_action=self.info_button_on
        )
        self.all_objects = self.get_all_drawable_objects()
        self.buttons = self.get_buttons()
        self.main_panel_items = self.get_main_panel_items()
        self.side = "left"
        self.active = True
        self.initialise(tower, previous_panel)
        self.tower.circle.show()

    def initialise(self, tower, previous_panel):
        if previous_panel is None:
            self.position_panel(tower.x)
        else:
            self.position_panel(tower.x, previous_panel.side)
            if previous_panel.info_button.on:
                for i in self.main_panel_items:
                    i.hide()
                self.info_button.switch_colours()
            previous_panel.deactivate()

    def position_panel(self, x: int, side="none"):
        if side == "left":
            return
        if side == "right" or x < 350:
            self.side = "right"
            for i in self.all_objects:
                i.x += 700
                if hasattr(i, "x2"):
                    i.x2 += 700

    def get_all_drawable_objects(self):
        """Call location must be considered or there will be duplicates/misses."""
        objects = []
        for i in self.__dict__.values():
            if type(i) is list and all(hasattr(j, "visible") for j in i):
                objects += i
            elif hasattr(i, "visible"):
                objects.append(i)
        return objects

    def get_main_panel_items(self):
        return [i for i in self.all_objects if not
        (i.group.order == 7 or getattr(i, "text", "") == "Protein Info" or i.y >= 470)]

    def get_buttons(self):
        return [i for i in self.all_objects if isinstance(i, Button)]

    def deactivate(self):
        if self.info_button.on:
            self.info_button.switch_colours()
        for i in self.all_objects:
            i.hide()
            i.delete()
        self.tower.circle.hide()
        del self.tower
        self.active = False

    def update(self):
        self.pop_count.text = f"Pop count: {self.tower.pop_count}"
        if self.tower not in self.placed_towers:
            self.deactivate()
        for i in self.buttons:
            if i.visible:
                i.hover(self.mouse)

    def retarget(self):
        targets = ("First", "Last", "Strong", "Weak")
        new_target = targets[(targets.index(self.tower.target_mode) + 1) % 4]
        self.tower.target_mode = new_target
        self.target_button.text = "Targeting: " + new_target

    def info_button_on(self):
        for item in self.main_panel_items:
            item.hide()
        self.tower_info.show()

    def info_button_off(self):
        for item in self.main_panel_items:
            item.show()
        self.tower_info.hide()

    def collide_point(self, point: tuple[int, int]) -> bool:
        return point[0] < 200 if self.side == "left" else point[0] > 700

    def __contains__(self, point: tuple[int, int]) -> bool:
        return self.collide_point(point)




