from django.urls import path
from .views import home_view, setting_view, profile_view, follow, like

urlpatterns = [
    path('', home_view),
    path('follow/', follow),
    path('like/', like),
    path('setting/', setting_view),
    path('profile/', profile_view),
]
