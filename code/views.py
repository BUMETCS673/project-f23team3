from flask import render_template, request, session, redirect, jsonify, url_for
from CloudOP import register_with_email, login_with_email
from DataOP import *
from Models import *
from app import app


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


@app.route("/cart", methods=['POST', 'GET'])
def cart():
    if request.method == 'POST':
        dish_name = request.form.get('dish_name')
        quantity = request.form.get('quantity')
        new_order = Cart(table_id=1, dish_id=int(dish_name), quantity=quantity, special=" ")
        db.session.add(new_order)
        db.session.commit()
        return redirect("/cart")
        # return jsonify({'message': 'Order placed and paid', 'order_id': new_order.dish_id})
    else:
        cart_items = Cart.query.filter_by(table_id=1).all()
        return render_template("cart.html", cart_items=cart_items)
        # return render_template("cart.html")


@app.route("/cart/order", methods=['POST', 'GET'])
def cart_order():
    if request.method == 'POST':
        return jsonify({'message': 'Order placed'})
    else:
        return render_template("cart.html")

@app.route('/cart/delete/<int:id>')
def delete(dish_id):
    item = Cart.query.filter_by(dish_id=dish_id, user_id=1).first()
    db.session.delete(item)
    db.session.commit()
    return redirect("/cart")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        # Handle form submission
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        # Actual login are handled in local file CloudOP.py
        try:
            user = login_with_email(email, password)
            session['user'] = user
            if is_staff(user['localId']):
                return render_template('staff.html', name=find_name_from_id(user['localId']))
            return render_template("login.html", success=True)
        except ValueError as err:
            return render_template("login.html", success=False, error=err)
    else:
        # Handle GET request to render the login page
        try:
            user_id = session['user']['localId']
        except KeyError:
            # User Not Logged in
            return render_template("./login.html")
        name = find_name_from_id(user_id)
        err = "You are Logged in as " + name + " already."
        if is_staff(user_id):
            return render_template('./staff.html', name=find_name_from_id(user_id))
        return render_template("./login.html", success=False, error=err)


@app.route("/register", methods=["GET", "POST"])
def sign_up_page():
    if request.method == "POST":
        # Handle form submission
        preferred_name = request.form.get("inputName")
        email = request.form.get("inputEmail")
        password = request.form.get("inputPassword")
        # Actual Registration are handled in local file CloudOP.py
        try:
            user = register_with_email(email, password)
            session['user'] = user
            new_user = Customer(id=user['localId'], name=preferred_name, email=email)
            db.session.add(new_user)
            db.session.commit()
            return render_template("signup.html", success=True)
        except ValueError as err:
            return render_template("signup.html", success=False, error=err)
    else:
        # Handle initial GET request to render the registration page
        return render_template("./signup.html")


@app.route("/server", methods=['POST', 'GET'])
def server_landing():
    try:
        user_id = session['user']['localId']
    except KeyError:
        # User Not Logged in
        return redirect('/login')
    if active_worker(user_id):
        # Get the Newest list of all orders related to that Server ID
        orders_data = get_orders_from_staff(user_id)
        # Get the table data related to that Server ID
        tables_data = get_tables_from_staff(staff_id=user_id)
        return render_template("server.html", orders=orders_data, tables=tables_data, name=find_name_from_id(user_id))
    else:
        # Not worker or not on duty (include manager and kitchen), return to order page.
        return render_template('staff.html', name=find_name_from_id(user_id))


@app.route('/completed-orders')
def completed_orders():
    c_orders = Order.query.filter_by(status='completed').all()
    return render_template('completed_orders.html', orders=c_orders)
# list all the completed orders


@app.route('/confirm')
def order_page():
    return render_template('./confirm.html')


@app.route('/menu')
def customer_index():
    main_dishes = DishType.query.all()
    return render_template('./menu/main_menu/customer_view.html', main_dishes=main_dishes)


@app.route("/general_admin_index", methods=["GET"])  # View all menu info for the admin user
def admin_index():
    main_dish_items = DishType.query.all()
    return render_template('./menu/main_menu/admin_view.html', main_menu_items=main_dish_items)


@app.route('/general_insert_form')  # main dishes insert form
def general_insert_index():
    return render_template('./menu/main_menu/insert.html')


@app.route('/insert_general_dishes', methods=['POST'])
def general_insert_post():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']
        main_dish = DishType(name=name, description=description)
        db.session.add(main_dish)
        db.session.commit()
        return redirect(url_for('app.general_insert_index'))


@app.route('/dishes_insert_form')  # dishes menu insert form
def dishes_insert_index():
    main_menu_data = db.session.query(Dish.id, Dish.name).all()
    return render_template('menu/full_menu/insert.html', main_menus=main_menu_data)


@app.route('/dishes_insert_post', methods=['POST'])  # dishes menu insert action method for POST
def dishes_insert_post():
    if request.method == 'POST':
        data = {

            'main_menu_id': request.form.get('main_menu_id'),
            'name': request.form.get('name'),
            'description': request.form.get('description'),
            'price': request.form.get('price')
        }
        full_menu = Dish(**data)
        db.session.add(full_menu)
        db.session.commit()
        return redirect(url_for('app.dishes_insert_index'))


@app.route('/dishes_customer_view/<int:general_dish_id>')
def dishes_customer_index(general_dish_id):
    dishes_items = Dish.query.filter_by(general_dish_id=general_dish_id).all()
    return render_template('menu/full_menu/customer_view.html', dishes_items=dishes_items)
