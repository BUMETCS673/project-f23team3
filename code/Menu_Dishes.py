from flask import Blueprint, Flask, render_template, url_for, request, redirect
from Models import db, Dish_Label, Menu_dishes

menu_dishes = Blueprint('menu_dishes', __name__)

@menu_dishes.route('/fm_insert_form')  # dishes menu insert form
def insert_index():
    main_menu_data = db.session.query(Menu_dishes.id, Menu_dishes.name).all()
    return render_template('menu/dishes/insert.html', main_menus=main_menu_data)


@menu_dishes.route('/fm_insert_post', methods=['POST'])  # dishes menu insert action method for POST
def insert_post():
    if request.method == 'POST':
        data = {

            'main_menu_id': request.form.get('main_menu_id'),
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price': request.form.get('price')
        }
        full_menu = Dish_Label(**data)
        db.session.add(full_menu)
        db.session.commit()
        return redirect(url_for('dishes.insert_index'))


@menu_dishes.route('/fm_customer_view/<int:main_dish_id>')
def customer_index(main_dish_id):
    dishes_items = Menu_dishes.query.filter_by(main_dish_id=main_dish_id).all()
    return render_template('menu/dishes/customer_view.html', dishes_items=dishes_items)
