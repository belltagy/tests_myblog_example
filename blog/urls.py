
from django.urls import path,include
from .views import HomeView,EntryDetial
app_name = 'blog'
urlpatterns = [
    path('',HomeView.as_view(),name='index'),
    path('<int:pk>/',EntryDetial.as_view(),name='entry_detial'),
]
