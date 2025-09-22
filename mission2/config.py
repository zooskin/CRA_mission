
from typing import Final
WEDNESDAY_BONUS: Final = 10
WEEKEND_BONUS: Final = 10

NORMAL_POINTS: Final = 1
TRAINING_POINTS: Final = 3
WEEKEND_POINTS: Final = 2


NORMAL_DAYS: Final = frozenset(["monday", "tuesday", "thursday", "friday"])
TRAINING_DAYS: Final = frozenset(["wednesday"])
WEEKEND_DAYS: Final = frozenset(["saturday", "sunday"])

GRADE_THRESHOLDS: Final = [
    ("GOLD", 50),
    ("SILVER", 30),
    ("NORMAL", 0),
]