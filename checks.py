# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 09:26:35 2019

Check the pre-requisites for a certain course given a list of enrolled 
students

@author: moconnor
"""
import csv

def __main__():
    '''
    Reads the transcript for each student on the course roster and prints
    a list of students who are missing prerequistes and overall compliance
    
    Returns:
        None
    '''
    course = input('Course: ')
    sem = input('Semester: ')
    all_students = 0
    missing_students = 0
    student_list = []
    # Open roster file
    with open(str(sem) + '/rosters/' + course +'.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        # build a list of classes for each student
        for row in csv_reader:
            all_students += 1
            build_classes(row, student_list,sem,course)
        # check prerequisites for each student
        for student in student_list:
            check_one(student, course, sem)
    for student in student_list:
        # print student if they are missing prerequisites
        if len(student.missing_courses)>0:
            missing_students += 1
            print(student.id_num + ';' + student.name + ';' + student.email + ';' + str(student.missing_courses))
    # print overall compliance
    print()
    print(missing_students)        
    print((all_students-missing_students)/all_students)
    
# key,value is course on transcript, required course, same when student takes
# required course, different when student took acceptable substitute
all_classes = {'ARCH161':'ARCH161', 'ARCH156':'ARCH156', 'ARCH164':'ARCH164',
               'ARCH263':'ARCH263','ARCH264':'ARCH264','ARCH363':'ARCH363',
               'ARCH364':'ARCH364','ARCH223':'ARCH223','ARCH241':'ARCH223',
               'ARCH541G':'ARCH223','ARCH227':'ARCH227','ARCH543G':'ARCH227',
               'ARCH229':'ARCH229','ARCH545G':'ARCH229','ARCH251':'ARCH251',
               'ARCH252':'ARCH252','ARCH323':'ARCH323','ARCH542G':'ARCH323',
               'ARCH329':'ARCH329','ARCH327':'ARCH327','ARCH544G':'ARCH327',
               'ARCH381':'ARCH381','ARCH382':'ARCH382','ARCH423':'ARCH423',
               'ARCH429':'ARCH429', 'HUM101':'HUM101', 'HUM100':'HUM101', 
               'MATH107':'MATH107', 'MATH113':'MATH113', 'MATH111':'MATH113',
               'PHYS102':'PHYS102', 'PHYS102A':'PHYS102A', 'PHYS111':'PHYS102',
               'PHYS111A':'PHYS102A', 'PHYS103':'PHYS103', 'HUM102':'HUM102',
               'PHYS103A':'PHYS103A', 'PHYS121':'PHYS103', 'PHYS121A':'PHYS103A',
               'MATH108':'MATH107', 'MATH110':'MATH107', 'MATH120':'MATH120', 
               'MATH115':'MATH107', 'MATH105':'MATH105', 'MATH138':'MATH113',
               'MTH127':'MATH113', 'ARCH163':'ARCH161', 'ARCH548G':'ARCH329',
               'ARCH282':'ARCH229', 'ARCH383':'ARCH329', 'HUM100': 'HUM101',
               'MATH115':'MATH107', 'MATH114':'MATH105', 'MATH112':'MATH107'}

# key, value is letter grade to weighted equivalent
grade_pts = {'A':4.0, 'B+':3.5, 'B':3.0, 'C+':2.5, 'C':2.0, 'D':1.0, 'F':0.0, 
             'W':0.0, 'I':0.0}


class Student:
    '''
    contains information about a single student
    '''
    def __init__(self, id_num, name, email):
        self.id_num=id_num
        self.name=name
        self.email=email
        self.com=[]
        self.ip={}

# parses transcript data line by line to build a list of successfully
# completed requirements and in progress courses
# info is (id_num, name, email)
def build_classes(info, student_list, sem,cou):
    s = Student(info[0],info[1],info[2])
    in_semester = False
    transfer = False
    term = 0
    with open(str(sem) + '/transcripts/' + str(s.id_num) + '.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        s.studio_grades = [0,0]
        for row in csv_reader:
            if row[0][:15]=='TRANSFER CREDIT':
                transfer = True
            if transfer and row[6]=='T' and row[0]+row[1] in all_classes:
                s.com.append(all_classes[row[0]+row[1]])
            if (row[0][:18] == 'INSTITUTION CREDIT' 
                or row[0][:19] == 'COURSES IN PROGRESS'):
                transfer = False
            if row[0][0:5]=='Term:':
                if row[0][11:]=='Fall':
                    term = int(row[0][6:10])*100+90
                elif row[0][11:]=='Spring':
                    term = int(row[0][6:10])*100+10
                elif row[0][11:]=='Summer':
                    term = int(row[0][6:10])*100+50
                else:
                    term = int(row[0][11:15])*100
            if not transfer and row[0] == 'Subject':
                in_semester = True
            elif row[0][0:11] == 'Term Totals' or row[0]=='':
                in_semester = False
            #check when grades are missing'
            elif in_semester:
                if int(term) <= int(sem) and row[8]=='':
                    if row[0]+row[1] in all_classes:
                        s.ip[all_classes[row[0]+row[1]]]=term
                elif (row[0]+row[1] in all_classes and 
                      all_classes[row[0]+row[1]] in 
                      ['HUM101', 'HUM102', 'MATH107']):
                    if row[8] in ['A','B+','B','C+','C','PASS']:
                        s.com.append(all_classes[row[0]+row[1]])
                elif (row[0]+row[1] in all_classes):
                    if row[8] in ['A','B+','B','C+','C','D','PASS']:
                        s.com.append(all_classes[row[0]+row[1]])
            if cou == 'ARCH363':
                if row[0]+row[1] == 'ARCH263':
                    if row[6] == 'T':
                        s.studio_grades[0] = 2.0
                    elif row[8] == '':
                        s.studio_grades[1] = 2.0
                    else:
                        s.studio_grades[0] = grade_pts[row[8]]
                elif row[0]+row[1] == 'ARCH264':
                    if row[6] == 'T':
                        s.studio_grades[1] = 2.0
                    elif row[8] == '':
                        s.studio_grades[1] = 2.0
                    else:
                        s.studio_grades[1] = grade_pts[row[8]]
            elif cou == 'options' or cou == 'int':
                if row[0]+row[1] == 'ARCH363':
                    s.studio_grades[0] = grade_pts[row[8]]
                elif row[0]+row[1] == 'ARCH364':
                    if row[8] == '':
                        s.studio_grades[1] = 2.0
                    else:
                        s.studio_grades[1] = grade_pts[row[8]]
            else:
                s.studio_grades = [2.0,2.0]
                
    student_list.append(s)

# checks prerequisites for one student            
def check_one(stu,cou,sem):
    missing = []
    def check_ARCH161(stu,sem):
        # Humanities continuous reg
        if 'HUM101' in stu.com:
            if 'HUM102' in stu.com:
                pass
            else:
                if 'HUM102' in stu.ip:
                    pass
                else:
                    missing.append('HUM102 reg')
        else:
            if 'HUM101' in stu.ip:
                pass
            else:
                missing.append('HUM101 reg')
        # Math continuous reg
        if 'MATH107' in stu.com:
            if 'MATH113' in stu.com:
                if 'MATH120' in stu.com or 'MATH105' in stu.com:
                    pass
                else:
                    if 'MATH120' in stu.ip or 'MATH105' in stu.ip:
                        pass
                    else:
                        missing.append('MATH120 reg')
            else:
                if 'MATH113' in stu.ip:
                    pass
                else:
                    missing.append('MATH113 reg')
        else:
            if 'MATH107' in stu.ip:
                pass
            else:
                if 'MATH113' in stu.ip:
                    pass
                else:
                    if 'MATH113' in stu.com:
                        if 'MATH105' in stu.com:
                            pass
                        else:
                            if 'MATH105' in stu.ip:
                                pass
                            else:
                                missing.append('MATH105 reg')
                    else:
                        missing.append('MATH107 reg')
    
    def check_ARCH164(stu,sem):
        check_ARCH161(stu,sem)
        if ('ARCH161' in stu.com or 
            'ARCH161' in stu.ip and stu.ip['ARCH161']<sem):
            pass
        else:
            missing.append('ARCH161')
            
    def check_ARCH263(stu,sem):
        check_ARCH164(stu,sem)
        if ('ARCH164' in stu.com or 
            'ARCH164' in stu.ip and stu.ip['ARCH164']<sem):
            pass
        else:
            missing.append('ARCH164')
            
    def check_ARCH264(stu,sem):
        check_ARCH263(stu,sem)
        if ('ARCH263' in stu.com or 
            'ARCH263' in stu.ip and stu.ip['ARCH263']<sem):
            pass
        else:
            missing.append('ARCH263')
            
    def check_ARCH363(stu,sem):
        check_ARCH264(stu,sem)
        if ('ARCH264' in stu.com or 
            'ARCH264' in stu.ip and stu.ip['ARCH264']<sem):
            pass
        else:
            missing.append('ARCH264')
        if ('ARCH223' in stu.com or 
            'ARCH223' in stu.ip and stu.ip['ARCH223']<sem):
            pass
        else:
            missing.append('ARCH223')  
        if ('ARCH227' in stu.com or 
            'ARCH227' in stu.ip and stu.ip['ARCH227']<sem):
            pass
        else:
            missing.append('ARCH227')
        if ('ARCH229' in stu.com or 
            'ARCH229' in stu.ip and stu.ip['ARCH229']<sem):
            pass
        else:
            missing.append('ARCH229')
        if ('ARCH251' in stu.com or 
            'ARCH251' in stu.ip and stu.ip['ARCH251']<sem):
            pass
        else:
            missing.append('ARCH251')
        if ('ARCH252' in stu.com or 
            'ARCH252' in stu.ip and stu.ip['ARCH252']<sem):
            pass
        else:
            missing.append('ARCH252')
        if sum(stu.studio_grades) < 4.0:
            missing.append('2nd year studio gpa')
            
    def check_ARCH364(stu,sem):
        check_ARCH363(stu,sem)
        if ('ARCH363' in stu.com or 
            'ARCH363' in stu.ip and stu.ip['ARCH363']<sem):
            pass
        else:
            missing.append('ARCH363')
    
    def check_options(stu,sem):
        check_ARCH364(stu,sem)
        for c in ['HUM101 reg','HUM102 reg','MATH120 reg','MATH113 reg',
                  'MATH105 reg','MATH107 reg']:
            try:
                missing.remove(c)
            except:
                pass
        if ('ARCH364' in stu.com or 
            'ARCH364' in stu.ip and stu.ip['ARCH364']<sem):
            pass
        else:
            missing.append('ARCH364')
        if ('ARCH323' in stu.com or 
            'ARCH323' in stu.ip and stu.ip['ARCH323']<sem):
            pass
        else:
            missing.append('ARCH323')
        if ('ARCH329' in stu.com or 
            'ARCH329' in stu.ip and stu.ip['ARCH329']<sem):
            pass
        else:
            missing.append('ARCH329')
        if ('ARCH327' in stu.com or 
            'ARCH327' in stu.ip and stu.ip['ARCH327']<sem):
            pass
        else:
            missing.append('ARCH327')
        if ('ARCH381' in stu.com or 
            'ARCH381' in stu.ip and stu.ip['ARCH381']<sem):
            pass
        else:
            missing.append('ARCH381')
        if ('ARCH382' in stu.com or 
            'ARCH382' in stu.ip and stu.ip['ARCH382']<sem):
            pass
        else:
            missing.append('ARCH382')
        if ('HUM101' in stu.com or 
            'HUM101' in stu.ip and stu.ip['HUM101']<sem):
            pass
        else:
            missing.append('HUM101')
        if ('HUM102' in stu.com or 
            'HUM102' in stu.ip and stu.ip['HUM102']<sem):
            pass
        else:
            missing.append('HUM102')
        if ('MATH113' in stu.com or 
            'MATH113' in stu.ip and stu.ip['MATH113']<sem):
            pass
        else:
            missing.append('MATH113')
        if ('MATH105' in stu.com or 
            'MATH105' in stu.ip and stu.ip['MATH105']<sem):
            pass
        else:
            if (('MATH107' in stu.com or 
            'MATH107' in stu.ip and stu.ip['MATH107']<sem) and 
            ('MATH120' in stu.com or 
            'MATH120' in stu.ip and stu.ip['MATH120']<sem)):
                pass
            else:
                missing.append('MATH107/MATH120')
        if ('PHYS102' in stu.com or 
            'PHYS102' in stu.ip and stu.ip['PHYS102']<sem):
            pass
        else:
            missing.append('PHYS102')
        if ('PHYS102A' in stu.com or 
            'PHYS102A' in stu.ip and stu.ip['PHYS102A']<sem):
            pass
        else:
            missing.append('PHYS102A')
        if ('PHYS103' in stu.com or 
            'PHYS103' in stu.ip and stu.ip['PHYS103']<sem):
            pass
        else:
            missing.append('PHYS103')
        if ('PHYS103A' in stu.com or 
            'PHYS103A' in stu.ip and stu.ip['PHYS103A']<sem):
            pass
        else:
            missing.append('PHYS103A')
        try:
            missing.remove('2nd year studio gpa')
        except:
            pass
        if sum(stu.studio_grades) < 4.0:
            missing.append('3nd year studio gpa')
            
        
    def check_int(stu,sem):
        check_options(stu,sem)
        if ('ARCH423' in stu.com or 
            'ARCH423' in stu.ip and stu.ip['ARCH423']<sem):
            pass
        else:
            missing.append('ARCH423')
        if ('ARCH429' in stu.com or 
            'ARCH429' in stu.ip and stu.ip['ARCH429']<sem):
            pass
        else:
            missing.append('ARCH429')
            
    function_call = {'ARCH161':check_ARCH161, 'ARCH164':check_ARCH164, 
                     'ARCH263':check_ARCH263, 'ARCH264':check_ARCH264, 
                     'ARCH363':check_ARCH363, 'ARCH364':check_ARCH364,
                     'options':check_options, 'int':check_int}
    function_call[cou](stu,sem)
        
    stu.missing_courses = list(set(missing))

__main__()