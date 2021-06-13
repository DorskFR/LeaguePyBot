from .mouse import Mouse


class Reporter:
    def __init__(self):
        self.mouse = Mouse(0.1)

    def click_report_window(self):
        self.mouse.set_position_and_click(800, 400)
        self.mouse.set_position_and_click(800, 445)
        self.mouse.set_position_and_click(800, 565)
        self.mouse.set_position_and_click(960, 765)

    def click_report_player(self, x: int, y: int):
        self.mouse.set_position_and_click(x, y)

    def report_all_players(self):
        x = 526
        y = 300
        for i in range(0, 10):
            self.click_report_player(x, y)
            self.click_report_window()
            y += 35
            if i == 4:
                y = 520
