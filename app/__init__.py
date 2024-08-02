from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler    # pylint: disable=E0401:import-error

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()

def create_app():
    """
    create app
    """
    app = Flask(__name__)
    app.config.from_object('config.Config')
    # 添加调度器默认配置
    app.config['SCHEDULER_API_ENABLED'] = True

    db.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)

    from app.blueprints import scraper
    def fetch_chat_with_context():
        with app.app_context():
            scraper.fetch_and_store_data()

    def summary_score_with_context():
        with app.app_context():
            scraper.batch_summary()
        
    scheduler.start()
    
    scheduler.add_job(id='Fetch Chat Record', func=fetch_chat_with_context, trigger='interval', minutes=1)
    scheduler.add_job(id='Summary Score', func=summary_score_with_context, trigger='interval', minutes=1)

    from .blueprints.book_management import book_management_bp # ignore C0415
    from app.blueprints.scraper import summary_score_manager
    
    app.register_blueprint(book_management_bp, url_prefix='/books')
    app.register_blueprint(summary_score_manager, url_prefix='/summary')

    return app

