GOLD_POINT = 50
SILVER_POINT = 30
WEDNESDAY_BONUS = 10
WEEKEND_BONUS = 10

NORMAL_POINTS = 1
TRAINING_POINTS = 3
WEEKEND_POINTS = 2

NORMAL_DAYS = ["monday", "tuesday", "thursday", "friday"]
TRAINING_DAYS = ["wednesday"]
WEEKEND_DAYS = ["saturday", "sunday"]

class Member:
    def __init__(self, name):
        self.point = 0
        self.grade = "NORMAL"
        self.name = name
        self.attended_training = False
        self.attended_weekend = False

def add_member(name, members):
    if name not in members:
        members[name] = Member(name)

def record_attendance(name, day, members):
    day = day.lower()
    if name in members:
        member = members[name]
        if day in NORMAL_DAYS:
            member.point += NORMAL_POINTS
        elif day in TRAINING_DAYS:
            member.point += TRAINING_POINTS
            member.attended_training = True
        elif day in WEEKEND_DAYS:
            member.point += WEEKEND_POINTS
            member.attended_weekend = True

def finalize_points(members):
    for member in members.values():
        add_bonus_points(member)
        classify_grade(member)

def add_bonus_points(member):
    if member.attended_training:
        member.point += WEDNESDAY_BONUS
    if member.attended_weekend:
        member.point += WEEKEND_BONUS

def classify_grade(member):
    if member.point >= GOLD_POINT:
        member.grade = "GOLD"
    elif member.point >= SILVER_POINT:
        member.grade = "SILVER"
    else:
        member.grade = "NORMAL"

def print_report(members):
    print("Attendance Report")
    print("=================")
    for member in members.values():
        print(f"NAME : {member.name}, POINT : {member.point}, GRADE : {member.grade}")

    print("\nRemoved player")
    print("==============")
    for member in members.values():
        if member.grade == "NORMAL" and not member.attended_training and not member.attended_weekend:
            print(member.name)

def read_attendance_data(members):
    try:
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
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
                add_member(name, members)
                record_attendance(name, day, members)

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

def process_attendance(members):
    finalize_points(members)
    print_report(members)

def main():
    members = {}
    read_attendance_data(members)
    process_attendance(members)

if __name__ == "__main__":
    main()

