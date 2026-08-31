class Book:

    book_count = 0

    def __init__(self, title: str, author: str, pages: int):
        self.title = title
        self.author = author
        self.pages = pages

        Book.book_count += 1

    #self is initial because it refers to the origin obj in Book class
    def description(self):
        print(
            f"{self.title} is written by "
            f"{self.author} in {self.pages} pages."
        )
    """def is_long(self):
        if self.pages > 500:
            return True
        else:
            return False"""

    def is_long(self):
        return self.pages > 500


####
class Classroom:
    def __init__(self, teacher: str, students: list, subject: str, room_number: int):
        self.teacher = teacher
        self.students = students
        self.subject = subject
        self.room_number = room_number
    def display_info(self):
        print(f"Teacher : {self.teacher}")
        print(f"Students : {self.students}")
        print(f"Subject : {self.subject}")
        print(f"Room_number : {self.room_number}")


my_class = Classroom(
    teacher = 'Miss Nemati',
    students = ['Neda' , 'Sara', 'Mona', 'Kiana'],
    subject = 'English',
    room_number = 6
)

my_class.display_info()


#####
class ClassroomWithDynamicStudents:
    def __init__(self, teacher: str, *students: str, subject: str, room_number: int):
        self.teacher = teacher
        self.students = students
        self.subject = subject
        self.room_number = room_number
    def display_info(self):
        print(f"Teacher : {self.teacher}")
        print(f"Students : {self.students}")
        print(f"Subject : {self.subject}")
        print(f"Room_number : {self.room_number}")

bonus_class = ClassroomWithDynamicStudents(
    'Mr. Johnson',
    'Neda', 'Sara', 'Mona', 'Kiana',
    subject = 'Science',
    room_number = 5
)

bonus_class.display_info()