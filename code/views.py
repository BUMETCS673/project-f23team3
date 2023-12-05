from flask import render_template, request, session, redirect, jsonify, url_for
from CloudOP import register_with_email, login_with_email
from DataOP import *
from Models import *
from app import app


def login_check(must_staff=False):
    # Login Check
    try:
        userID = session['user']['localId']
    except KeyError:
        return False
    if must_staff:
        if is_staff(userID):
            return userID
        else:
            return False
    else:
        return userID

# User Not Logged in, visitor


@app.route('/')
def index():
    # Login Check
    try:
        user_id = session['user']['localId']
    except KeyError:
        # User Not Logged in, visitor
        return render_template('home.html', layout='./base/visitor.html')
    # Staff Check
    if active_worker(user_id):
        # Active staff
        return redirect('/server')
    # User Logged in, normal customer
    return redirect('/menu')


@app.route('/logout')
def logout():
    try:
        session.pop('user', None)
    except KeyError:
        pass
    return redirect('/login')


@app.route("/order", methods=['POST', 'GET'])
def order():
    user_id = login_check()
    if not user_id:
        return redirect('/login')
    if request.method == 'POST':
        return redirect("/order")
    else:
        order_items = db.session.query(Order.id, Requests).filter(Requests.order_id == Order.id).filter_by(
            customer_id=user_id).all()
        order_dict = {}
        for item in reversed(order_items):
            if item[0] in order_dict:
                order_dict[item[0]].append(item[1])
            else:
                order_dict[item[0]] = [item[1]]
        return render_template("order.html", order_items=order_dict)


@app.route("/kitchen", methods=['POST', 'GET'])
def kitchen():
    user_id = login_check(must_staff=True)
    if not user_id:
        return redirect('/login')
    if request.method == 'POST':
        return redirect("/kitchen")
    else:
        oids = db.session.query(Order.id).filter_by(status="0")
        kitchen_items = db.session.query(Requests).filter(Requests.order_id.in_(oids)).all()
        # return jsonify({'message': kitchen_items[0].quantity})
        return render_template("kitchen.html", kitchen_items=kitchen_items)


@app.route('/kitchen/finish/<int:id>')
def finish_order(id):
    user_id = login_check(must_staff=True)
    if not user_id:
        return redirect('/login')
    item = Order.query.filter_by(id=id).first()
    item.status = "1"
    db.session.commit()
    return redirect("/kitchen")


@app.route("/table-connect", methods=['GET', 'POST'])
def table_connect():
    if request.method == "POST":
        user_id = login_check()
        if not user_id:
            return redirect('/login')
        # Handle form submission
        table_id = request.form.get("inputTable")
        passphrase = request.form.get("inputPassphrase")
        if join_party(user_id, table_id, passphrase):
            return redirect('/cart')
        else:
            return render_template("table_connect.html", success=False, error='Incorrect combination')
    else:
        # Handle GET request to render the login page
        user_id = login_check()
        if not user_id:
            return redirect('/login')
        if not party_check(user_id):
            return render_template('table_connect.html')


@app.route("/cart", methods=['POST', 'GET'])
def cart():
    # User check
    user_id = login_check()
    if not user_id:
        return redirect('/login')
    # Table check
    if not party_check(user_id):
        return redirect('/table-connect')

    if request.method == 'POST':
        dish_name = request.form.get('dish_name')
        quantity = request.form.get('quantity')
        new_cart_entry = Cart(table_id=1, dish_id=int(dish_name), quantity=quantity, special=" ")
        db.session.add(new_cart_entry)
        db.session.commit()
        return redirect("/cart")
        # return jsonify({'message': 'Order placed and paid', 'order_id': new_order.dish_id})
    else:
        cart_items = Cart.query.filter_by(table_id=1).all()
        return render_template("cart.html", cart_items=cart_items)
        # return render_template("cart.html")


@app.route("/cart/order", methods=['POST', 'GET'])
def cart_order():
    # User check
    user_id = login_check()
    if not user_id:
        return redirect('/login')
    # Table check
    if not party_check(user_id):
        return redirect('/table-connect')
    if request.method == 'POST':
        # add item to Requests table
        tid = Party.query.filter_by(customer_id=user_id).first().table_id
        items = Cart.query.filter_by(table_id=tid)
        server_id = DiningTable.query.get(id=tid).server
        # add an order to Orders table, ID auto increment
        new_order = Order(status="0", customer_id=user_id, total=0, server_id=server_id)
        db.session.add(new_order)
        db.session.commit()
        oid = new_order.id
        for item in items:
            new_request = Requests(order_id=oid, dish_id=item.dish_id, quantity=item.quantity, special='0')
            db.session.add(new_request)
            db.session.commit()
        clear_cart(tid)
        return redirect("/order")
    else:
        return render_template("cart.html")


@app.route('/cart/delete/<int:id>')
def delete(id):
    # User check
    user_id = login_check()
    if not user_id:
        return redirect('/login')
    # Table check
    if not party_check(user_id):
        return redirect('/table-connect')

    item = Cart.query.filter_by(dish_id=id, table_id=1).first()
    db.session.delete(item)
    db.session.commit()
    return redirect("/cart")


@app.route('/cart/add/<int:id>')
def add(id):
    # User check
    user_id = login_check()
    if not user_id:
        return redirect('/login')
    # Table check
    if not party_check(user_id):
        return redirect('/table-connect')

    item = Cart.query.filter_by(dish_id=id, table_id=1).first()
    item.quantity += 1
    db.session.commit()
    return redirect("/cart")


@app.route('/cart/subtract/<int:id>')
def subtract(id):
    # User check
    user_id = login_check()
    if not user_id:
        return redirect('/login')
    # Table check
    if not party_check(user_id):
        return redirect('/table-connect')

    item = Cart.query.filter_by(dish_id=id, table_id=1).first()
    item.quantity -= 1
    if item.quantity > 0:
        db.session.commit()
    else:
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
            return redirect('/')
        except ValueError as err:
            return render_template("login.html", success=False, error=err)
    else:
        # Handle GET request to render the login page
        try:
            user_id = session['user']['localId']
        except KeyError:
            # User Not Logged in
            return render_template("./login.html")
        return redirect('/')


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
            return render_template("signup.html", success=True, layout='./base/visitor.html')
        except ValueError as err:
            return render_template("signup.html", success=False, error=err, layout='./base/visitor.html')
    else:
        # Handle initial GET request to render the registration page
        return render_template("./signup.html", layout='./base/visitor.html')


@app.route("/server", methods=['POST', 'GET'])
def server_landing():
    user_id = login_check(True)
    if not user_id:
        return redirect('/login')

    if active_worker(user_id):
        # Get the Newest list of all orders related to that Server ID
        orders_data = Order.query.filter_by(server_id=user_id)
        # Get the table data related to that Server ID
        tables_data = get_tables_from_staff(staff_id=user_id)
        if tables_data is None:
            return redirect('/kitchen')
        return render_template("server.html", orders=orders_data, tables=tables_data, layout='./base/staff.html')
    else:
        # Not worker or not on duty (include manager and kitchen), return to order page.
        return redirect('/menu')


@app.route('/completed-orders')
def completed_orders():
    user_id = login_check()
    if not user_id:
        return redirect('/login')
    c_orders = Order.query.filter_by(status='completed').all()
    return render_template('completed_orders.html', orders=c_orders, layout='./base/customer.html')


@app.route('/menu')
def customer_index():
    main_dishes = DishType.query.all()
    try:
        user_id = session['user']['localId']
        return render_template('./menu/main_menu/customer_view.html', main_dishes=main_dishes,
                               layout='./base/customer.html')
    except KeyError:
        # User Not Logged in
        return render_template('./menu/main_menu/customer_view.html', main_dishes=main_dishes,
                               layout='./base/visitor.html')


@app.route("/general_admin_index", methods=["GET"])  # View all menu info for the admin user
def admin_index():
    user_id = login_check(must_staff=True)
    if not user_id:
        return redirect('/login')
    main_dish_items = DishType.query.all()
    return render_template('./menu/main_menu/admin_view.html', main_menu_items=main_dish_items)


@app.route('/general_insert_form')  # main dishes insert form
def general_insert_index():
    user_id = login_check(must_staff=True)
    if not user_id:
        return redirect('/login')
    return render_template('./menu/main_menu/insert.html')


@app.route('/insert_general_dishes', methods=['POST'])
def general_insert_post():
    user_id = login_check(must_staff=True)
    if not user_id:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        pic_url = request.form['image_url']
        main_dish = DishType(name=name, description=description, pic_url=pic_url)
        db.session.add(main_dish)
        db.session.commit()
        return redirect(url_for('app.general_insert_index'))


@app.route('/dishes_insert_form')  # dishes menu insert form
def dishes_insert_index():
    user_id = login_check(must_staff=True)
    if not user_id:
        return redirect('/login')
    main_menu_data = db.session.query(Dish.id, Dish.name).all()
    return render_template('menu/full_menu/insert.html', main_menus=main_menu_data)


@app.route('/dishes_insert_post', methods=['POST'])  # dishes menu insert action method for POST
def dishes_insert_post():
    user_id = login_check(must_staff=True)
    if not user_id:
        return redirect('/login')
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
    try:
        user_id = session['user']['localId']
        return render_template('menu/full_menu/customer_view.html', dishes_items=dishes_items,
                               layout='./base/customer.html')
    except KeyError:
        # User Not Logged in
        return render_template('menu/full_menu/customer_view.html', dishes_items=dishes_items,
                               layout='./base/visitor.html')
