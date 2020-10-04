import logging

level = logging.INFO

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=level)
logging.getLogger().setLevel(level)