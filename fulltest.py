import time

def get_current_time():
    # Get the current date and time
    time1 = time.localtime() # get struct_time
    time_string = time.strftime("%d/%m/%Y, %H:%M", time1)

    return time_string
#--------------------------------------------------------------------------------------------------------------------------------------------
import os

class ClassroomManagementSystem:
    def __init__(self):
        self.students = {}
        self.timetables = {}
        self.assignments = {}

    def load_initial_data(self):
        self.load_attendance_data()
        self.load_timetable_data()
        self.load_assignment_data()

    def load_attendance_data(self):
        with open('attendance_StudentID.txt', 'r') as file:
            for line in file:
                student_id, *attendance = line.strip().split(',')
                self.students[student_id] = {'attendance': attendance}

    def load_timetable_data(self):
        with open('timetables_StudentID.txt', 'r') as file:
            for line in file:
                course_code, course_name, instructor, room_number, *time_slots = line.strip().split(',')
                self.timetables[course_code] = {'course_name': course_name, 'instructor': instructor,
                                                    'room_number': room_number, 'time_slots': time_slots}

    def load_assignment_data(self):
        with open('assignments_StudentID.txt', 'r') as file:
            for line in file:
                course_code, student_id, assignment_status = line.strip().split(',')
                if course_code not in self.assignments:
                    self.assignments[course_code] = {}
                self.assignments[course_code][student_id] = assignment_status

    def check_student_valid(self, student_id):
        studentid = student_id
        if studentid == "10001":
            studentname = "Cheong Cheng Yi Danny"
        elif studentid == "10002":
            studentname = "A"
        elif studentid == "10003":
            studentname = "B"
        else:
            print("Haven't Register!!")
            exit()
        return studentname, student_id
    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    import os
    def mark_attendance(self, student_id, course_code, class_time):
    # Record attendance for the student in the specified class
        if course_code in self.timetables:
            if student_id in self.students:
                current_time = get_current_time()
                class_start_time = time.strptime(class_time, "%H:%M")
                fifteen_minutes_after_start = class_start_time.replace(minute=class_start_time.minute + 15)
                
                if current_time <= fifteen_minutes_after_start:
                    if 'attendance' not in self.students[student_id]:
                        self.students[student_id]['attendance'] = []

                    self.students[student_id]['attendance'].append(course_code)
                else:
                    print("Attendance cannot be marked after the first 15 minutes of the class.")
            else:
                print("Student ID not found.")
        else:
            print("Course code not found in timetables.")

    def calculate_attendance_percentage(self, student_id):
    # Calculate and display attendance percentage for the student
        if student_id in self.students:
            total_classes = len(self.timetables)
            attended_classes = sum(1 for course in self.students[student_id].get('attendance', []) if course in self.timetables)
            
            if total_classes > 0:
                return (attended_classes / total_classes) * 100
            else:
                return 0
        else:
            print("Student ID not found.")
            return 0
    #-------------------------------------------------------------------------------------------------------------------------------------------------
    def create_timetable(self):
        course_code = input("Enter course code: ")
        course_name = input("Enter course name: ")
        instructor = input("Enter instructor's name: ")
        room_number = input("Enter room number: ")
        time_slots = input("Enter time slots: ")

        self.timetables[course_code] = {'course_name': course_name, 'instructor': instructor,
                                            'room_number': room_number, 'time_slots': time_slots}


    def update_timetable(self, course_code, updated_timetable):
    # Update an existing timetable entry
        if course_code in self.timetables:
            self.timetables[course_code].update(updated_timetable)

    def delete_timetable(self, course_code):
    # Delete a timetable entry
        if course_code in self.timetables:
            del self.timetables[course_code]
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    def submit_assignment(self, student_id, course_code, assignment_status):
    # Check if the course code already exists in assignments
        if course_code in self.assignments:
            # Check if the student ID already exists for the given course code
            if student_id in self.assignments[course_code]:
                # Update the assignment status for the existing student ID
                self.assignments[course_code][student_id] = assignment_status
            else:
                # If the student ID doesn't exist, add a new entry for it
                self.assignments[course_code][student_id] = assignment_status
        else:
            # If the course code doesn't exist, create a new entry for it
            self.assignments[course_code] = {student_id: assignment_status}

        # Example usage:
        # Assuming 'self.assignments' is a dictionary containing assignments
        # Instantiate your class and call the submit_assignment method with the student ID, course code, and assignment status
        # For example:
        # my_instance.submit_assignment('123', 'CS101', 'submitted')
        
    def check_assignment_status(self, student_id, course_code):
    # Check if the course code exists in assignments
        if course_code in self.assignments:
            # Check if the student ID exists for the given course code
            if student_id in self.assignments[course_code]:
                # Return the assignment status if found
                return self.assignments[course_code][student_id]
            else:
                # Return a message indicating that the student ID is not found
                return f"Student ID '{student_id}' not found for course '{course_code}'."
        else:
            # Return a message indicating that the course code is not found
            return f"Course code '{course_code}' not found."

        # Example usage:
        # Assuming 'self.assignments' is a dictionary containing assignments
        # Instantiate your class and call the check_assignment_status method with the student ID and course code
        # For example:
        # my_instance.check_assignment_status('123', 'CS101')

    def update_assignment_status(self, student_id, course_code, new_status):
        if course_code in self.assignments and student_id in self.assignments[course_code]:
            self.assignments[course_code][student_id] = new_status
        else:
            # If the course or student is not found in the assignments dictionary
            # you can handle this case based on your requirements.
            # For example, you may raise an exception or log a message.
            # Here, I'm printing a message indicating that the assignment status cannot be updated.
            print("Assignment status update failed: Course or student not found.")
    #---------------------------------------------------------------------------------------------------------------------------------------
    def display_attendance_records(self):
        print("Attendance Records:")
        for student_id, data in self.students.items():
            attendance_list = ", ".join(data.get('attendance', []))  # Get attendance list or empty list if not available
            print(f"Student ID: {student_id}, Attendance: {attendance_list}")

    def display_timetables(self):
        print("Timetables:")
        for course_code, data in self.timetables.items():
            time_slots = ', '.join(data.get('time_slots', []))  # Get time slots or empty list if not available
            instructor = data.get('instructor', 'N/A')  # Get instructor or 'N/A' if not available
            room_number = data.get('room_number', 'N/A')  # Get room number or 'N/A' if not available
            print(f"Course Code: {course_code}, Course Name: {data['course_name']}, Instructor: {instructor},"
                f" Room Number: {room_number}, Time Slots: {time_slots}")

    def display_assignment_statuses(self):
        print("Assignment Submission Statuses:")
        for course_code, students in self.assignments.items():
            print(f"Course Code: {course_code}")
            for student_id, status in students.items():
                print(f"Student ID: {student_id}, Status: {status}")
    #--------------------------------------------------------------------------------------------------------------------------------------------------
    def write_updated_data_to_files(self):
        self.write_attendance_data_to_file()
        self.write_timetable_data_to_file()
        self.write_assignment_data_to_file()

    def write_attendance_data_to_file(self):
        with open('attendance_StudentID.txt', 'w') as file:
            for student_id, data in self.students.items():
                file.write(f"{student_id},{','.join(data['attendance'])}\n")

    def write_timetable_data_to_file(self):
        with open('timetables_StudentID.txt', 'w') as file:
            for course_code, data in self.timetables.items():
                file.write(f"{course_code},{data['course_name']},{data['instructor']},{data['room_number']},"
                            f"{','.join(data['time_slots'])}\n")

    def write_assignment_data_to_file(self):
        with open('assignments_StudentID.txt', 'w') as file:
            for course_code, students in self.assignments.items():
                for student_id, status in students.items():
                    file.write(f"{course_code},{student_id},{status}\n")
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def check_validation(self):
        print("Welcome to EduHub University")
        student_id = input("Please Enter Your StudentID: ")
        self.check_student_valid(student_id)
        student_name = self.check_student_valid(student_id)

        return student_name, student_id



    def display_menu(self):
        print(f"Welcome, student_name!")
        print("[1] Mark Attendance")
        print("[2] Manage Timetables")
        print("[3] Submit/Check Assignments")
        print("[4] Display")
        print("[5] Exit Program")

    def execute_menu_option(self, userInput):
        if userInput == "1": # Mark Attendance
                print("---Mark Attendance---")
                print("[1] Checkin Attendance")
                print("[2] Attendance Percentages")
                print("[3] Back to Homepage")
                userInputAttendance = input("Please Enter Your Selection. ")
                if userInputAttendance == "1":
                    print("---Checkin Attendance---")
                elif userInputAttendance == "2":
                    print("---Attendance Percentages---")


                elif userInputAttendance == "3":
                    print("---Back to Homepage---")
                    
                else:
                    print("Invaild Selection!!")



        elif userInput == "2": # Manage Timetables
            print("[1] Modify Timetable")
            print("[2] Display the Current Timetables")
            print("[3] Back to Homepage")
            userInput = input("Please Enter Your Selection. ")
            if userInput == "1":
                print("---Modify Timetable---")
                print("[1] Create Timetable")
                print("[2] Update Timetable")
                print("[3] Delete Timetable")
                print("Back To Homepage")
                userInput1 = input("Please Enter Your Selection. ")

                if userInput1 == "1":
                    print("---Create Timetable---")
                    self.create_timetable(self)
                elif userInput == "2":
                    print("---Update Timetable---")
                elif userInput == "3":
                    print("---Delete Timetable---")
                elif userInput == "4":
                    print()
                else:
                    print("Invalid Selection!!")
            elif userInput == "2":
                print()
            elif userInput == "3":
                print()
            else:
                print("Invaild Selection!!")


        elif userInput == "3": # Submit/Check Assignments
            print("[1] Submittion")
            print("[2] Check Submittion Status")
            print("[3] Update Assignment Status")
            print("[4] Back to Homepage")
            userInputsub = input("Please Enter Your Selection. ")
            if userInputsub == "1":
                print("---Submittion---")
            elif userInputsub == "2":
                print("---Check Submittion Status---")
            elif userInputsub == "3":
                print("---Update Assignment Status---")
            elif userInputsub == "4":
                print("---Back to Homepage---")
            else:
                print("Invaild Selection!!")


        elif userInput == "4": # Display
            print()


        elif userInput == "5": #  Exit
            self.write_updated_data_to_files()
            print("Exiting...")
            exit()

        else: # Invalid Selection
            print("")
            print("Invaild Selection!!")
            print("")
        
# Initialize the Classroom Management System
cms = ClassroomManagementSystem()
cms.load_initial_data()

# Main loop to execute the program
while True:
    cms.display_menu()
    userInput = input("Enter Your Choice: ")
    cms.execute_menu_option(userInput)
