from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship

from .orm import get_base


Base = get_base()


class Faculty(Base):
    """
    Модель "Факультет"
    """

    __tablename__ = 'univer_faculty'

    id = Column('faculty_id', Integer, primary_key=True)
    status = Column(Integer)
    name_kz = Column('faculty_name_kz', String(200))
    name_ru = Column('faculty_name_ru', String(200))
    name_en = Column('faculty_name_en', String(200))

    def __repr__(self):
        return "<Faculty {}>".format(self)
    
    def __str__(self):
        return self.name_ru


class Stage(Base):
    """
    Модель "Уровень"
    """

    __tablename__ = 'univer_stage'

    id = Column('stage_id', Integer, primary_key=True)
    status = Column(Integer)
    name_kz = Column('stage_name_kz', String(200))
    name_ru = Column('stage_name_ru', String(200))
    name_en = Column('stage_name_en', String(200))

    def __repr__(self):
        return "<Stage {}>".format(self)
    
    def __str__(self):
        return self.name_ru


class EducationForm(Base):
    """
    Модель "Форма обучения"
    """

    __tablename__ = 'univer_education_form'

    id = Column('education_form_id', Integer, primary_key=True)
    status = Column(Integer)
    name_kz = Column('education_form_name_kz', String(200))
    name_ru = Column('education_form_name_ru', String(200))
    name_en = Column('education_form_name_en', String(200))

    def __repr__(self):
        return "<EducationForm {}>".format(self)

    def __str__(self):
        return self.name_ru


class Speciality(Base):
    """
    Модель "Специальность"
    """

    __tablename__ = 'univer_speciality'

    id = Column('speciality_id', Integer, primary_key=True)
    status = Column(Integer)
    faculty_id = Column(ForeignKey('univer_faculty.faculty_id'))
    faculty = relationship('Faculty')
    stage_id = Column(ForeignKey('univer_stage.stage_id'))
    stage = relationship('Stage')
    name_kz = Column('speciality_name_kz', String(200))
    name_ru = Column('speciality_name_ru', String(200))
    name_en = Column('speciality_name_en', String(200))
    code = Column('speciality_okpd', String(10))
    description_kz = Column('speciality_discription_kz', String)
    description_ru = Column('speciality_discription_ru', String)
    description_en = Column('speciality_discription_en', String)
    result_ru = Column(String)
    result_kz = Column(String)
    result_en = Column(String)
    type = Column(Integer)

    def __repr__(self):
        return "<Speciality {}>".format(self)
    
    def __str__(self):
        return "{} - {}".format(self.code, self.name_ru)


class StructureDivision(Base):
    """
    Модель "Подразделение"
    """

    __tablename__ = 'univer_structure_division_1c'

    id = Column('structure_division_id', Integer, primary_key=True)
    name_kz = Column('structure_division_name_kz', String(500))
    name_ru = Column('structure_division_name_ru', String(500))
    name_en = Column('structure_division_name_en', String(500))
    status = Column(Integer)

    def __repr__(self):
        return '<StructureDivision {}>'.format(self)
    
    def __str__(self):
        return self.name_ru


class PersonnelStructureDivisionLink(Base):
    """
    Модель "Ссылка персонала с подразделением"
    """

    __tablename__ = 'univer_personal_struct_pos_link_1c'

    id = Column('pers_struct_pos_link_id', Integer, primary_key=True)
    status = Column(Integer)
    personnel_id = Column('personal_id', ForeignKey('univer_personal.personal_id'))
    personnel = relationship('Personnel')
    structure_division_id = Column(ForeignKey('univer_structure_division_1c.structure_division_id'))
    structure_division = relationship('StructureDivision')

    def __repr__(self):
        return '<PersonnelStructureDivisionLink {}>'.format(self)
    
    def __str__(self):
        return '{} ({})'.format(personnel, structure_division)


class Chair(Base):
    """
    Модель "Кафедра"
    """

    __tablename__ = 'univer_chair'

    id = Column('chair_id', Integer, primary_key=True)
    status = Column(Integer)
    name_kz = Column('chair_name_kz', String(200))
    name_ru = Column('chair_name_ru', String(200))
    name_en = Column('chair_name_en', String(200))
    structure_division_id = Column(ForeignKey('univer_structure_division_1c.structure_division_id'))
    structure_division = relationship('StructureDivision')

    def __repr__(self):
        return '<Chair {}>'.format(self)
    
    def __str__(self):
        return self.name_ru


class SpecialityChair(Base):
    """
    Модель отношений "Специальность-Кафедра"
    """

    __tablename__ = 'univer_speciality_chair'

    speciality_id = Column(ForeignKey('univer_speciality.speciality_id'), primary_key=True)
    speciality = relationship('Speciality')
    chair_id = Column(ForeignKey('univer_chair.chair_id'), primary_key=True)
    chair = relationship('Chair')

    def __repr__(self):
        return '<SpecialityChair {}>'.format(self)
    
    def __str__(self):
        return '{} - {}'.format(self.chair, self.speciality)


class Subject(Base):
    """
    Модель "Дисциплина"
    """

    __tablename__ = 'univer_subject'

    id = Column('subject_id', Integer, primary_key=True)
    name_kz = Column('subject_name_kz', String(500))
    name_ru = Column('subject_name_ru', String(500))
    name_en = Column('subject_name_en', String(500))
    status = Column(Integer)

    def __repr__(self):
        return '<Subject {}>'.format(self.name_ru)
    
    def __str__(self):
        return self.name_ru


class EducType(Base):
    __tablename__ = 'univer_educ_type'

    id = Column('educ_type_id', Integer, primary_key=True)
    name_ru = Column('educ_type_name_ru', String(100))

    def __repr__(self):
        return '<EducType {}>'.format(self.name_ru)

    def __str__(self):
        return self.name_ru


class LangDivision(Base):
    """
    Модель "Языковый отдел"
    """

    __tablename__ = 'univer_lang_division'

    id = Column('lang_division_id', Integer, primary_key=True)
    name_ru = Column('lang_division_name_ru', String(100))

    def __repr__(self):
        return '<LangDivision {}>'.format(self.name_ru)
    
    def __str__(self):
        return self.name_ru


class User(Base):
    """
    Модель "Пользователь"
    """
    __tablename__ = 'univer_users'

    id = Column('user_id', Integer, primary_key=True)
    username = Column('user_login', String(50))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def __str__(self):
        return self.username


class Student(Base):
    """
    Модель "Студент"
    """
    __tablename__ = 'univer_students'

    id = Column('students_id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('univer_users.user_id'))
    user = relationship('User')
    status = Column('status', Integer)
    reg_date = Column('student_reg_date', DateTime)

    # ФИО студента
    last_name = Column('students_sname', String(100))
    first_name = Column('students_name', String(100))
    middle_name = Column('students_father_name', String(100))

    # Фамилия и Имя студента транслитом
    last_name_translit = Column('students_sname_intern', String(100))
    first_name_translit = Column('students_name_intern', String(100))

    email = Column('students_email', String(25))

    # ИИН студента
    identify_code = Column('students_identify_code', String(50))

    # Факультет
    faculty_id = Column(ForeignKey('univer_faculty.faculty_id'))
    faculty = relationship('Faculty')

    # ОП
    speciality_id = Column(ForeignKey('univer_speciality.speciality_id'))
    speciality = relationship('Speciality')

    # Год начала действия учебного плана
    educ_plan_adm_year = Column(Integer)

    education_form_id = Column(ForeignKey('univer_education_form.education_form_id'))
    education_form = relationship('EducationForm')

    def __repr__(self):
        return '<Student {}>'.format(self)
    
    def __str__(self):
        return ' '.join(filter(None, [self.last_name, self.first_name, self.middle_name]))


class Personnel(Base):
    """
    Модель "Сотрудник"
    """
    __tablename__ = 'univer_personal'

    id = Column('personal_id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('univer_users.user_id'))
    user = relationship('User')
    status = Column('status', Integer)

    # ФИО персонала
    last_name = Column('personal_sname', String(200))
    first_name = Column('personal_name', String(100))
    middle_name = Column('personal_father_name', String(100))

    # Фамилия и Имя персонала транслитом
    last_name_translit = Column('personal_translit_sname', String(100))
    first_name_translit = Column('personal_translit_name', String(100))

    work_email = Column('personal_work_email', String(50))
    identify_code = Column('personal_identification_number', String(150))

    def __repr__(self):
        full_name = ' '.join(filter(None, [self.last_name, self.first_name, self.middle_name]))

        return '<Personnel {}>'.format(full_name)
    
    def __str__(self):
        return ' '.join(filter(None, [self.last_name, self.first_name, self.middle_name]))


class Teacher(Base):
    """
    Модель "Преподаватель"
    """

    __tablename__ = 'univer_teacher'

    id = Column('teacher_id', Integer, primary_key=True)
    personnel_id = Column('personal_id', ForeignKey('univer_personal.personal_id'))
    personnel = relationship('Personnel')
    status = Column('status', Integer)

    def __repr__(self):
        return '<Teacher {}>'.format(self.personnel)
    
    def __str__(self):
        return str(self.personnel)


class AcademCalendar(Base):
    """
    Модель "Академический календарь"
    """

    __tablename__ = 'univer_academ_calendar_pos'

    id = Column('acpos_id', Integer, primary_key=True)
    educ_plan_id = Column(ForeignKey('univer_educ_plan.educ_plan_id'))
    educ_plan = relationship('EducPlan')
    acpos_semester = Column(Integer)
    acpos_module = Column(Integer)
    control_id = Column(ForeignKey('univer_control.control_id'))
    control = relationship('Control')
    acpos_weeks = Column(Integer)
    acpos_date_start = Column(DateTime)
    acpos_date_end = Column(DateTime)

    def __repr__(self):
        return '<AcademCalendar {}>'.format(self)
    
    def __str__(self):
        return '{}'.format(self.id)


class EducPlan(Base):
    """
    Модель "Учебный план"
    """

    __tablename__ = 'univer_educ_plan'

    id = Column('educ_plan_id', Integer, primary_key=True)
    speciality_id = Column('speciality_id', ForeignKey('univer_speciality.speciality_id'))
    speciality = relationship(Speciality)
    education_form_id = Column(ForeignKey('univer_education_form.education_form_id'))
    education_form = relationship('EducationForm')
    year = Column('educ_plan_adm_year', Integer)

    def __repr__(self):
        return "<EducPlan {} {}>".format(self.speciality, self.year)
    
    def __str__(self):
        return "{} {}".format(self.speciality, self.year)


class EducPlanPos(Base):
    """
    Модель "Позиции учебного плана"
    """

    __tablename__ = 'univer_educ_plan_pos'

    id = Column('educ_plan_pos_id', Integer, primary_key=True)
    educ_plan_id = Column('educ_plan_id', ForeignKey('univer_educ_plan.educ_plan_id'))
    educ_plan = relationship('EducPlan')
    subject_id = Column('subject_id', ForeignKey('univer_subject.subject_id'))
    subject = relationship(Subject)
    semester = Column('educ_plan_pos_semestr', Integer)

    def __repr__(self):
        return "<EducPlanPos {}: {} ({} семестр)>".format(self.educ_plan, self.subject, self.semester)
    
    def __str__(self):
        return "{}: {} ({} семестр)".format(self.educ_plan, self.subject, self.semester)


class Attendance(Base):
    """
    Модель "Журнал посещаемости"
    """

    __tablename__ = 'univer_attendance'

    date = Column('att_date', Date, primary_key=True)
    grade = Column('ball', Float)
    was = Column(Boolean)
    student_id = Column(ForeignKey('univer_students.students_id'), primary_key=True)
    student = relationship(Student)
    group_id = Column(ForeignKey('univer_group.group_id'), primary_key=True)
    group = relationship('Group')

    def __repr__(self):
        return '<Attendance {}: {} балл ({})>'.format(self.student, self.grade, self.date)
    
    def __str__(self):
        return '{}: {} балл ({})'.format(self.student, self.grade, self.date)


class Group(Base):
    """
    Модель "Группа"
    """

    __tablename__ = 'univer_group'

    id = Column('group_id', Integer, primary_key=True)
    educ_plan_pos_id = Column('educ_plan_pos_id', ForeignKey('univer_educ_plan_pos.educ_plan_pos_id'))
    educ_plan_pos = relationship(EducPlanPos, backref='groups')
    teacher_id = Column('teacher_id', ForeignKey('univer_teacher.teacher_id'))
    teacher = relationship(Teacher)
    year = Column('group_year', Float)
    semester = Column('group_semestr', Integer)
    educ_type_id = Column('educ_type_id', ForeignKey('univer_educ_type.educ_type_id'))
    educ_type = relationship(EducType)
    lang_division_id = Column('lang_division_id', ForeignKey('univer_lang_division.lang_division_id'))
    lang_division = relationship(LangDivision)

    def __repr__(self):
        return '<Group {}>'.format(self)
    
    def __str__(self):
        return '{} ({} год)'.format(self.educ_plan_pos.educ_plan.speciality, self.educ_plan_pos.educ_plan.year)


class GroupStudent(Base):
    """
    Модель "Студент в группе"
    """

    __tablename__ = 'univer_group_student'

    id = Column('group_student_id', Integer, primary_key=True)
    group_id = Column(ForeignKey('univer_group.group_id'))
    group = relationship(Group, backref='group_students')
    student_id = Column(ForeignKey('univer_students.students_id'))
    student = relationship(Student)


class Control(Base):
    """
    Модель "Контроль"
    """

    __tablename__ = 'univer_control'

    id = Column('control_id', Integer, primary_key=True)
    name_ru = Column('control_name_ru', String(100))

    def __repr__(self):
        return '<Control {} (id={})>'.format(self, self.id)
    
    def __str__(self):
        return self.name_ru


class ControllType(Base):
    """
    Модель "Тип контроля"
    """

    __tablename__ = 'univer_controll_type'

    # Идентификатор
    id = Column('controll_type_id', Integer, primary_key=True)

    # Наименование
    name_kz = Column('controll_type_name_kz', String(100))
    name_ru = Column('controll_type_name_ru', String(100))
    name_en = Column('controll_type_name_en', String(100))

    def __repr__(self):
        return '<ControllType {}>'.format(self)
    
    def __str__(self):
        return self.name_ru


class MarkType(Base):
    """
    Модель "Тип оценки"
    """

    __tablename__ = 'univer_mark_type'

    # Идентификатор
    id = Column('mark_type_id', Integer, primary_key=True)

    # Символ оценки
    symbol = Column('mark_type_symbol', String(10))

    # GPA
    gpa = Column('mark_type_gpa', Float)

    def __repr__(self):
        return '<MarkType {}>'.format(self)

    def __str__(self):
        return '{} ({})'.format(self.symbol, self.gpa)


class Progress(Base):
    """
    Модель "Прогресс студента"
    """

    __tablename__ = 'univer_progress'

    # Идентификатор
    id = Column('progress_id', Integer, primary_key=True)

    # Академический год
    academ_year = Column(Integer)

    # Студент
    student_id = Column(ForeignKey('univer_students.students_id'))
    student = relationship('Student')

    # Дисциплина
    subject_id = Column(ForeignKey('univer_subject.subject_id'))
    subject = relationship('Subject')

    # Тип оценки
    mark_type_id = Column(ForeignKey('univer_mark_type.mark_type_id'))
    mark_type = relationship('MarkType')

    # Кредит
    credit = Column('progress_credit', Integer)

    # Оценки
    result_rk1 = Column('progress_result_rk1', Integer)
    result_rk2 = Column('progress_result_rk2', Integer)
    result = Column('progress_result', Integer)

    # Семестры
    semester = Column('n_seme', Integer)

    # Тип контроля
    controll_type_id = Column(ForeignKey('univer_controll_type.controll_type_id'))
    controll_type = relationship('ControllType')

    # Статус
    status = Column(Integer)

    def __repr__(self):
        return '<Progress {}>'.format(self)
    
    def __str__(self):
        return '{} - {}'.format(self.student, self.subject)


class Sheet(Base):
    """
    Модель "Ведомость"
    """

    __tablename__ = 'univer_sheet'

    # Идентификатор
    id = Column('sheet_id', Integer, primary_key=True)

    # Группа
    group_id = Column(ForeignKey('univer_group.group_id'))
    group = relationship('Group')

    def __repr__(self):
        return '<Sheet {}>'.format(self)
    
    def __str__(self):
        return str(self.id)


class SheetResult(Base):
    """
    Модель "Результаты ведомости"
    """

    __tablename__ = 'univer_sheet_result'

    sheet_id = Column(ForeignKey('univer_sheet.sheet_id'), primary_key=True)
    sheet = relationship('Sheet')
    subject_id = Column(ForeignKey('univer_subject.subject_id'))
    subject = relationship('Subject')
    teacher_id = Column(ForeignKey('univer_teacher.teacher_id'))
    teacher = relationship('Teacher')
    academ_year = Column(Integer)
    semester = Column('semestr', Integer)
    control = Column(Integer, primary_key=True)
    student_id = Column(ForeignKey('univer_students.students_id'), primary_key=True)
    student = relationship('Student')
    result = Column(Float)
    date_keep = Column(DateTime)
    P_P = Column(Integer)
    n_seme = Column(Integer)
    mark_sheet_result = Column(Integer)
    retake_type = Column(Integer)

    def __repr__(self):
        return '<SheetResult {} (sheet_id={})>'.format(self, self.sheet_id)
    
    def __str__(self):
        return str(self.sheet_id)