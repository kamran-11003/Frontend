
from django.contrib import admin
from django.urls import path
from Main import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('Demo', views.home, name='home'),
    path('', views.index, name='index'),
    path('takeCommand/', views.takeCommand, name='takeCommand'),
    path('say/', views.say, name='say'),
    path('update_feedback/', views.update_feedback, name='update_feedback'),

]
