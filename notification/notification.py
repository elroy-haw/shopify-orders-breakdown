from abc import ABC, abstractmethod
from enum import Enum


class Notification(ABC):
    @abstractmethod
    def notify(self, breakdowns: dict) -> Exception:
        pass


class NotificationType(Enum):
    EMAIL = "email"
