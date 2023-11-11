from flask import Blueprint, render_template, request, redirect, url_for
from Models import db, Dishes, Dish_Label

main_menu = Blueprint('main_menu', __name__)


@main_menu.route('/menu') # List all menu items to the customer
def customer_index():
    main_menu_items = Dishes.query.all()
    default_image = 'mm.png'
    return render_template('/menu/main_menu/customer_view.html', main_menu_items=main_menu_items)
    #return render_template('menu/main_menu/customer_view.html')


@main_menu.route("/mm_admin_index", methods=["GET"])  # View all menu info for the admin user
def admin_index():
    main_menu_items = Dishes.query.all()
    return render_template('/menu/main_menu/admin_view.html', main_menu_items=main_menu_items)


@main_menu.route('/mm_insert_form')  # main menu insert form
def insert_index():
    return render_template('/menu/main_menu/insert.html')


@main_menu.route('/mm_insert_post', methods=['POST'])  # main menu insert action method for POST
def insert_post():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']
        main_menu = Dishes(name=name, description=description)
        db.session.add(main_menu)
        db.session.commit()
        return redirect(url_for('main_menu.insert_index'))


