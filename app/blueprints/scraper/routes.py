import json
from flask import render_template, request, jsonify, url_for
from flask_cors import cross_origin

from . import summary_score_manager
from app.models import Score

import logging
logger = logging.getLogger(__name__)

# @summary_score_manager.route('/')
# def index():
#     """
#     query
#     """
#     books = Book.query.all()
#     return render_template('book_list.html', books=books)

@summary_score_manager.route('/<string:address>', methods=['GET'])
@cross_origin()
def get_score(address):
    """
    get score
    """
    logger.info(f"query request: {address}")
    resp = {
        "code": 0,
        "message": '',
        "data": {}
    }
    if request.method == 'GET':
        score = Score.query.filter_by(address=address, is_deleted=False).first()
        if score:
            resp['data'] = json.loads(score.score_json)

            return jsonify(resp)
        resp['message'] = "Empty"
        return jsonify(resp)
    resp['message'] = f'Unsupport Method {request.method}'
    return jsonify(resp)

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

