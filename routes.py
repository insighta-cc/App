from flask import Blueprint, request, jsonify
from models import db, Book
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('main', __name__)

@bp.route('/books', methods=['GET'])
def get_books():
    try:
        books = Book.query.all()
        return jsonify([{
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "stock": book.stock
        } for book in books]), 200
    except SQLAlchemyError as e:
        return {"error": "Database error occurred."}, 500

@bp.route('/books', methods=['POST'])
def add_book():
    try:
        data = request.json
        book = Book(title=data['title'], author=data['author'], stock=data.get('stock', 0))
        db.session.add(book)
        db.session.commit()
        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "stock": book.stock
        }), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error occurred."}, 500

@bp.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    try:
        data = request.json
        book = Book.query.get_or_404(id)
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'stock' in data:
            book.stock = data['stock']
        db.session.commit()
        return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "stock": book.stock
        }), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error occurred."}, 500

@bp.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    try:
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return '', 204
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error occurred."}, 500
