from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict


class Notification(ABC):
    @abstractmethod
    def notify(self, breakdowns: Dict[str, Dict[str, Dict[str, str]]]) -> Exception:
        pass


class NotificationType(Enum):
    EMAIL = "email"
