
from django.urls import path

from reviews import views


app_name = 'reviews'


urlpatterns = [

    path('', views.ReviewListView.as_view(), name='list'),

    path('api/', views.ReviewAPI.as_view(), name='api')

]

app_urls = i18n_patterns(

    path('reviews/', include((urlpatterns, app_name)))

)
