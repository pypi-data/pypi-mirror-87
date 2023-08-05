from zuper_commons.logs import setup_logging, ZLogger


def test_logger1():
    setup_logging()
    logger = ZLogger("here")
    logger.info("info")
    logger.error("info")
    logger.warn("info")
    logger.warning("info")
    logger.debug("info")
    logger.setLevel(logger.INFO)
    logger.debug("info")


def test_logger2():
    logger = ZLogger("here")
    logger = logger.getChild("a")
    b = 2
    logger.info("info", 1, 2, b, a=4)
