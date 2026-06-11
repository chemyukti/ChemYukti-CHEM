from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Register as', choices=[('student', 'Student'), ('institute', 'Institute')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ChangePasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')

class LearningBlueprintForm(FlaskForm):
    student_class = StringField('Class', validators=[DataRequired()])
    board = StringField('Board', validators=[DataRequired()])
    exam_type = StringField('Exam Type', validators=[DataRequired()])
    learning_goal = TextAreaField('Learning Goal', validators=[DataRequired()])
    subject_interests = TextAreaField('Subject Interests', validators=[DataRequired()])
    submit = SubmitField('Generate Blueprint')

class LeadRequestForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    service_type = SelectField('Service Interested In', choices=[
        ('website', 'Educational Website Development'),
        ('app', 'Android App Development'),
        ('community', 'Private Learning Community'),
        ('integration', 'School Assessment Integration'),
        ('other', 'Other Educational Solution')
    ])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Request')

class PublicationForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price (₹)', default=150.0)
    type = SelectField('Type', choices=[('Book', 'Book'), ('Module', 'Module'), ('Resource', 'Resource')])
    submit = SubmitField('Save Publication')

class ForumPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class ForumReplyForm(FlaskForm):
    content = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Reply')
