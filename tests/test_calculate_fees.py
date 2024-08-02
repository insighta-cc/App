from app.utils import calculate_fees
from app.models import BorrowRecord

def test_calculate_fees(test_app, init_database):
    with test_app.app_context():
        calculate_fees()
        borrow_record = BorrowRecord.query.first()
        assert borrow_record.fee > 0  # Check if the fee has been updated

