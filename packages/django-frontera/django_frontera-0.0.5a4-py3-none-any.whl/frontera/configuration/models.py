from django.core.validators import MinLengthValidator, MinValueValidator, \
    MaxValueValidator
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy

from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, \
  FieldPanel, PageChooserPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailschemaorg.models import BaseLDSetting
from wagtailschemaorg.registry import register_site_thing
from wagtailschemaorg.utils import extend


@register_setting(icon='form')
@register_site_thing
class OrganizationInfoSettings(BaseLDSetting):
    name = models.CharField(
        max_length=100,
        help_text=ugettext_lazy('Your organization\'s public name'),
        verbose_name=ugettext_lazy('Name'))
    phone_number = models.CharField(
        blank=True,
        max_length=20,
        help_text=ugettext_lazy('Public phone number'),
        verbose_name=ugettext_lazy('Phone number'))
    email = models.EmailField(
        blank=True,
        help_text=ugettext_lazy('Public contact email'),
        verbose_name=ugettext_lazy('Email'))
    twitter_handle = models.CharField(
        max_length=15,
        blank=True,
        help_text=ugettext_lazy('Without the @'),
        verbose_name=ugettext_lazy('Twitter handle'))

    facebook_url = models.URLField(
        blank=True,
        help_text=ugettext_lazy('Page\'s url in facebook'),
        verbose_name=ugettext_lazy('Facebook'))
    twitter_url = models.URLField(
        blank=True,
        help_text=ugettext_lazy('Page\'s url in twitter'),
        verbose_name=ugettext_lazy('Twitter'))
    instagram_url = models.URLField(
        blank=True,
        help_text=ugettext_lazy('Page\'s url in instagram'),
        verbose_name=ugettext_lazy('Instagram'))
    linkedin_url = models.URLField(
        blank=True,
        help_text=ugettext_lazy('Page\'s url in linkedin'),
        verbose_name=ugettext_lazy('LinkedIn'))
    youtube_url = models.URLField(
        blank=True,
        help_text=ugettext_lazy('Page\'s url in youtube'),
        verbose_name=ugettext_lazy('Youtube'))
    vimeo_url = models.URLField(
        blank=True,
        help_text=ugettext_lazy('Page\'s url in vimeo'),
        verbose_name=ugettext_lazy('Vimeo'))
    googleplus_url = models.URLField(
        blank=True,
        help_text=ugettext_lazy('Page\'s url in google plus'),
        verbose_name=ugettext_lazy('Google Plus'))
    
    organization_tab_panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('phone_number'),
            FieldPanel('email'),
            FieldPanel('twitter_handle'),
        ], heading=ugettext_lazy('General Information')),
    ]

    social_tab_panels = [
        MultiFieldPanel([
            FieldPanel('instagram_url'),
            FieldPanel('linkedin_url'),
            FieldPanel('twitter_url'),
            FieldPanel('facebook_url'),
            FieldPanel('youtube_url'),
            FieldPanel('vimeo_url'),
            FieldPanel('googleplus_url'),
        ], heading=ugettext_lazy('URLs')),
    ]

    edit_handler = TabbedInterface([
        ObjectList(organization_tab_panels, heading=ugettext_lazy('General Information')),
        ObjectList(social_tab_panels, heading=ugettext_lazy('Social Links')),
    ])

    class Meta:
        verbose_name = ugettext_lazy('Organization')
        verbose_name_plural = ugettext_lazy('Organization')

    def ld_generate_organization(self):
        customData = {
            '@type': 'Organization',
            'sameAs': [
                self.twitter_url,
                self.facebook_url,
            ],
        }
        sameAs = []
        if self.name: customData['name'] = self.name
        if self.email: customData['email'] = self.email
        if self.phone_number: customData['telephone'] = self.phone_number
        if self.twitter_url: sameAs.append(self.twitter_url)
        if self.facebook_url: sameAs.append(self.facebook_url)
        if self.instagram_url: sameAs.append(self.instagram_url)
        if self.linkedin_url: sameAs.append(self.linkedin_url)
        if self.youtube_url: sameAs.append(self.youtube_url)
        if self.vimeo_url: sameAs.append(self.vimeo_url)
        if self.googleplus_url: sameAs.append(self.googleplus_url)
        customData['sameAs'] = sameAs
        return customData

    # def ld_generate_website(self):
    #     customData = {
    #         '@type': 'WebSite',
    #     }
    #     return customData

    def ld_entity(self):
        organization = self.ld_generate_organization()
        # website = self.ld_generate_website()
        return extend(super().ld_entity(), organization)


@register_setting(icon='password')
class OtherSettings(BaseSetting):
    sentry_active = models.BooleanField(
        default=False,
        verbose_name=ugettext_lazy('Activate'))
    sentry_dsn = models.URLField(
        blank=True,
        help_text=ugettext_lazy('Get it from sentry.io'),
        verbose_name=ugettext_lazy('DSN for frontend error reporting'))
    google_recaptcha_public = models.CharField(
        blank=False,
        max_length=255,
        verbose_name=ugettext_lazy('Recaptcha Public Key'))
    google_recaptcha_secret = models.CharField(
        blank=False,
        max_length=255,
        verbose_name=ugettext_lazy('Recaptcha Secret Key'))
    ssl_on = models.BooleanField(
        default=False,
        verbose_name=ugettext_lazy('Is SSL active?'))

    CRITERIA_TIME = 'Express'
    CRITERIA_PRICE = 'Normal'
    CRITERIA_CHOICES = (
        (CRITERIA_TIME, ugettext_lazy('Express')),
        (CRITERIA_PRICE, ugettext_lazy('Normal')),
    )
    sending_criteria = models.CharField(
        blank=False,
        max_length=14,
        default=CRITERIA_PRICE,
        choices=CRITERIA_CHOICES,
        verbose_name=ugettext_lazy('Preference'))

    apis_tab_panels = [
        MultiFieldPanel([
            FieldPanel('sending_criteria'),
        ], heading=ugettext_lazy('Sending Criteria')),
        MultiFieldPanel([
            FieldPanel('ssl_on'),
        ], heading=ugettext_lazy('Site')),
        MultiFieldPanel([
            FieldPanel('google_recaptcha_public'),
            FieldPanel('google_recaptcha_secret'),
        ], heading=ugettext_lazy('Recaptcha')),
        MultiFieldPanel([
            FieldPanel('sentry_active'),
            FieldPanel('sentry_dsn'),
        ], heading='Sentry'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(apis_tab_panels, heading=ugettext_lazy('Security')),
    ])

    class Meta:
        verbose_name = ugettext_lazy('Security')
        verbose_name_plural = ugettext_lazy('Security')


@register_setting(icon='warning')
class AnalyticsSettings(BaseSetting):
    facebook_pixel = models.CharField(
        blank=True,
        max_length=70,
        verbose_name=ugettext_lazy('Pixel ID'))
    facebook_account = models.CharField(
        blank=True,
        max_length=70,
        verbose_name=ugettext_lazy('Account ID'))
    facebook_app = models.CharField(
        blank=True,
        max_length=70,
        verbose_name=ugettext_lazy('App ID'))
    google_analytics_enabled = models.BooleanField(
        default=False,
        blank=True,
        verbose_name=ugettext_lazy('Analytics enabled'))
    google_analytics_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=ugettext_lazy('Analytics ID'))
    google_adwords_enabled = models.BooleanField(
        default=False,
        blank=True,
        verbose_name=ugettext_lazy('Adwords enabled'))
    google_adwords_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=ugettext_lazy('Adwords ID'))
    google_tagmanager_enabled = models.BooleanField(
        default=False,
        blank=True,
        verbose_name=ugettext_lazy('Tagmanager enabled'))
    google_tagmanager_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=ugettext_lazy('TagManager ID'))
    google_site_verification = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=ugettext_lazy('Site Verification Key'))
    
    default_title = models.CharField(
        blank=False,
        max_length=300,
        verbose_name=ugettext_lazy('Title'))
    title_suffix = models.CharField(
        blank=False,
        default='Wuafbox',
        max_length=40,
        help_text=ugettext_lazy('For SEO the pages will appear in this manner: Title | Suffix'),
        verbose_name=ugettext_lazy('Title Suffix'))
    default_description = models.CharField(
        blank=False,
        max_length=255,
        verbose_name=ugettext_lazy('Description'))
    default_promote_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=ugettext_lazy('Share Image'),
        help_text=ugettext_lazy(
            'Image used by default for the SEO metas. 1200x630 preferably'
        ))
    default_language = models.CharField(
        default='es',
        choices=(
            ('es', 'Spanish'),
            ('en', 'English'),
        ),
        max_length=6,
        verbose_name=ugettext_lazy('Language'))

    other_tab_panels = [
        MultiFieldPanel([
            FieldPanel('title_suffix'),
            FieldPanel('default_title'),
            FieldPanel('default_description'),
            ImageChooserPanel('default_promote_image'),
            FieldPanel('default_language'),
        ], heading=ugettext_lazy('SEO Defaults')),
    ]
    keys_panels = [
        MultiFieldPanel([
            FieldPanel('google_analytics_id'),
            FieldPanel('google_analytics_enabled'),
            FieldPanel('google_tagmanager_id'),
            FieldPanel('google_tagmanager_enabled'),
            FieldPanel('google_adwords_id'),
            FieldPanel('google_adwords_enabled'),
            FieldPanel('google_site_verification'),
        ], heading=ugettext_lazy('Google')),
        MultiFieldPanel([
            FieldPanel('facebook_pixel'),
            FieldPanel('facebook_account'),
            FieldPanel('facebook_app'),
        ], heading=ugettext_lazy('Facebook'))
    ]

    edit_handler = TabbedInterface([
        ObjectList(other_tab_panels, heading=ugettext_lazy('Defaults')),
        ObjectList(keys_panels, heading=ugettext_lazy('APIs')),
    ])

    class Meta:
        verbose_name = ugettext_lazy('SEO')
        verbose_name_plural = ugettext_lazy('SEO')


