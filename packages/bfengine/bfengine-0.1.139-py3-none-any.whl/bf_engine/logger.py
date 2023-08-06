import logging
import sys

log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s --- [bf-engine-sdk]%(message)s'
)
handler.setFormatter(formatter)

log.addHandler(handler)
log.setLevel(logging.INFO)
