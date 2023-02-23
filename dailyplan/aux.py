from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired,Email
from flask_mail import Message

from dailyplan.auth import login_required, get_user
from dailyplan import mail
import os

# Creates blueprint 'auth' 
bp = Blueprint('aux', __name__, url_prefix='/')


class ContactForm(FlaskForm):

    def __init__(self, user_name, user_email):
        super().__init__()
        self.name.data = user_name
        self.email.data = user_email

    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    purpose = SelectField('Purpose', choices = [('Feedback', 'Feedback'), ('Bug', 'Bug'), ('Feature Request', 'Feature Request'), ('Other', 'Other')], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


@bp.route('/contact', methods = ['GET', 'POST'])
@login_required
def contact():
    recipients = [os.environ.get('ADMIN_EMAIL')]
    name = get_user(g.user['id'])['name']
    email = get_user(g.user['id'])['email']
    form = ContactForm(name, email)

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form, name=name, email=email)
        else:
            msg = Message(form.purpose.data, recipients=recipients)
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('contact.html', form=form, name=name, email=email, success=True)
    elif request.method == 'GET':
        return render_template('contact.html', form=form, name=name, email=email)
