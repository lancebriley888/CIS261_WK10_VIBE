#Lance Briley
#CIS261
#WK10 VIBE Coding

"""Student Grade Calculator.

Option B: student records are represented with a Student class.
"""

from dataclasses import dataclass
from pathlib import Path


FILE_NAME = "student_grades.txt"


@dataclass
class Student:
	"""Store one student's scores and calculated results."""

	name: str
	student_id: str
	test1: float
	test2: float
	test3: float

	@property
	def average(self):
		return (self.test1 + self.test2 + self.test3) / 3

	@property
	def grade(self):
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	def to_file_line(self):
		return (
			f"{self.name}|{self.student_id}|{self.test1:.2f}|"
			f"{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}\n"
		)


def save_students(students):
	"""Save all student records using the required pipe-delimited format."""
	try:
		with open(FILE_NAME, "w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line())
		print(f"Student records saved to {FILE_NAME}.")
		return True
	except OSError as error:
		print(f"Error saving student records: {error}")
		return False


def load_students():
	"""Load valid student records, reporting file and data errors clearly."""
	students = []
	file_path = Path(FILE_NAME)
	if not file_path.exists():
		return students

	try:
		with open(file_path, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				if not line.strip():
					continue
				try:
					fields = line.rstrip("\n").split("|")
					if len(fields) != 7:
						raise ValueError("expected 7 pipe-delimited fields")
					name, student_id, test1, test2, test3, average, grade = fields
					student = Student(name, student_id, float(test1), float(test2), float(test3))
					if abs(student.average - float(average)) > 0.01 or student.grade != grade:
						raise ValueError("calculated average or grade does not match")
					students.append(student)
				except (ValueError, TypeError) as error:
					print(f"Skipping invalid record on line {line_number}: {error}")
	except OSError as error:
		print(f"Error loading student records: {error}")
	return students


def get_score(test_number):
	"""Prompt until a test score from 0 through 100 is entered."""
	while True:
		try:
			score = float(input(f"Enter Test {test_number} score (0-100): "))
			if 0 <= score <= 100:
				return score
			print("Score must be between 0 and 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	print("\nAdd Student")
	name = input("Enter student name: ").strip()
	student_id = input("Enter student ID: ").strip()
	if not name or not student_id:
		print("Name and student ID cannot be blank.")
		return
	scores = [get_score(number) for number in range(1, 4)]
	students.append(Student(name, student_id, *scores))
	print(f"Student added. Average: {students[-1].average:.2f}, Grade: {students[-1].grade}")


def display_students(students):
	if not students:
		print("No student records found.")
		return
	print("\nStudent Records")
	print("-" * 92)
	print(f"{'Name':<22}{'ID':<14}{'Test 1':>10}{'Test 2':>10}{'Test 3':>10}{'Average':>12}{'Grade':>8}")
	print("-" * 92)
	for student in students:
		print(
			f"{student.name:<22.22}{student.student_id:<14.14}"
			f"{student.test1:>10.2f}{student.test2:>10.2f}{student.test3:>10.2f}"
			f"{student.average:>12.2f}{student.grade:>8}"
		)
	print("-" * 92)


def display_statistics(students):
	if not students:
		print("No student records found.")
		return
	averages = [student.average for student in students]
	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	print("\nClass Statistics")
	print(f"Highest average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest average:  {lowest.average:.2f} ({lowest.name})")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_student(students):
	search_name = input("Enter the student name to search for: ").strip().casefold()
	matches = [student for student in students if search_name in student.name.casefold()]
	if matches:
		display_students(matches)
	else:
		print("No matching student found.")


def main():
	students = load_students()
	if students:
		print(f"Loaded {len(students)} student record(s) from {FILE_NAME}.")

	while True:
		print("\nStudent Grade Calculator")
		print("1. Add student")
		print("2. Display all students")
		print("3. Display class statistics")
		print("4. Search for a student")
		print("Type ESC to save and exit.")
		choice = input("Choose an option: ").strip()

		if choice.upper() == "ESC" or "\x1b" in choice:
			save_students(students)
			print("Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		else:
			print("Invalid option. Please choose 1-4 or type ESC.")


if __name__ == "__main__":
	main()