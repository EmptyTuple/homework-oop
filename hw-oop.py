from statistics import mean

# Создаем переменные для хранения списков студентов, преподавателей  и ревьюверов
students_list = []
lecturers_list = []
reviewers_list = []

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        students_list.append(self)

    def rate_lecturer(self, lecturer, course, grade):
        # Создаем функцию для выставления оценок лекторам
        # Не делал проверки значения оценок, предположив, что как и на сайте Нетологии,
        # значения оценок будут считываться как количество звездочек, поставленных студентом.
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and \
                      course in lecturer.courses_attached:
            if course not in lecturer.student_grades:
                lecturer.student_grades[course] = [grade]
            else:
                lecturer.student_grades[course] += [grade]
        else:
            print('Ошибка, проверьте входные данные!')

    def calc_avg_grade_student(self):
        # Создаем функцию, считающую среднее значение оценок студента
        # Предполагаем, что студент может обучаться на нескольких курсах - оценки по разным предметам даем отдельно.
        if len(self.grades) != 0:
            summary_grades = ''
            for course, rate in sorted(self.grades.items(), key=lambda x:mean(x[1])):
                summary_grades += f'{course}: {mean(rate)}  '
            return summary_grades
        else:
            return 'Оценок пока нет'
    
    def __lt__(self, other):    
        # Реализуем функцию сравнения студентов по средней оценке за лекции
        # Объединим оценки за все курсы и посчитаем общее среднее.
        if isinstance(other, Student) and isinstance(self, Student):
            self.avg_self = mean(sum(self.grades.values(), []))
            self.avg_other = mean(sum(other.grades.values(), []))
            return self.avg_self < self.avg_other
        else:
            return "Ошибка"
        
    def __str__(self):
        self.student_bio = f'''Имя: {self.name} \nФамилия: {self.surname}
Средняя оценка за домашние задания: {self.calc_avg_grade_student()}
Курсы в процессе изучения: {', '.join(map(str, self.courses_in_progress))}
Завершенные курсы: {', '.join(map(str, self.finished_courses))}'''
        return self.student_bio
      
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        mentor_bio = f'Имя: {self.name} \nФамилия: {self.surname}'
        return mentor_bio

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.student_grades = {}
        lecturers_list.append(self)
    
    def calc_avg_grade(self):
        # Создаем функцию, считающую среднее значение оценок студентов.
        # Предполагаем, что лектор может вести разные предметы - оценки студентов по разным предметам даем отдельно.
        if len(self.student_grades) != 0:
            summary_grades = ''
            for course, rate in sorted(self.student_grades.items(), key=lambda x:mean(x[1])):
                summary_grades += f'{course}: {mean(rate)}  '
            return summary_grades
        else:
            return 'Оценок пока нет'
        
    def __lt__(self, other):    
        # Реализуем функцию сравнения лекторов по средней оценке за лекции.
        # Исходим из логики что лектор может вести разные предметы, вычисляем среднее по все предметам.
        if isinstance(other, Lecturer) and isinstance(self, Lecturer):
            self.avg_self_lector = mean(sum(self.student_grades.values(), []))
            self.avg_other_lector = mean(sum(other.student_grades.values(), []))
            return self.avg_self_lector < self.avg_other_lector
        else:
            return "Ошибка"
  
    def __str__(self):
        lecturer_bio = f'Имя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за лекции: {self.calc_avg_grade()}'
        return lecturer_bio 

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        reviewers_list.append(self)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print('Ошибка')
    
    def __str__(self):
        reviewer_bio = f'Имя: {self.name} \nФамилия: {self.surname}'
        return reviewer_bio


lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Дорофей', 'Дорофеев')
reviewer1 = Reviewer('Петр', 'Петров')
reviewer2 = Reviewer('Сидор', 'Сидоров')
studen1 = Student("John", "Ort", "male")
studen2 = Student("John", "Smith", "male")

lecturer1.courses_attached += ['Python']
lecturer1.courses_attached += ['SQL']
lecturer2.courses_attached += ['Python']
lecturer2.courses_attached += ['SQL']

studen1.courses_in_progress += ['Python']
studen1.courses_in_progress += ['SQL']
studen1.finished_courses += ['Java']

studen2.courses_in_progress += ['Python']
studen2.courses_in_progress += ['SQL']
studen2.finished_courses += ['Java']

studen1.rate_lecturer(lecturer1, 'Python', 4)
studen1.rate_lecturer(lecturer1, 'Python', 7)
studen1.rate_lecturer(lecturer1, 'SQL', 5)
studen1.rate_lecturer(lecturer1, 'SQL', 7)

studen2.rate_lecturer(lecturer1, 'Python', 5)
studen2.rate_lecturer(lecturer1, 'Python', 8)
studen2.rate_lecturer(lecturer1, 'SQL', 6)
studen2.rate_lecturer(lecturer1, 'SQL', 8)

studen1.rate_lecturer(lecturer2, 'Python', 2)
studen1.rate_lecturer(lecturer2, 'Python', 3)
studen1.rate_lecturer(lecturer2, 'SQL', 5)
studen1.rate_lecturer(lecturer2, 'SQL', 4)

reviewer1.courses_attached += ['Python']
reviewer1.rate_hw(studen1, 'Python', 5)
reviewer1.rate_hw(studen1, 'Python', 3)

reviewer2.courses_attached += ['SQL']
reviewer2.rate_hw(studen1, 'SQL', 6)
reviewer2.rate_hw(studen1, 'SQL', 5)

reviewer1.rate_hw(studen2, 'Python', 7)
reviewer1.rate_hw(studen2, 'Python', 5)

reviewer2.rate_hw(studen2, 'SQL', 6)
reviewer2.rate_hw(studen2, 'SQL', 11)

# print(studen1.grades)
# print(lecturer1)
# print(lecturer1.courses_attached)
# print(reviewer1)

print(studen1)
print(studen2)
print(studen1 < studen2)

print(lecturer1)
print(lecturer2)
print(lecturer1 > lecturer2)



 
# best_student = Student('Ruoy', 'Eman', 'your_gender')
# best_student.courses_in_progress += ['Python']
# best_student.courses_in_progress += ['SQL']
 
# cool_mentor = Mentor('Some', 'Buddy')
# cool_mentor.courses_attached += ['Python']
# cool_mentor.courses_attached += ['SQL']

# print(cool_mentor.courses_attached)
 
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 50)
# cool_mentor.rate_hw(best_student, 'SQL', 10)
# cool_mentor.rate_hw(best_student, 'SQL', 30)

# print(best_student.grades)