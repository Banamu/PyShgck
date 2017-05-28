import logging

from pyshgck.log import get_logger


DEFAULT_LOG_LEVEL = logging.DEBUG
LOG = get_logger('pyshgck.libs.django', level=DEFAULT_LOG_LEVEL)


try:
    from django.db import models
except ImportError:
    LOG.error("Can't import Django.")


class DatetimedModel(models.Model):
    """ A model with 'created' and 'updated' read-only datetime fields. """ 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
