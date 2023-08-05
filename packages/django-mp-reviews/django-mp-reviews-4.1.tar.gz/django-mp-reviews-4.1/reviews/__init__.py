
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ReviewsConfig(AppConfig):
    name = 'reviews'
    verbose_name = _("Reviews")


default_app_config = 'reviews.ReviewsConfig'
