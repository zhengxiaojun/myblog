from flask import Blueprint, render_template

admin = Blueprint(
    'admin',
    '__name__',
    template_folder='template/admin',
    static_folder='static/admin',
    url_prefix='/admin')


@admin.route('/')
def home():
    return render_template('home.html')
