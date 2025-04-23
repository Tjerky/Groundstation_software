from logger import get_logger

logger = get_logger(logfile="log_test.txt")

logger.info("This is a test!")

for i in range(5):
    logger.info(f"Task #{i+1} added")
