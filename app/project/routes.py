# app > project > route.py

from flask import render_template, request, redirect, url_for, g, flash, abort
from flask_login import current_user, login_required

from . import bp
from app.models.projects import Project
from app.forms import NewProjectForm

from app.bcolors import bcolors

from app import project


@bp.url_value_preprocessor
def get_project_object(endpoint, values):
    g.project = Project.get_by_uuid(uuid=values.get(
        'project_id'))


@ bp.route('/<project_id>')
def show(project_id):
    '''Retreives the page for the project car if found and if the requesting client has access to the page.'''

    if not g.project:
        abort(404)

    return render_template('project.html')


@ bp.route('/new', methods=['GET', 'POST'])
@ login_required
def new():
    '''GET returns new project page and POST submits new project'''
    form = NewProjectForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        model_id = form.model_id.data
        private = form.private.data

        year = form.year.data
        make = form.make.data
        model = form.model.data
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


@bp.route('/<project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(project_id):
    '''GET returns a project edit page and POST will update project'''

    # TO BE IMPLEMENTED
    form = ''

    if form.validate_on_submit():

        if project:
            flash('Project successfully updated')
            return redirect(url_for('project.show', project_id=project.id))
        flash('Error occurred')

    return render_template('edit.html', form=form, user=current_user)


@bp.route('/<project_id>/delete', methods=['DELETE'])
@login_required
def delete(project_id):
    '''Deletes project from database'''

    if not g.project.user == current_user:
        abort(403)

    if g.project.delete():
        flash('Project deleted')
        return redirect(url_for('profile.show',))
    flash('Error Occured')

    return redirect(url_for('project.show', project_id=project_id))
