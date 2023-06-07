from collections import defaultdict


class Logger:
    def __init__(self) -> None:
        self.current_turn: int = 0

        self.history: defaultdict[int, list] = defaultdict(list)