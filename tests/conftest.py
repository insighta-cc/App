import pytest
from datetime import datetime
from app import create_app, db
from app.models import Book, BorrowRecord

@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture(scope='module')
def init_database():
    # Insert test data
    book = Book(title="Test Book", author="Author", published_date=datetime.strptime("2024-01-01", "%Y-%m-%d"), price=10.0)
    db.session.add(book)
    db.session.commit()

    borrow_record = BorrowRecord(book_id=book.id, borrow_date=datetime.strptime("2024-01-01", "%Y-%m-%d"), fee=0.0)
    db.session.add(borrow_record)
    db.session.commit()

    yield db

    # Clean up
    db.session.remove()
    db.drop_all()

