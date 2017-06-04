from app import db
from flask_wtf import FlaskForm
from wtforms import IntegerField, FileField, DecimalField, StringField, BooleanField, TextAreaField, RadioField, validators

class SchemeForm(FlaskForm):
	description = TextAreaField('Description', validators=[validators.length(max=200)])
	image = FileField('Image', validators=[validators.DataRequired()])
	price = DecimalField('Price', validators=[validators.DataRequired(),validators.NumberRange(max=1000.0)])

class BidForm(FlaskForm):
	schID = IntegerField("SchemeID", validators=[validators.DataRequired()])
	dcID = IntegerField("DcFormID", validators=[validators.DataRequired()])
	description = TextAreaField('Description', validators=[validators.length(max=200)])
	discount = DecimalField('Discount', validators=[validators.DataRequired(),validators.NumberRange(min = 0.0, max = 1.0)])
