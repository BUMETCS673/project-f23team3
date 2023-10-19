from flask import Blueprint, Flask, render_template, url_for, request, redirect
from Models import db, MainMenu, FullMenu

full_menu = Blueprint('full_menu', __name__)


@full_menu.route('/fm_insert_form')  # Full menu insert form
def insert_index():
    main_menu_data = db.session.query(MainMenu.id, MainMenu.name).all()
    return render_template('menu/full_menu/insert.html', main_menus=main_menu_data)


@full_menu.route('/fm_insert_post', methods=['POST'])  # Full menu insert action method for POST
def insert_post():
    if request.method == 'POST':
        data = {
            'main_menu_id': request.form.get('main_menu_id'),
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price': request.form.get('price')
        }
        full_menu = FullMenu(**data)
        db.session.add(full_menu)
        db.session.commit()
        return redirect(url_for('full_menu.insert_index'))


@full_menu.route('/fm_customer_view/<int:main_menu_id>')
def customer_index(main_menu_id):
    fullmenu_items = FullMenu.query.filter_by(main_menu_id=main_menu_id).all()
    return render_template('menu/full_menu/customer_view.html', full_menu_items=fullmenu_items)
