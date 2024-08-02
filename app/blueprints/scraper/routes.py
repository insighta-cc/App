from flask import render_template, request, redirect, url_for
from . import summary_score_manager
from app.models import Score

# @summary_score_manager.route('/')
# def index():
#     """
#     query
#     """
#     books = Book.query.all()
#     return render_template('book_list.html', books=books)

@summary_score_manager.route('/<str:address>', methods=['GET'])
def get_score(address):
    """
    add
    """
    if request.method == 'GET':
        score = Score.query.get_or_404(address=address)
        return score
    return render_template('404.html')

# @summary_score_manager.route('/edit/<int:id>', methods=['GET', 'POST'])
# def edit_book(id):
#     """
#     edit
#     """
#     book = Book.query.get_or_404(id)
#     if request.method == 'POST':
#         book.title = request.form['title']
#         book.author = request.form['author']
#         book.published_date = request.form['published_date']
#         book.price = request.form['price']
#         db.session.commit()
#         return redirect(url_for('book_management.index'))
#     return render_template('book_form.html', book=book)

# @summary_score_manager.route('/delete/<int:id>', methods=['POST'])
# def delete_book(id):
#     """
#     delete
#     """
#     book = Book.query.get_or_404(id)
#     db.session.delete(book)
#     db.session.commit()
#     return redirect(url_for('book_management.index'))

