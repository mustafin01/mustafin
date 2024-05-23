from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_views),
    path('signup', register_views),
    path('logout', logout_view),
    path('claims', getApps),
    path('claim', creatApp),
    path('claim/<int:pk>', delete_app_view),
    path('admin/<int:pk>', redact_or_delete_app),
]