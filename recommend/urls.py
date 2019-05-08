from django.urls import path
from . import views

app_name = 'recommend'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('map/<str:account>/', views.map_with_baidu, name='map'),
    path('map/<str:account>/<str:latitude>/<str:longitude>/', views.show_position, name='show_position'),
    # path('logout/', views.log_out, name='log_out'),
]