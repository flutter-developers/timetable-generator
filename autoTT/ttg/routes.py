from flask import render_template, url_for, flash, redirect, request
from ttg import app, db
from ttg.model import Professor, Course, Batch
from ttg.new_scheduler import scheduler
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os

@login_required
@app.route('/add_course',methods=['GET','POST'])
def add_course():
	if request.method=='POST':
		subject=request.form['subject']
		'''
		{
			course_id: 1,
			course_name: 'ABC DEF',
			course_short_form: 'AD',
			course_type: 'lab/lecture/elective',
			preferred_rooms: None -- only for labs we send it
		}
		'''
		
		# check if already in DB
		c1 = Course.query.filter_by(course_id=subject.course_id).first()		
		# If yes, Don't add
		if c1 :
			flash('Course already exists!','warning')
			return {
			'status': 'FAILURE'
			}
			# return redirect(url_for('index'))	
		# If No, Add!
		else:
			duration, frequency = 0, 0
    		# Create course object and initialize
			if subject.course_type == 'elective':
				duration, frequency = 2 , 2 
			elif oe.course_type == 'Lecture':
				duration, frequency = 1 , 4 
			elif oe.course_type == 'lab':
				preferred_rooms = subject.preferred_rooms
			c = Course(subject.course_id, subject.course_name, subject.course_short_form,subject.course_type,duration,frequency,preferred_rooms)
			# db.session.begin_nested()
			db.session.add(c)
			# db.session.flush()
			db.session.commit()
			flash('Course added!','success')
			# return redirect(url_for('index'))
			return {
			'status': 'SUCCESS'
			}

@login_required
@app.route('/delete_course',methods=['GET','POST'])
def delete_course():
	if request.method=='POST':
		course_id=request.form['course_id']	
		c=Course.query.filter_by(course_id=course_id).first()
		# db.session.delete(cart)
		c.delete()
		db.session.commit()
		flash('Course removed!','success')
		return {
			'status': 'SUCCESS'
			}

@app.route('/view_courses',methods=['GET'])
def view_courses():
	if request.method=='GET':
		c=Course.query().all()
		return {
			'status': 'SUCCESS',
			'data': c
			}

###################################################################

@login_required
@app.route('/add_faculty',methods=['GET','POST'])
def add_faculty():
	if request.method=='POST':
		f=request.form['faculty']
		'''
		{
			professor_id: 1,
			professor_name: 'ABC DEF',
			department: 'CSE'
		}
		'''		
		# check if already in DB
		p1 = Professor.query.filter_by(professor_id=f.professor_id).first()		
		# If yes, Don't add
		if p1 :
			flash('Faculty already exists!','warning')
			return {
			'status': 'FAILURE'
			}	
		# If No, Add!
		else:
    		# Create Faculty object and initialize		
			p = Professor(f.department, f.professor_id, f.professor_name)
			# db.session.begin_nested()
			db.session.add(p)
			# db.session.flush()
			db.session.commit()
			flash('Faculty added!','success')
			# return redirect(url_for('index'))
			return {
			'status': 'SUCCESS'
			}


@login_required
@app.route('/delete_faculty',methods=['GET','POST'])
def delete_faculty():
	if request.method=='POST':
		professor_id=request.form['professor_id']	
		p=Professor.query.filter_by(professor_id=professor_id).first()
		# db.session.delete(cart)
		p.delete()
		db.session.commit()
		flash('Professor removed!','success')
		return {
			'status': 'SUCCESS'
			}

@app.route('/view_faculty',methods=['GET'])
def view_faculty():
	if request.method=='GET':
		p=Professor.query().all()
		return {
			'status': 'SUCCESS',
			'data': p
			}

###################################################################

@login_required
@app.route('/generate_timetable',methods=['GET'])
def generate_timetable():
	if request.method=='GET':
		batch_list = []
		# b_room = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8',
		# 'R9', 'R10', 'R11', 'R12', 'R13', 'R14', 'R15', 'R16']
		# for _ in range(16):
		# 	t = Batch('CSE', 4, _ + 1, b_room[_], False)
		# 	batch_list.append(t)

		b_room = ['R1', 'R2', 'R3', 'R4']
		for _ in range(4):
			t = Batch('CSE', 3, _ + 1, b_room[_], False)
			batch_list.append(t)
		print('\n#################################################################')
		print('batch_list === ',batch_list)
		print('#################################################################\n')

		course_list = Course.query().all()
		print('\n#################################################################')
		print('course_list === ', course_list)
		print('#################################################################\n')

		faculty_list = p=Professor.query().all()
		print('\n#################################################################')
		print('faculty_list === ', faculty_list)
		print('#################################################################\n')

		timetable = scheduler(course_list,faculty_list,batch_list)
		print('\n#################################################################')
		print(timetable)
		print('#################################################################\n')
		

