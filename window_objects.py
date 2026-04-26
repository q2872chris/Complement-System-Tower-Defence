class Mouse:
    def __init__(self):
        self.click = False
        self.scroll = False
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.focus = ""

    def set_focus(self, focus: str, override=False):
        if not self.focus or override:
            self.focus = focus

    def has_focus(self, *focuses: str) -> bool:
        if not focuses:
            return self.focus == ""
        return self.focus in focuses

    def release_focus(self, focus=""):
        if self.focus == focus:
            self.focus = ""

    def get_click(self, *focuses: str) -> bool:
        if not self.focus or self.focus in focuses:
            return self.click
        return False

    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

