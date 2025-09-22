from attendace_manager import AttendanceManager

def main():
    attendance_manager = AttendanceManager()
    attendance_manager.read_attendance_data()
    attendance_manager.finalize_points()
    attendance_manager.print_report()

if __name__ == "__main__":
    main()

