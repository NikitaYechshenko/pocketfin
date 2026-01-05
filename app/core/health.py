import logging
import asyncio
from threading import Thread
from app.core.database import check_database_connection

logger = logging.getLogger(__name__)


def start_health_check(interval: int = 120):
    """Запускает проверку БД каждые interval секунд (по умолчанию 2 минуты)"""
    def health_check_loop():
        while True:
            try:
                asyncio.sleep(interval)
                is_connected = check_database_connection()
                if not is_connected:
                    logger.warning("⚠ БД недоступна - требуется переподключение")
            except Exception as e:
                logger.error(f"Ошибка в health check: {str(e)}")

    thread = Thread(target=health_check_loop, daemon=True)
    thread.start()
    logger.info(f"Health check запущен (проверка каждые {interval} сек)")