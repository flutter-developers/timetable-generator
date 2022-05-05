from ttg import db, login_manager

class Professor(db.Model):
    __table_args__ = {'extend_existing': True}
    professor_id = db.Column(db.String(20),primary_key=True)
    professor_name = db.Column(db.String(50),unique=True,nullable=False)
    department = db.Column(db.String(7),nullable=False)


class Course(db.Model):
    __table_args__ = {'extend_existing': True}
    course_id = db.Column(db.String(20),primary_key=True)
    course_name = db.Column(db.String(50),unique=True,nullable=False)
    course_short_form = db.Column(db.String(10),unique=True,nullable=False)
    course_type = db.Column(db.String(10),nullable=False)
    duration = db.Column(db.Integer,nullable=True)
    frequency = db.Column(db.Integer,nullable=True)
    preferred_rooms = db.Column(db.String(20),nullable=True)   

    def __repr__(self):
        return str(self.course_short_form)


class Batch:
    def __init__(self, branch, year, section, batch_room, is_jnr):
        self.branch = branch
        self.year = year
        self.section = section
        self.batch_room = batch_room
        self.non_empty_slots = 0
        self.is_jnr = is_jnr

    def __repr__(self):
        return str(self.year) + "-" + str(self.section)


# TODO: Create [Room & Branch] Class According to USE CASE

class Data:

    def __new__(cls, *args, **kwargs):
        temp = object.__new__(cls)
        return temp

    def __init__(self):
        self.batch = None
        self.course = None
        self.faculty = None
        self.slots = None
        self.room = []
        self.batch_check = None
        self.faculty_check = None
        self.room_check = None
        self.duration = None
        self.frequency = None
        self.can_change_time = None
        self.can_change_day = None
        self.is_pseudo = False
        self.is_compound = False
        self.is_lab = False
        self.is_jnr = None

    def create_lecture_data(self, batch, course, faculty):
        self.batch = batch
        self.course = course
        self.faculty = faculty

        # Initiation
        self.room = list(batch)[0].batch_room
        self.duration = list(course)[0].duration
        self.frequency = list(course)[0].frequency
        self.batch_check = True
        self.room_check = False
        self.faculty_check = True
        self.can_change_day = True
        self.can_change_time = True
        self.is_jnr = list(batch)[0].is_jnr

        # Misc
        for b in batch:
            b.non_empty_slots += self.duration * self.frequency

        return self

    def create_lab_data(self, batch, course, faculty, duration, frequency):
        self.batch = batch
        self.course = course
        self.faculty = faculty

        # Initiation
        # self.room = []
        # for _ in course:
        #     self.room.append(list(_.preferred_rooms))
        self.duration = duration
        self.frequency = frequency
        self.batch_check = True
        self.room_check = True
        self.faculty_check = True
        self.can_change_day = True
        self.can_change_time = True
        self.is_lab = True
        self.is_jnr = list(batch)[0].is_jnr

        # Misc
        for b in batch:
            b.non_empty_slots += self.duration * self.frequency

        return self

    def create_compound_data(self, batch, course):
        self.batch = batch
        self.course = course

        # Initiation
        self.duration = list(course)[0].duration
        self.frequency = list(course)[0].frequency
        self.batch_check = True
        self.room_check = False
        self.faculty_check = False
        self.can_change_day = True
        self.can_change_time = True
        self.is_compound = True
        self.is_jnr = list(batch)[0].is_jnr

        # Misc
        for b in batch:
            b.non_empty_slots += self.duration * self.frequency

        return self

    def create_pseudo_data(self, batch, duration, frequency):
        self.batch = batch

        # Initiation
        self.duration = duration
        self.frequency = frequency
        self.room = list(batch)[0].batch_room
        self.batch_check = True
        self.room_check = False
        self.faculty_check = False
        self.can_change_day = True
        self.can_change_time = False
        self.is_pseudo = True
        self.is_jnr = list(batch)[0].is_jnr

        return self
