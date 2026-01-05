import logging
import time
from threading import Thread
from app.core.database import check_database_connection

logger = logging.getLogger(__name__)


def start_health_check(interval: int = 120):
    def health_check_loop():
        while True:
            try:
                time.sleep(interval)
                is_connected = check_database_connection()
                if not is_connected:
                    logger.warning("⚠ Database unavailable")
            except Exception as e:
                logger.error(f"Health check error: {str(e)}")

    thread = Thread(target=health_check_loop, daemon=True)
    thread.start()
    logger.info(f"Health check started (interval: {interval} seconds)")