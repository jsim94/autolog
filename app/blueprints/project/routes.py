# app > project > route.py
import os
from sqlalchemy.exc import NoResultFound
from flask import current_app, render_template, request, redirect, url_for, g, flash, abort
from flask_login import current_user, login_required

from . import bp
from app.models.projects import Project, Update, Comment
from app.models.images import ProjectPicture
from app.forms import NewProjectForm, EditProjectForm, AddModForm, UpdateForm, CommentForm
from app.utils import owner_required, save_image_file, delete_image_file

from app.bcolors import bcolors


@bp.url_value_preprocessor
def get_project_object(endpoint, values):
    '''Gets the project object from database and adds it and the users ownership status to flask global'''
    try:
        g.project = Project.get_by_id(id=values['project_id'])
        g.owner = True if g.project.user == current_user else False
    except NoResultFound:
        abort(404)
    except KeyError:
        return
    if g.project.private.value == 'PRIVATE' and not g.owner:
        abort(403)


@bp.route('/<project_id>/get-form')
def get_modal_form(project_id):
    '''Takes 'form' query param and returns the request form '''
    type = request.args.get('form')
    update_id = request.args.get('updateId')
    comment_id = request.args.get('commentId')

    if type == 'newUpdate':
        if not g.owner:
            abort(403)
        title = 'New Post'
        url = url_for('project.new_update', project_id=project_id)
        return render_template('modal_form.html', form=UpdateForm(), title=title, url=url)

    if type == 'editUpdate':
        if not g.owner:
            abort(403)
        title = 'Update Post'
        url = url_for('project.edit_update',
                      project_id=project_id, update_id=update_id)
        update = Update.get_by_id(update_id)
        return render_template('modal_form.html', form=UpdateForm(obj=update), title=title, url=url)

    if type == 'addMod':
        if not g.owner:
            abort(403)
        title = 'Add Mod'
        url = url_for('project.add_mod', project_id=project_id)
        return render_template('modal_form.html', form=AddModForm(), title=title, url=url)

    if type == 'followers':
        title = 'Followers'
        return render_template('modal_followers.html', title=title)

    if type == 'editComment':
        if not current_user:
            abort(403)
        title = 'Edit Comment'
        url = url_for('project.edit_comment',
                      project_id=project_id, comment_id=comment_id)
        comment = Comment.get_by_id(comment_id)
        return render_template('modal_form.html', title=title, url=url, form=CommentForm(obj=comment))

    abort(400)


@bp.route('/<project_id>')
def show(project_id):
    '''Retreives the page for the project car if found and if the requesting client has access to the page.'''

    try:
        comment_form = CommentForm(
            user_id=getattr(g, 'current_user').id)
    except AttributeError:
        comment_form = None

    return render_template('project.html', comment_form=comment_form)


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
        data = form.data.copy()
        data.pop('csrf_token', None)

        g.project.edit(keys=data)
        flash('Project Successfully edited', 'info')

        return redirect(url_for('project.show', project_id=project_id))

    return render_template('project_edit.html', form=form, user=current_user)


@bp.route('/<project_id>/add-follow')
@login_required
def add_follow(project_id):
    '''Route to add a project to a users following list'''
    try:
        g.project.add_follow(user=current_user)
        flash(f'Now following {g.project.name}', 'info')
    except:
        flash('Error occured', 'error')
        abort(500)
    return redirect(request.referrer)


@bp.route('/<project_id>/remove-follow')
@login_required
def remove_follow(project_id):
    '''Route to remove a project to a users following list'''
    try:
        g.project.remove_follow(user=current_user)
        flash(f'No longer following {g.project.name}', 'info')
    except:
        flash('Error occured', 'error')
        abort(500)

    return redirect(request.referrer)


@bp.route('/<project_id>/add-picture', methods=['POST'])
@owner_required
def add_picture(project_id):
    '''Route to add a picture to a users project'''
    ip = request.remote_addr
    file = request.files['file']

    image = ProjectPicture.create(
        filename=file.filename, project=g.project, ip=ip)
    save_image_file(
        file=file,
        fn=image.filename,
        path=os.path.join(
            current_app.config['UPLOAD_FOLDER'], 'project_pictures'),
        tb_size=(350, 350))

    if image:
        return 'Success', 200
    abort(500)


@bp.route('/<project_id>/<picture_id>/delete')
@owner_required
def delete_picture(project_id, picture_id):
    '''Route to remove a picture from a users project'''
    try:
        image = ProjectPicture.get_by_id(id=picture_id)
        image.delete()
        delete_image_file(
            fn=image.filename,
            path=os.path.join(
                current_app.config['UPLOAD_FOLDER'], 'project_pictures'))
    except AttributeError:
        abort(404)
    except FileNotFoundError as e:
        print('WARNING', e)
        flash('Error deleting picture')

    flash('Picture deleted', 'info')
    return redirect(url_for('project.show', project_id=project_id))


@bp.route('/<project_id>/add-mod', methods=['POST'])
@owner_required
def add_mod(project_id):
    '''Route to add a mod to a project's mod list'''
    form = AddModForm()
    if form.validate_on_submit():
        mod = form.mod.data
        g.project.add_mod(mod)
        return redirect(url_for('project.show', project_id=project_id))
    abort(400)


@bp.route('/<project_id>/delete-mod/<int:index>', methods=['DELETE'])
@owner_required
def delete_mod(project_id, index):
    '''Route to delete a mod from a project's mod list'''
    try:
        g.project.delete_mod(index=index)
    except IndexError:
        abort(404)
    return 'Success', 200


@bp.route('/<project_id>/new-update', methods=['POST'])
@owner_required
def new_update(project_id):
    '''Route to add an update to a users project'''
    form = UpdateForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        update = Update.create(project_id=project_id,
                               title=title, content=content)
    else:
        flash('Error Occurred', 'error')
    return redirect(url_for('project.show', project_id=project_id))


@bp.route('/<project_id>/edit-update/<update_id>', methods=['POST'])
@owner_required
def edit_update(project_id, update_id):
    '''Route to edit an existing project update'''
    form = UpdateForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        update = Update.get_by_id(update_id)
        update.edit(title=title, content=content)
    else:
        flash('Error Occurred', 'error')
    return redirect(url_for('project.show', project_id=project_id))


@bp.route('<project_id>/delete-update/<update_id>')
@owner_required
def delete_update(project_id, update_id):
    '''Route to delete an update from a users project'''
    try:
        update = Update.get_by_id(update_id)
    except NoResultFound:
        abort(404)
    update.delete()
    return redirect(url_for('project.show', project_id=project_id))


@bp.route('/<project_id>/new-comment', methods=['POST'])
@login_required
def new_comment(project_id):
    '''Route to add a comment to a project'''
    form = CommentForm()

    if form.validate_on_submit():
        user_id = form.user_id.data
        content = form.content.data

        comment = Comment.create(
            user_id=user_id, project_id=project_id, content=content)

        if not comment:
            flash('Error adding comment', 'error')
        return redirect(url_for('project.show', project_id=project_id))
    abort(400)


@bp.route('/<project_id>/edit-comment/<comment_id>', methods=['POST'])
@login_required
def edit_comment(project_id, comment_id):
    '''Route to edit a comment'''
    form = CommentForm()

    try:
        comment = Comment.get_by_id(comment_id)
    except NoResultFound:
        abort(404)

    if not current_user == comment.user:
        abort(403)

    if form.validate_on_submit():
        content = form.content.data
        comment.edit(content=content)
        flash('Comment updated', 'info')

        return redirect(url_for('project.show', project_id=project_id))
    abort(400)


@bp.route('/<project_id>/delete-comment/<comment_id>')
@login_required
def delete_comment(project_id, comment_id):
    '''Route to delete a comment to a project'''
    try:
        comment = Comment.get_by_id(comment_id)
    except NoResultFound:
        abort(404)

    if g.owner or current_user == comment.user:
        comment.delete()
    return redirect(url_for('project.show', project_id=project_id))


@bp.route('/<project_id>/delete')
@owner_required
def delete(project_id):
    '''Deletes project from database'''
    g.project.delete()
    flash('Project deleted', 'info')
    return redirect(url_for('profile.show', username=g.project.user.username))
