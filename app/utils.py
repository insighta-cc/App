from datetime import datetime


def calculate_fees():
    """
    calculate fees
    """
    print("task running")

    from app.models import db, BorrowRecord
    now = datetime.utcnow()
    borrow_records = BorrowRecord.query.filter(BorrowRecord.return_date.is_(None)).all()
    for record in borrow_records:
        days_borrowed = (now - record.borrow_date).days
        record.fee = days_borrowed * 0.5  # Example fee calculation
    db.session.commit()
