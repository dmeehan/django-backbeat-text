# text/managers.py

from datetime import datetime

from django.db import models
from django.db.models.query import QuerySet

class EntryMixin(object):
    def live(self):
        return self.get_query_set().filter(status=self.model.STATUS_LIVE)

    def pending(self):
        return self.get_query_set().filter(status=self.model.STATUS_PENDING)

    def hidden(self):
        return self.get_query_set().filter(status=self.model.STATUS_HIDDEN)

    def rejected(self):
        return self.get_query_set().filter(status=self.model.STATUS_REJECTED)

    def future(self):
        return self.get_query_set().filter(status=self.model.STATUS_LIVE)\
                                   .filter(published__lte=datetime.now)

class EntryQuerySet(QuerySet, EntryMixin):
    pass

class EntryManager(models.Manager, EntryMixin):
    def get_query_set(self):
        return EntryQuerySet(self.model, using=self._db)