from flask import render_template, request, redirect, url_for
from . import book_management_bp
from app.models import db, Book

@book_management_bp.route('/')
def index():
    """
    query
    """
    books = Book.query.all()
    return render_template('book_list.html', books=books)

@book_management_bp.route('/add', methods=['GET', 'POST'])
def add_book():
    """
    add
    """
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        published_date = request.form['published_date']
        price = request.form['price']
        new_book = Book(title=title, author=author, published_date=published_date, price=price)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('book_management.index'))
    return render_template('book_form.html')

@book_management_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    """
    edit
    """
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.published_date = request.form['published_date']
        book.price = request.form['price']
        db.session.commit()
        return redirect(url_for('book_management.index'))
    return render_template('book_form.html', book=book)

@book_management_bp.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    """
    delete
    """
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('book_management.index'))

