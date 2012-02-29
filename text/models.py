# text/models.py

import datetime

from django.conf import settings
from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.db.models import permalink

from text.managers import PostManager

class TitleBase(models.Model):
    """
        An abstract content block with a title.
    """
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True

class BlurbBase(models.Model):
    """
        An abstract content block with a text blurb.
    """
    text = models.TextField()

    def __unicode__(self):
        return self.text[:20]

    class Meta:
        abstract = True

class ArticleBase(TitleBase, BlurbBase):
    """
        An abstract content block with a title, text blurb, and excerpt.
    """
    excerpt = models.TextField()
    slug = models.SlugField(unique_for_date='date_published')

    class Meta:
        abstract=True

class StatusMixin(models.Model):
    """
        Allow for a content to be marked with a status

    """
    STATUS_LIVE = 1
    STATUS_HIDDEN = 2
    STATUS_PENDING = 3
    STATUS_DRAFT = 4
    STATUS_CHOICES = (
        (STATUS_LIVE, 'Live'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_DRAFT, 'Draft'),
        (STATUS_HIDDEN, 'Hidden'),
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                              default=STATUS_LIVE,
                                              help_text="Only content with live status will be publicly displayed.")

    class Meta:
        abstract = True

        
class PostMixin(models.Model):
    """
        A mixin for a catalogued content type.
    """

    objects = PostManager()

    # metadata
    author = models.ForeignKey(User)
    published = models.DateTimeField(default=datetime.datetime.now)

    #auto-generated fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-published']
        get_latest_by = 'published'

    def get_previous(self):
        return self.get_previous_by_published(status=self.STATUS_LIVE)

    def get_next(self):
        return self.get_next_by_published(status=self.STATUS_LIVE)


class EntryBase(ArticleBase, StatusMixin, PostMixin):
    """
        An article with status and post information
    """
    class Meta:
        abstract = True


    



