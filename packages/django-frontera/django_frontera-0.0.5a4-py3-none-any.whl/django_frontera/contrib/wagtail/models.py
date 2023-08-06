from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel,\
    StreamFieldPanel
from wagtail.api import APIField
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page as CorePage
from wagtail.images.edit_handlers import ImageChooserPanel


class Page(CorePage):
    include_in_sitemap = models.BooleanField(
        default=True,
        help_text=_('Should this page appear in the sitemap'))
    promote_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('Share Image'),
        help_text=_('1200x630 preferably'))
    keywords = TaggableManager(
        verbose_name=_('Keywords'))
    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel('seo_title', 'Title'),
                FieldPanel('search_description', 'Description'),
                FieldPanel('keywords', 'Keywords'),
                ImageChooserPanel('promote_image'),
            ],
            _('SEO configuration')),
        MultiFieldPanel(
            [
                FieldPanel('slug'),
                FieldPanel('include_in_sitemap'),
                FieldPanel('show_in_menus'),
            ],
            _('Site Configuration')),
    ]

    class Meta:
        abstract = True

    def get_sitemap_urls(self, request):
        if not self.include_in_sitemap:
            return []
        else:
            return super(Page, self).get_sitemap_urls(request)