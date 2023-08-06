from django.db import models
from django.utils.translation import ugettext_lazy

class BaseModel(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=ugettext_lazy('Creation date'))
    edition_date = models.DateTimeField(
        auto_now=True,
        verbose_name=ugettext_lazy('Edition date'))
    

    class Meta:
        abstract = True

    @classmethod
    def get_list_url(cls):
        return '/'

    def get_absolute_url(self):
        return '/'