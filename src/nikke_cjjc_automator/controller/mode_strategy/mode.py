from abc import ABC, abstractmethod
from typing import Any

class ModeStrategy(ABC):
    @abstractmethod
    def run(self, context: Any) -> None:
        pass

class ModeContext:
    def __init__(self, strategy: ModeStrategy):
        self.strategy = strategy
    def execute(self, context: Any) -> None:
        self.strategy.run(context)
