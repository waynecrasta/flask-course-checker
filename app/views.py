from flask import render_template, flash, request
from app import app
from .forms import CourseForm
from .course_checker import check_open


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CourseForm()
    if form.validate_on_submit():
        avail = check_open(form.department.data, form.number.data, form.crn.data)
        flash(avail)
        # flash(return_crn(form.department.data, form.number.data))
    return render_template('course.html', form=form)


@app.route('/result', methods=['POST'])
def result():
    f = request.form
    avail = check_open(f['department'], f['course'], f['crn'])
    return render_template('result.html', avail=avail, section=f['crn'])
