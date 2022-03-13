class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        self.student_bio = f'''Имя: {self.name} \nФамилия: {self.surname}
Средняя оценка за домашние задания: {None}
Курсы в процессе изучения: {None}
Завершенные курсы: {None}'''
        return self.student_bio

studen1 = Student("John", "Ort", "male")
print(studen1)
        
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
        
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        mentor_bio = f'Имя: {self.name} \nФамилия: {self.surname}'
        return mentor_bio

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.student_grades = {}
    
    def __str__(self):
        average_grade = 0
        lecturer_bio = f'Имя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за лекции: {average_grade}'
        return lecturer_bio 

class Reviewer(Mentor):
    
    def __str__(self):
        reviewer_bio = f'Имя: {self.name} \nФамилия: {self.surname}'
        return reviewer_bio 

lecturer1 = Lecturer('Иван', 'Иванов')
print(lecturer1)

reviewer1 = Reviewer('Петр', 'Петров')
print(reviewer1)


 
best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
 
cool_mentor = Mentor('Some', 'Buddy')
cool_mentor.courses_attached += ['Python']
 
cool_mentor.rate_hw(best_student, 'Python', 10)
cool_mentor.rate_hw(best_student, 'Python', 10)
cool_mentor.rate_hw(best_student, 'Python', 10)
 
print(best_student.grades)