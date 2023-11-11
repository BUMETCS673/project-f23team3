from flask import Blueprint, render_template, request, redirect, url_for
from Models import db, Menu_main_dishes, Dish_Label

main_dishes = Blueprint('Menu_MainDishes', __name__)


@main_dishes.route('/menu') # List all main dish items to the customer
def customer_index():
    main_dishes = Menu_main_dishes.query.all()
    default_image = 'mm.png'
    return render_template('/menu/main_dishes/customer_view.html', main_dishes=main_dishes)
    #return render_template('menu/main_dishes/customer_view.html')


@main_dishes.route("/mm_admin_index", methods=["GET"])  # View all menu info for the admin user
def admin_index():
    main_dish_items = main_dishes.query.all()
    return render_template('/menu/main_dishes/admin_view.html', main_menu_items=main_dish_items)


@main_dishes.route('/mm_insert_form')  # main dishes insert form
def insert_index():
    return render_template('/menu/main_dishes/insert.html')


@main_dishes.route('/mm_insert_post', methods=['POST'])  # main dishes insert action method for POST
def insert_post():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']
        main_menu = main_dishes(name=name, description=description)
        db.session.add(main_menu)
        db.session.commit()
        return redirect(url_for('main_dishes.insert_index'))


