import threading

from config import (
    NORMAL_DAYS,
    TRAINING_DAYS,
    WEEKEND_DAYS,
    GRADE_THRESHOLDS,
    NORMAL_POINTS,
    TRAINING_POINTS,
    WEEKEND_POINTS,
    WEDNESDAY_BONUS,
    WEEKEND_BONUS,
)

class Member:
    def __init__(self, name):
        self.point = 0
        self.grade = "NORMAL"
        self.name = name
        self.attended_training = False
        self.attended_weekend = False
   
class AttendanceManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def reset_instance(cls):
        with cls._lock:
            if cls._instance is not None:
                delattr(cls._instance, '_initialized')
            cls._instance = None

    def __init__(self, grade_thresholds: list[tuple[str, int]] | None = None):
        if getattr(self, '_initialized', False):
            return
        self.members = {}
        self.init_grade_val(grade_thresholds)
        self._initialized = True

    def init_grade_val(self, grade_thresholds):
        raw = grade_thresholds if grade_thresholds is not None else GRADE_THRESHOLDS
        cleaned: list[tuple[str, int]] = []
        for item in raw:
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                continue
            name, thr = item[0], int(item[1])
            cleaned.append((str(name), thr))
        cleaned.sort(key=lambda x: x[1], reverse=True)
        self.grade_thresholds = cleaned
        self.lowest_grade_name = cleaned[-1][0] if cleaned else "NORMAL"

    def add_member(self, name):
        if name not in self.members:
            self.members[name] = Member(name)

    def record_attendance(self, name, day):
        day = day.lower()
        if name in self.members:
            member = self.members[name]
            if day in NORMAL_DAYS:
                member.point += NORMAL_POINTS
            elif day in TRAINING_DAYS:
                member.point += TRAINING_POINTS
                member.attended_training = True
            elif day in WEEKEND_DAYS:
                member.point += WEEKEND_POINTS
                member.attended_weekend = True

    def finalize_points(self):
        for member in self.members.values():
            self.add_bonus_points(member)
            self.classify_grade(member)

    def add_bonus_points(self, member):
        if member.attended_training:
            member.point += WEDNESDAY_BONUS
        if member.attended_weekend:
            member.point += WEEKEND_BONUS

    def classify_grade(self, member):
        for grade_name, threshold in self.grade_thresholds:
            if member.point >= threshold:
                member.grade = grade_name
                return

    def print_report(self):
        print("Attendance Report")
        print("=================")
        for member in self.members.values():
            print(f"NAME : {member.name}, POINT : {member.point}, GRADE : {member.grade}")

        print("\nRemoved player")
        print("==============")
        for member in self.members.values():
            if member.grade == self.lowest_grade_name and not member.attended_training and not member.attended_weekend:
                print(member.name)
    
    def read_attendance_data(self, filename="attendance_weekday_500.txt"):
        try:
            with open(filename, encoding='utf-8') as f:
                for lineno, raw in enumerate(f, start=1):
                    line = raw.strip()
                    if not line:
                        continue
                    if line.startswith('#'):
                        continue
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    name, day = parts[0], parts[1]
                    self.add_member(name)
                    self.record_attendance(name, day)
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
        return len(self.members)