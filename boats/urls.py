from django.urls import path, include


urlpatterns = [
    path('images/<image>', include('views.index')),
]
