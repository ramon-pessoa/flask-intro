#################
#### imports ####
#################

from project import db
from project.models import BlogPost
from flask import render_template, Blueprint, flash, url_for, redirect, request
from forms import MessageForm
from sqlalchemy.exc import OperationalError
from flask_login import login_required, current_user

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


################
#### routes ####
################

# use decorators to link the function to a url
@home_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
	error = None
	form = MessageForm(request.form)
	if form.validate_on_submit():
		new_message = BlogPost(
			form.title.data,
			form.description.data,
			current_user.id
		)
		db.session.add(new_message)
		db.session.commit()
		flash('New entry was successfully posted. Thanks.')
		return redirect(url_for('home.home'))
	else:
		posts=""
		try:
			posts = db.session.query(BlogPost).all()
		except OperationalError:
			flash("You have no database! Please, contact your system administrator to set up the database!")

		return render_template('index.html', posts=posts, form=form, error=error)

@home_blueprint.route('/welcome')
def welcome():
	return render_template("welcome.html") # render a template
