
class ReviewSettings(object):

    @property
    def STYLESHEETS(self):
        return super().STYLESHEETS + (
            'jquery.rateit/rateit.css',
        )

    @property
    def JAVASCRIPT(self):
        return super().JAVASCRIPT + (
            'reviews/reviews.js',
            'jquery.rateit/jquery.rateit.js',
            'jquery.form.js',
        )

    @property
    def INSTALLED_APPS(self):
        apps = super().INSTALLED_APPS + [
            'reviews'
        ]

        if not 'captcha' in apps:
            apps += ['captcha']

        return apps
