from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, RadioField, validators

class DecorationForm(FlaskForm):
	description = TextAreaField('Decoration Descriptions',\
				 validators=[validators.DataRequired(), validators.Length(max=200)])

class CommentForm(FlaskForm):
	rank = RadioField('Rank', validators=[validators.DataRequired()], choices=['5','4','3','2','1'])
	contents = TextAreaField("Contents", validators=[validators.DataRequired(), validators.length(max=200)])