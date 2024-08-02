import logging
from app.blueprints import scraper
import os

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import dotenv
dotenv.load_dotenv()


def test_fetch(test_app, init_database):
    with test_app.app_context():
        scraper.fetch_and_store_data()