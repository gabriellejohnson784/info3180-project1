"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app,db
from flask import render_template, request, redirect, url_for
from app.models import Property
from app.forms import propform
from werkzeug.utils import secure_filename

###
# Routing for your application.
###


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/property/create', methods =['POST', 'GET']) 
def create(): 
    form = propform()

    if request.method =='POST':
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            rooms = form.rooms.data
            bathrooms =form.bathrooms.data
            price = form.price.data
            type = form.type.data
            location = form.location.data
            photo = form.photo.data
            filename= secure_filename(photo.filename)
            newlisting= Property(title, description, rooms, bathrooms, price, type,location, filename)
            db.session.add(newlisting)
            db.session.commit()
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Property has been saved successfully')
            return redirect(url_for('property'))
    return render_template('property.html', form=form)

@app.route('/properties')
def properties():
    # Query all the properties from the database
    proplist = Property.query.all()
    # Render a template and pass the properties to it
    return render_template('allproperties.html', properties=proplist)

@app.route('/properties/<int:property_id>')
def propertydesc(id):
    # Query the specific property from the database using its ID
    property = Property.query.filter_by(id=id).first()
    # Render the detailed property view template with the property data
    return render_template('propdesc.html', property=property)



def get_uploaded_image():
    uploads_dir = os.path.join(app.config['UPLOAD_FOLDER'])
    uploaded_images = [f for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f))]
    return uploaded_images

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)




@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
