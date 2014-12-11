from flask_wtf import Form
from wtforms import TextField


class SearchForm(Form):
	search = TextField('Search')