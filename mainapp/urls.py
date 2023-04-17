from django.urls import path
from . import views

urlpatterns = [
    path(''                , views.index          , name="index"),
    path('inicio/'         , views.index          , name="inicio"),
    path('register/'       , views.register_page  , name="register"),
    path('login/'          , views.login_page     , name="login"),
    path('logout/'         , views.logout_user    , name="logout"),
    path('register-action/', views.register_action, name="register_action"),
    path('login-action/'   , views.login_action   , name="login_action"),
]
