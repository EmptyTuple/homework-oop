from statistics import mean

# Создаем переменные для хранения списков студентов и преподавателей
students_list = []
lecturers_list = []

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
                summary_grades += f'{course}: {round(mean(rate), 2)}  '
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
        lecturers_list.append(f'{self.name} {self.surname}')
    
    def calc_avg_grade(self):
        # Создаем функцию, считающую среднее значение оценок студентов.
        # Предполагаем, что лектор может вести разные предметы - оценки студентов по разным предметам даем отдельно.
        if len(self.student_grades) != 0:
            summary_grades = ''
            for course, rate in sorted(self.student_grades.items(), key=lambda x:mean(x[1])):
                summary_grades += f'{course}: {round(mean(rate), 2)}  '
            return summary_grades
        else:
            return 'Оценок пока нет'
        
    def __lt__(self, other):    
        # Реализуем функцию сравнения лекторов по средней оценке за лекции.
        # Исходим из логики что лектор может вести разные предметы, вычисляем среднее как по предметам, так и общую.
        if isinstance(other, Lecturer) and isinstance(self, Lecturer):
            self.avg_self_lector = mean(sum(self.student_grades.values(), []))
            self.avg_other_lector = mean(sum(other.student_grades.values(), []))
            return self.avg_self_lector < self.avg_other_lector
        else:
            return "Ошибка"
  
    def __str__(self):
        lecturer_bio = f'Имя: {self.name} \nФамилия: {self.surname} \
            \nСредняя оценка за лекции по курсам: {self.calc_avg_grade()} \
            \nОбщая средняя оценка: {mean(sum(self.student_grades.values(), []))}'
        return lecturer_bio 

class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

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

# Определяем функции для подсчета средних оценок внутри курсов:


def get_avg_lectures(lecturers_list, course):
    grades_sum = 0
    lecturers_count = 0
    for lecturer in lecturers_list:
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached:
            grades_sum += lecturer.student_grades()
            lecturers_count += 1
    # if lecturers_count == 0:
    #     return 'Ошибка'
    return round(grades_sum / lecturers_count, 2)



# Полевые испытания

student_001 = Student("Алексей", "Алексеев", "male")
student_002 = Student("Сергей", "Сергеев", "male")

lecturer_001 = Lecturer('Иван', 'Иванов')
lecturer_002 = Lecturer('Дорофей', 'Дорофеев')

reviewer_001 = Reviewer('Петр', 'Петров')
reviewer_002 = Reviewer('Сидор', 'Сидоров')

student_001.courses_in_progress += ['Python']
student_001.courses_in_progress += ['SQL']
student_001.finished_courses += ['Java']

student_002.courses_in_progress += ['Python']
student_002.courses_in_progress += ['C++']
student_002.finished_courses += ['Java']

lecturer_001.courses_attached += ['Python']
lecturer_001.courses_attached += ['SQL']
lecturer_002.courses_attached += ['Python']
lecturer_002.courses_attached += ['C++']

student_001.rate_lecturer(lecturer_001, 'Python', 4)
student_001.rate_lecturer(lecturer_002, 'Python', 5)
student_001.rate_lecturer(lecturer_001, 'SQL', 5)
student_001.rate_lecturer(lecturer_001, 'SQL', 3)

student_002.rate_lecturer(lecturer_001, 'Python', 3)
student_002.rate_lecturer(lecturer_002, 'Python', 2)
student_002.rate_lecturer(lecturer_002, 'C++', 4)
student_002.rate_lecturer(lecturer_002, 'C++', 5)
student_002.rate_lecturer(lecturer_002, 'C++', 2)

reviewer_001.courses_attached += ['Python']
reviewer_001.courses_attached += ['SQL']
reviewer_002.courses_attached += ['C++']

reviewer_001.rate_hw(student_001, 'Python', 5)
reviewer_001.rate_hw(student_001, 'Python', 3)
reviewer_001.rate_hw(student_001, 'Python', 5)
reviewer_001.rate_hw(student_001, 'SQL', 2)
reviewer_001.rate_hw(student_001, 'SQL', 3)
reviewer_001.rate_hw(student_002, 'Python', 4)
reviewer_001.rate_hw(student_002, 'Python', 1)
reviewer_001.rate_hw(student_002, 'Python', 3)
reviewer_002.rate_hw(student_002, 'C++', 4)
reviewer_002.rate_hw(student_002, 'C++', 5)

# Печатаем отчеты:

# print(student_001)
# print()
# print(student_002)
# print()
# print(student_001 < student_002)
# print()

# print(reviewer_001)
# print()
# print(reviewer_002)
# print()

# print(lecturer_001)
# print()
# print(lecturer_002)
# print()
# print(lecturer_001 < lecturer_002)
# print()
print(*lecturers_list)
print(len(lecturers_list))
# get_avg_lectures(lecturers_list, 'Python')