from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo


class AdminLoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password1 = PasswordField(label='Password1', validators=[DataRequired()])
    password2 = PasswordField(label='Password2', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class AdminRegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password1 = PasswordField(label='Password1', validators=[DataRequired()])
    confirm_password1 = PasswordField(label='Confirm Password 1', validators=[DataRequired(),
                                                                           EqualTo('password1')])

    password2 = PasswordField(label='Password2', validators=[DataRequired()])
    confirm_password2 = PasswordField(label='Confirm Password 2', validators=[DataRequired(),
                                                                           EqualTo('password2')])

    submit = SubmitField(label='register')


class AddBlogForm(FlaskForm):
    title = StringField(label='title', validators=[DataRequired()])
    first_par = StringField(label='first paragraph', validators=[DataRequired()])
    image_file = FileField(label='Your Blog Picture', validators=[FileAllowed(['png', 'jpg'])])
    tags = StringField(label='Tags', validators=[DataRequired()])
    submit = SubmitField(label='Add Bolg')


class UpdateBlogForm(FlaskForm):
    title = StringField(label='title', validators=[DataRequired()])
    first_par = StringField(label='first paragraph', validators=[DataRequired()])
    image_file = FileField(label='Update Your Blog Picture', validators=[FileAllowed(['png', 'jpg'])])
    tags = StringField(label='Tags', validators=[DataRequired()])
    # image_file = StringField(label='image', validators=[DataRequired()])
    content_holder = TextAreaField(label='HTML Content')
    submit = SubmitField(label='Update Bolg')


class AddTopicForm(FlaskForm):
    name = StringField(label='Name The Topic', validators=[DataRequired()])
    topic_tags = StringField(label='Topic Tags')
    submit = SubmitField(label='Add Topic')
