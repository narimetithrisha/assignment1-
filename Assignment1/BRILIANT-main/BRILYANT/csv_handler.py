import csv

def read_csv(file_path):
    students = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append({
                'name': row['name'],
                'age': int(row['age']),
                'grade': float(row['grade']),
            })
    return students

def calculate_average_grade(students):
    if not students:
        return 0
    total_grades = sum(student['grade'] for student in students)
    return total_grades / len(students)

def find_highest_grade_student(students):
    if not students:
        return None
    return max(students, key=lambda student: student['grade'])

if __name__ == '__main__':
    file_path = 'student.csv'  # Specify your CSV file path
    students = read_csv(file_path)
    average_grade = calculate_average_grade(students)
    highest_student = find_highest_grade_student(students)

    print(f'Average Grade: {average_grade}')
    if highest_student:
        print(f'Student with Highest Grade: {highest_student["name"]} ({highest_student["grade"]})')
