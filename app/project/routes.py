# app > project > route.py

from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required

from . import bp
from app.models.projects import Project
from app.forms import NewProjectForm

from app.bcolors import bcolors

from app import project


@bp.route('/<project_id>')
def show(project_id):
    '''Retreives the page for the project car if found and if the requesting client has access to the page.'''
    project = Project.get_by_uuid(project_id)
    return render_template('project.html', project=project)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    '''GET returns new project page and POST submits new project'''
    form = NewProjectForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        model_id = form.model_id.data
        private = form.private.data

        year = request.form.get('year')
        make = request.form.get('make')
        model = request.form.get('model')

        horsepower = form.horsepower.data
        torque = form.torque.data
        weight = form.weight.data
        drivetrain = form.drivetrain.data
        engine_size = form.engine_size.data

        project = Project.create(
            user_pk=current_user.pk,
            name=name,
            description=description,
            model_id=model_id,
            private=private,
            year=year,
            make=make,
            model=model,
            horsepower=horsepower,
            torque=torque,
            weight=weight,
            drivetrain=drivetrain,
            engine_size=engine_size
        )
        return redirect(url_for('project.show', project_id=project.id))

    return render_template('project_form.html', form=form)
