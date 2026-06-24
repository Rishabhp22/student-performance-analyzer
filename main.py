import os
import json
import csv
import numpy as np

# ==========================================
# CREATE MAIN SCHOOL DATA FOLDER
# ==========================================

os.makedirs("school_data", exist_ok=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def normalize_class_name(class_name):

    return class_name.strip().replace(" ", "").upper()


def create_class_folder(class_name):

    folder_name = f"class_{class_name}"

    folder_path = os.path.join("school_data", folder_name)

    os.makedirs(folder_path, exist_ok=True)

    return folder_path


def get_paths(folder_path):

    config_path = os.path.join(folder_path, "config.json")

    csv_path = os.path.join(folder_path, "students.csv")

    return config_path, csv_path


def load_config(config_path):

    try:

        with open(config_path, "r") as file:

            return json.load(file)

    except:

        return None


def save_config(config_path, config):

    with open(config_path, "w") as file:

        json.dump(config, file, indent=4)


def create_csv_if_not_exists(csv_path, subjects):

    if not os.path.exists(csv_path):

        header = ["ROLL", "NAME"] + subjects

        with open(csv_path, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow(header)


def load_students(csv_path):

    students = []

    if not os.path.exists(csv_path):

        return students

    with open(csv_path, "r") as file:

        reader = csv.reader(file)

        next(reader)

        for row in reader:

            students.append(row)

    return students


def get_marks_array(students):

    marks_data = []

    for row in students:

        marks = list(map(int, row[2:]))

        marks_data.append(marks)

    return np.array(marks_data)


def student_exists(students, roll):

    for row in students:

        if row[0] == roll:

            return True

    return False


def grade_generator(avg):

    if avg >= 90:
        return "A"

    elif avg >= 75:
        return "B"

    elif avg >= 60:
        return "C"

    elif avg >= 40:
        return "D"

    else:
        return "F"


# ==========================================
# CLASS ANALYTICS MENU
# ==========================================

def class_menu(class_name, config, csv_path):

    while True:

        print("\n====================================")
        print(f"CLASS : {class_name}")
        print("====================================")

        print("1. Add Student")
        print("2. View All Students")
        print("3. Student-wise Average")
        print("4. Subject-wise Average")
        print("5. Topper Detection")
        print("6. Lowest Performer")
        print("7. Pass / Fail System")
        print("8. Grade Generator")
        print("9. Report Card Generator")
        print("10. Search Student")
        print("11. Back")

        choice = input("\nEnter choice: ")

        # ==========================================
        # LOAD STUDENTS
        # ==========================================

        students = load_students(csv_path)

        # ==========================================
        # 1. ADD STUDENT
        # ==========================================

        if choice == "1":

            print("\n===== ADD STUDENT =====")

            while True:

                roll = input("Enter Roll Number: ").strip()

                if roll == "":

                    print("Roll number cannot be empty!")

                elif student_exists(students, roll):

                    print("Roll number already exists!")

                else:
                    break

            while True:

                name = input("Enter Student Name: ").strip().title()

                if name == "":

                    print("Name cannot be empty!")

                else:
                    break

            marks = []

            for subject in config["subjects"]:

                while True:

                    try:

                        mark = int(input(f"Enter {subject} marks: "))

                        if 0 <= mark <= 100:

                            marks.append(mark)
                            break

                        else:

                            print("Marks must be between 0 and 100!")

                    except:

                        print("Please enter valid integer marks!")

            student_data = [roll, name] + marks

            with open(csv_path, "a", newline="") as file:

                writer = csv.writer(file)

                writer.writerow(student_data)

            print("\nStudent added successfully!")

        # ==========================================
        # 2. VIEW ALL STUDENTS
        # ==========================================

        elif choice == "2":

            if len(students) == 0:

                print("\nNo students found!")

            else:

                print("\n===== ALL STUDENTS =====\n")

                for row in students:

                    print(row)

        # ==========================================
        # 3. STUDENT-WISE AVERAGE
        # ==========================================

        elif choice == "3":

            if len(students) == 0:

                print("\nNo students found!")

            else:

                marks_array = get_marks_array(students)

                averages = np.mean(marks_array, axis=1)

                print("\n===== STUDENT AVERAGES =====\n")

                for i in range(len(students)):

                    print(f"{students[i][1]} : {averages[i]:.2f}")

        # ==========================================
        # 4. SUBJECT-WISE AVERAGE
        # ==========================================

        elif choice == "4":

            if len(students) == 0:

                print("\nNo students found!")

            else:

                marks_array = get_marks_array(students)

                subject_avg = np.mean(marks_array, axis=0)

                print("\n===== SUBJECT AVERAGES =====\n")

                for i in range(len(config["subjects"])):

                    print(f"{config['subjects'][i]} : {subject_avg[i]:.2f}")

        # ==========================================
        # 5. TOPPER DETECTION
        # ==========================================

        elif choice == "5":

            if len(students) == 0:

                print("\nNo students found!")

            else:

                marks_array = get_marks_array(students)

                averages = np.mean(marks_array, axis=1)

                topper_index = np.argmax(averages)

                print("\n===== TOPPER =====\n")

                print(f"Name : {students[topper_index][1]}")
                print(f"Roll : {students[topper_index][0]}")
                print(f"Average : {averages[topper_index]:.2f}")

        # ==========================================
        # 6. LOWEST PERFORMER
        # ==========================================

        elif choice == "6":

            if len(students) == 0:

                print("\nNo students found!")

            else:

                marks_array = get_marks_array(students)

                averages = np.mean(marks_array, axis=1)

                low_index = np.argmin(averages)

                print("\n===== LOWEST PERFORMER =====\n")

                print(f"Name : {students[low_index][1]}")
                print(f"Roll : {students[low_index][0]}")
                print(f"Average : {averages[low_index]:.2f}")

        # ==========================================
        # 7. PASS / FAIL
        # ==========================================

        elif choice == "7":

            if len(students) == 0:

                print("\nNo students found!")

            else:

                marks_array = get_marks_array(students)

                print("\n===== PASS / FAIL =====\n")

                for i in range(len(students)):

                    if np.all(marks_array[i] >= 40):

                        status = "PASS"

                    else:

                        status = "FAIL"

                    print(f"{students[i][1]} : {status}")

        # ==========================================
        # 8. GRADE GENERATOR
        # ==========================================

        elif choice == "8":

            if len(students) == 0:

                print("\nNo students found!")

            else:

                marks_array = get_marks_array(students)

                averages = np.mean(marks_array, axis=1)

                print("\n===== GRADES =====\n")

                for i in range(len(students)):

                    grade = grade_generator(averages[i])

                    print(f"{students[i][1]} : {grade}")

        # ==========================================
        # 9. REPORT CARD
        # ==========================================

        elif choice == "9":

            if len(students) == 0:

                print("\nNo students found!")

            else:

                roll_search = input("Enter Roll Number: ").strip()

                found = False

                for row in students:

                    if row[0] == roll_search:

                        found = True

                        marks = list(map(int, row[2:]))

                        marks_array = np.array(marks)

                        average = np.mean(marks_array)

                        print("\n================================")
                        print("REPORT CARD")
                        print("================================")

                        print(f"Name : {row[1]}")
                        print(f"Roll : {row[0]}")
                        print(f"Class : {class_name}")

                        print()

                        for i in range(len(config["subjects"])):

                            print(f"{config['subjects'][i]} : {marks[i]}")

                        print(f"\nAverage : {average:.2f}")

                        grade = grade_generator(average)

                        print(f"Grade : {grade}")

                        if np.all(marks_array >= 40):

                            print("Status : PASS")

                        else:

                            print("Status : FAIL")

                if not found:

                    print("\nRoll number not found!")

        # ==========================================
        # 10. SEARCH STUDENT
        # ==========================================

        elif choice == "10":

            roll_search = input("Enter Roll Number: ").strip()

            found = False

            for row in students:

                if row[0] == roll_search:

                    found = True

                    print("\nStudent Found:\n")

                    print(row)

            if not found:

                print("\nStudent not found!")

        # ==========================================
        # 11. BACK
        # ==========================================

        elif choice == "11":

            break

        else:

            print("\nInvalid choice!")


# ==========================================
# IMPORT FULL CSV SYSTEM
# ==========================================

def import_full_csv():

    print("\nEnter FULL CSV path")
    print("Example:")
    print("C:/Users/risha/Downloads/students.csv")

    import_path = input("\nCSV Path: ").strip()

    if not os.path.exists(import_path):

        print("\nFile does not exist!")

        return

    try:

        with open(import_path, "r") as file:

            reader = csv.reader(file)

            header = next(reader)

            # Required first columns
            required = ["CLASS", "ROLL", "NAME"]

            if header[:3] != required:

                print("\nCSV format invalid!")
                print("First columns must be:")
                print(required)

                return

            subjects = header[3:]

            rows = list(reader)

            if len(rows) == 0:

                print("\nCSV file empty!")

                return

            class_name = normalize_class_name(rows[0][0])

            folder_path = create_class_folder(class_name)

            config_path, csv_path = get_paths(folder_path)

            config = {
                "class": class_name,
                "subjects": subjects
            }

            save_config(config_path, config)

            create_csv_if_not_exists(csv_path, subjects)

            existing_students = load_students(csv_path)

            imported_count = 0
            skipped_count = 0

            with open(csv_path, "a", newline="") as main_file:

                writer = csv.writer(main_file)

                for row in rows:

                    try:

                        roll = row[1]

                        name = row[2].strip().title()

                        marks = list(map(int, row[3:]))

                        if student_exists(existing_students, roll):

                            skipped_count += 1
                            continue

                        valid = True

                        for mark in marks:

                            if mark < 0 or mark > 100:

                                valid = False
                                break

                        if valid:

                            final_row = [roll, name] + marks

                            writer.writerow(final_row)

                            imported_count += 1

                        else:

                            skipped_count += 1

                    except:

                        skipped_count += 1

            print(f"\nClass {class_name} created successfully!")
            print(f"{imported_count} students imported!")
            print(f"{skipped_count} invalid rows skipped!")

    except Exception as e:

        print("\nError importing CSV!")
        print(e)


# ==========================================
# OPEN EXISTING CLASS
# ==========================================

def open_existing_class():

    folders = os.listdir("school_data")

    if len(folders) == 0:

        print("\nNo classes found!")

        return

    print("\n===== AVAILABLE CLASSES =====\n")

    for i, folder in enumerate(folders):

        print(f"{i+1}. {folder}")

    try:

        choice = int(input("\nSelect class number: "))

        selected_folder = folders[choice - 1]

        folder_path = os.path.join("school_data", selected_folder)

        config_path, csv_path = get_paths(folder_path)

        config = load_config(config_path)

        class_name = config["class"]

        class_menu(class_name, config, csv_path)

    except:

        print("\nInvalid selection!")


# ==========================================
# CREATE / OPEN CLASS
# ==========================================

def create_or_open_class():

    class_name = input("Enter class name: ")

    class_name = normalize_class_name(class_name)

    folder_path = create_class_folder(class_name)

    config_path, csv_path = get_paths(folder_path)

    if not os.path.exists(config_path):

        print("\nNew class detected!")

        while True:

            try:

                num_subjects = int(input("How many subjects? "))

                if num_subjects > 0:

                    break

                else:

                    print("Minimum 1 subject required!")

            except:

                print("Enter valid number!")

        subjects = []

        for i in range(num_subjects):

            while True:

                subject = input(f"Enter subject {i+1}: ")

                subject = subject.strip().upper()

                if subject == "":

                    print("Subject cannot be empty!")

                elif subject in subjects:

                    print("Duplicate subject!")

                else:

                    subjects.append(subject)
                    break

        config = {
            "class": class_name,
            "subjects": subjects
        }

        save_config(config_path, config)

    else:

        config = load_config(config_path)

    create_csv_if_not_exists(csv_path, config["subjects"])

    class_menu(class_name, config, csv_path)


# ==========================================
# MAIN SYSTEM MENU
# ==========================================

while True:

    print("\n====================================")
    print("STUDENT MARKS ANALYTICS SYSTEM")
    print("====================================")

    print("1. Create / Open Class")
    print("2. Import Full Student CSV")
    print("3. Open Existing Class")
    print("4. Exit")

    main_choice = input("\nEnter choice: ")

    # ==========================================
    # CREATE / OPEN CLASS
    # ==========================================

    if main_choice == "1":

        create_or_open_class()

    # ==========================================
    # IMPORT FULL CSV
    # ==========================================

    elif main_choice == "2":

        import_full_csv()

    # ==========================================
    # OPEN EXISTING CLASS
    # ==========================================

    elif main_choice == "3":

        open_existing_class()

    # ==========================================
    # EXIT
    # ==========================================

    elif main_choice == "4":

        print("\nExiting program...")
        break

    else:

        print("\nInvalid choice!")