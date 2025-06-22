from django.urls import path, include
from django.contrib import admin
from flashcard_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('flashcard_app.urls')),

]