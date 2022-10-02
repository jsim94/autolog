# app > project > route.py

from functools import wraps
from flask import render_template, request, redirect, url_for, g, flash, abort
from flask_login import current_user, login_required

from . import bp
from app.models.projects import Project
from app.forms import NewProjectForm, EditProjectForm, AddModForm

from app.bcolors import bcolors


@bp.url_value_preprocessor
def get_project_object(endpoint, values):
    '''Gets the project object from database and adds it and the users ownership status to flask global'''
    try:
        g.project = Project.get_by_uuid(uuid=values['project_id'])
        g.owner = True if g.project.user == current_user else False
    except KeyError:
        return
    if not g.project:
        abort(404)


def owner_required(func):
    '''Decorator to return a 403 error if the current user is not authorized to access endpoint'''
    @wraps(func)
    def inner(*args, **kwargs):
        if not g.get('owner'):
            abort(403)
        return func(*args, **kwargs)
    return inner


@bp.route('/<project_id>')
def show(project_id):
    '''Retreives the page for the project car if found and if the requesting client has access to the page.'''
    mod_form = AddModForm()

    return render_template('project.html', mod_form=mod_form)


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

    return render_template('project_new.html', form=form)


@bp.route('/<project_id>/edit', methods=['GET', 'POST'])
@owner_required
def edit(project_id):
    '''GET returns a project edit page and POST will update project'''

    form = EditProjectForm(obj=g.project)

    if form.validate_on_submit():
        form.populate_obj(g.project)
        status = g.project.update()

        if status == 403:
            abort(403)

        if status == 200:
            flash('Project successfully updated', 'info')
            return redirect(url_for('project.show', project_id=project_id))
        flash('Error occurred')

    return render_template('project_edit.html', form=form, user=current_user)


@bp.route('/<project_id>/add-follow')
@login_required
def add_follow(project_id):
    '''Route to add a project to a users following list'''

    status = current_user.add_follow(g.project)

    match status:
        case 200:
            flash(f'Now following {g.project.name}', 'info')
            return redirect(request.referrer)
        case 500:
            flash('Error occured', 'error')
            abort(500)


@bp.route('/<project_id>/remove-follow')
@login_required
def remove_follow(project_id):
    '''Route to remove a project to a users following list'''
    status = current_user.remove_follow(g.project)

    match status:
        case 200:
            flash(f'No longer following {g.project.name}', 'info')
            return redirect(request.referrer)
        case 500:
            flash('Error occured', 'error')
            abort(500)


@bp.route('/<project_id>/add-mod', methods=['POST'])
@owner_required
def add_mod(project_id):
    '''Route to add a mod to a project's mod list'''
    form = AddModForm()
    if form.validate_on_submit():
        mod = form.mod.data
        g.project.add_mod(mod)

    else:
        flash('Error', 'error')

    return redirect(url_for('project.show', project_id=project_id))


@bp.route('/<project_id>/delete-mod/<int:index>', methods=['DELETE'])
@owner_required
def delete_mod(project_id, index):
    '''Route to delete a mod from a project's mod list'''
    status = g.project.delete_mod(index=index)
    match status:
        case 200:
            return 'Successfully deleted', 200
        case 404:
            return 'Not found', 404
        case 403:
            return 'Forbidden', 403


@bp.route('/<project_id>/delete')
@owner_required
def delete(project_id):
    '''Deletes project from database'''
    status = g.project.delete()
    match status:
        case 403:
            abort(403)
        case 200:
            flash('Project deleted', 'info')
            return redirect(url_for('profile.show', username=g.project.user.username))

    flash('Error Occured')
    return redirect(url_for('profile.show', project_id=project_id))
