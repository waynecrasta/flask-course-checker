from flask import render_template, flash
from app import app
from .forms import CourseForm
from .course_checker import check_open


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CourseForm()
    if form.validate_on_submit():
        avail = check_open(form.department.data, form.number.data, form.crn.data)
        flash(avail)
    return render_template('course.html', form=form)
