import pytest
from attendace_manager import AttendanceManager
from config import GRADE_THRESHOLDS


def test_singleton_identity():
    AttendanceManager.reset_instance()
    a = AttendanceManager()
    b = AttendanceManager()
    assert a is b

def test_init_early_return():
    AttendanceManager.reset_instance()
    a = AttendanceManager()
    a.some_marker = 123
    b = AttendanceManager()
    assert a is b
    assert getattr(b, 'some_marker') == 123

def test_add_record_and_finalize():
    AttendanceManager.reset_instance()
    m = AttendanceManager()
    m.add_member('alice')
    m.record_attendance('alice', 'monday')
    m.record_attendance('alice', 'wednesday')
    # before finalize, bonus not applied yet
    assert m.members['alice'].point == 1 + 3
    m.finalize_points()
    # after finalize, wednesday bonus added
    assert m.members['alice'].point == 1 + 3 + 10
    assert m.members['alice'].grade in [g for g, _ in GRADE_THRESHOLDS]


def test_read_attendance_data(tmp_path):
    AttendanceManager.reset_instance()
    p = tmp_path / "att.txt"
    p.write_text("alice monday\nbob saturday\n \n han \n#comment\ncarol wednesday\n")
    m = AttendanceManager()
    processed = m.read_attendance_data(str(p))
    assert processed == 3
    assert 'alice' in m.members and 'bob' in m.members and 'carol' in m.members

def test_read_attendance_file_not_found(capsys, tmp_path):
    AttendanceManager.reset_instance()
    m = AttendanceManager()
    missing = tmp_path / "no_such_file.txt"
    m.read_attendance_data(str(missing))
    captured = capsys.readouterr()
    assert "파일을 찾을 수 없습니다." in captured.out

def test_custom_grade_thresholds():
    AttendanceManager.reset_instance()
    custom = [('PLAT', 5), ('GOLD', 3), ('NORMAL', 0)]
    m = AttendanceManager(grade_thresholds=custom)
    m.add_member('d')
    m.members['d'].point = 6
    m.classify_grade(m.members['d'])
    assert m.members['d'].grade == 'PLAT'

def test_init_grade_val_filters_and_empty():
    AttendanceManager.reset_instance()
    raw = [('A', 5), ('BAD',), 'x', ('B', '2')]
    m = AttendanceManager(grade_thresholds=raw)
    names = [n for n, _ in m.grade_thresholds]
    assert 'A' in names and 'B' in names

    # now test empty thresholds
    AttendanceManager.reset_instance()
    m2 = AttendanceManager(grade_thresholds=[])
    assert m2.lowest_grade_name == 'NORMAL'

def test_print_report_and_removed_players(capsys):
    AttendanceManager.reset_instance()
    m = AttendanceManager()
    m.add_member('to_remove')
    m.add_member('keep')
    m.members['keep'].attended_weekend = True
    m.members['keep'].grade = m.lowest_grade_name

    m.print_report()
    out = capsys.readouterr().out
    assert 'Attendance Report' in out
    assert 'Removed player' in out
    assert 'to_remove' in out
    assert 'keep' in out


def test_record_attendance_no_member_noop():
    AttendanceManager.reset_instance()
    m = AttendanceManager()
    m.record_attendance('ghost', 'monday')
    assert 'ghost' not in m.members


def test_add_bonus_points_applies():
    AttendanceManager.reset_instance()
    m = AttendanceManager()
    m.add_member('x')
    member = m.members['x']
    member.attended_training = True
    member.attended_weekend = True
    member.point = 0
    m.add_bonus_points(member)
    assert member.point > 0
