from flask import redirect, render_template, request, url_for, Blueprint, flash
from project.messages.models import Message, Like
from project.users.views import ensure_correct_user
from project.messages.forms import MessageForm
from flask_login import current_user, login_required
from project import db
from sqlalchemy import and_

messages_blueprint = Blueprint(
    'messages',
    __name__,
    template_folder='templates'
)


@messages_blueprint.route('/', methods=["POST"])
@login_required
def index(id):
    if current_user.get_id() == str(id):
        form = MessageForm()
        if form.validate():
            new_message = Message(
                text=form.text.data,
                user_id=id
            )
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('users.show', id=id))
    return render_template('messages/new.html', form=form)


@messages_blueprint.route('/new')
@login_required
@ensure_correct_user
def new(id):
    return render_template('messages/new.html', form=MessageForm())


def check_liked_message(message_id):
    for like in current_user.likes:
        if like.message_id == message_id:
            return True
    return False 

@messages_blueprint.route('/<int:message_id>', methods=["GET", "DELETE"])
def show(id, message_id):
    found_message = Message.query.get(message_id)
    liked = check_liked_message(message_id)
    if request.method == b"DELETE" and current_user.id == id:
        db.session.delete(found_message)
        db.session.commit()
        return redirect(url_for('users.show', id=id))
    return render_template('messages/show.html', message=found_message, liked=liked)

def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

@messages_blueprint.route('/<int:message_id>/likes', methods=["POST", "DELETE"])
@login_required
def like(id, message_id):
    if request.method == "POST":
        new_like = Like(current_user.id, message_id)
        db.session.add(new_like)
        db.session.commit()
        flash('Liked message')
    elif request.method == b'DELETE':
        removed_like = Like.query.filter(and_(Like.user_id == id, Like.message_id == message_id)).first()  
        db.session.delete(removed_like)
        db.session.commit()    
    return redirect(redirect_url())

