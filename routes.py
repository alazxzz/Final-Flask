from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import User, Product, Cart, Discount,  Category
from models import Contact
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  # Veritabanı bağlantısı
from app import app  # Flask uygulamanız
import re

#  user list
def user_list():
    return [
        {"id": 1, "name": "johndoe", "email": "johndoe@example.com", "age": 28, "password": "password123", "photo": "https://th.bing.com/th/id/OIP.IGNf7GuQaCqz_RPq5wCkPgHaLH?rs=1&pid=ImgDetMain"},
        {"id": 2, "name": "janedoe", "email": "janedoe@example.com", "age": 34, "password": "janedoe456", "photo": "https://avatars.githubusercontent.com/u/40491049?v=4?s=400"},
        {"id": 3, "name": "alice", "email": "alice@example.com", "age": 22, "password": "alice789", "photo": "https://d2908q01vomqb2.cloudfront.net/972a67c48192728a34979d9a35164c1295401b71/2023/04/14/internal-cdn.amazon-2.jpg"},
        {"id": 4, "name": "bob", "email": "bob@example.com", "age": 45, "password": "bob321", "photo": "https://th.bing.com/th/id/OIP.WQvPJdjEpvh8OTXB-NBfJwHaHw?rs=1&pid=ImgDetMain"},
        {"id": 5, "name": "charlie", "email": "charlie@example.com", "age": 31, "password": "charlie654", "photo": "https://p7.hiclipart.com/preview/873/123/771/rare-leadership-4-uncommon-habits-for-increasing-trust-joy-and-engagement-in-the-people-you-lead-marcus-warner-author-amazon-com-pastor-moody.jpg"},
        {"id": 6, "name": "david", "email": "david@example.com", "age": 29, "password": "david987", "photo": "https://p7.hiclipart.com/preview/913/234/333/david-hoyle-uncle-david-business-dota-2-trinity-south-coast-business.jpg"},
        {"id": 7, "name": "eve", "email": "eve@example.com", "age": 27, "password": "eve135", "photo": "eve.jpg"},
        {"id": 8, "name": "frank", "email": "frank@example.com", "age": 33, "password": "frank246", "photo": "frank.jpg"},
        {"id": 9, "name": "grace", "email": "grace@example.com", "age": 25, "password": "grace369", "photo": "grace.jpg"},
        {"id": 10, "name": "hank", "email": "hank@example.com", "age": 37, "password": "hank852", "photo": "hank.jpg"}
    ]

# Home route
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)  # Ürünü veritabanından getir
    return render_template('product_detail.html', product=product)
@app.route('/')
@app.route('/category/<string:category>')
def home(category=None):
    if category:
        category_obj = Category.query.filter_by(title=category).first_or_404()
        products = Product.query.filter_by(category_id=category_obj.id).all()
    else:
        products = Product.query.all()
    
    categories = Category.query.all()
    return render_template('shop.html', products=products, categories=categories, current_category=category)


@app.route('/discounted-products')
def discounted_products():
    discounted_items = Discount.query.all()
    products = []
    for item in discounted_items:
        product = Product.query.get(item.product_id)
        product.discount_percentage = item.discount_percentage  # İndirimli fiyatı hesaplarken lazım olabilir
        products.append(product)
    
    return render_template('shop.html', products=products, discounted=True)
@app.route('/admin')
def admin():
    return redirect(url_for('home'))

# Detail 
@app.route('/detail', methods=['GET', 'POST'])
def detail():
    return render_template('detail.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and password :
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('profile'))
        else:
            flash('Invalid login credentials', 'danger')

    return render_template('login.html')

# Password  checker
def is_password_complex(password):
    return (len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

# Registration
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not is_password_complex(password):
            flash('Password must be at least 8 characters long and include a capital letter, a lowercase letter, a number, and a special character.', 'danger')
            return redirect(url_for('register'))

        
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/category/<category_name>')
def category_products(category_name):
    if category_name == 'all':
        products = Product.query.all()
    else:
        # Filter products by the category name
        category = Category.query.filter_by(title=category_name).first()
        products = Product.query.filter_by(category_id=category.id).all()
    
    return render_template('shop.html', products=products, current_category=category_name)
    

    return render_template('category.html', category=category, products=products)
# Profile
@app.route('/profile/', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your profile', 'warning')
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    if user:
        return render_template('profile.html', user=user)
    return "User not found", 404


# Product
@app.route('/product/<int:product_id>')
def product_details(product_id):
    return render_template('product_details.html')

# Search
@app.route('/search', methods=['GET'])
def search():
    return render_template('products.html')

# Product
@app.route('/products')
def product_list():
    return render_template('products.html')

#favorites
@app.route('/add_to_favorites/<int:product_id>', methods=['POST'])
def add_to_favorites(product_id):
    # Logic to add the product to user's favorites (implement this)
    return redirect(url_for('favorites_list'))

# Favorites
@app.route('/favorites')
def favorites_list():
    return render_template('favorites.html')

# Remove from favorites
@app.route('/remove_from_favorites/<int:product_id>', methods=['POST'])
def remove_from_favorites(product_id):
    return redirect(url_for('favorites_list'))

# Contact
@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        new_contact = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(new_contact)
        db.session.commit()

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')
@app.route('/basket')
def basket():
    return render_template('basket.html')



from flask import render_template
from models import Category, Product  

@app.route('/shop', methods=['GET'])
def shop():
    categories = Category.query.all()
    selected_category = request.args.get('category')
    if selected_category:
        products = Product.query.filter_by(category_id=selected_category).all()
    else:
        products = Product.query.all()
    return render_template('shop.html', categories=categories, products=products, current_category=selected_category)









if __name__ == '__main__':
    app.run(debug=True)
