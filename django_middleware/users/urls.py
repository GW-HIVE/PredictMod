from django.urls import path

# from . import views

urlpatterns = [
    path("csrf/", views.get_csrf, name="api-csrf"),
    path("create-user/", views.create_user_view, name="create-user"),
    path("login/", views.login_view, name="api-login"),
    path("logout/", views.logout_view, name="api-logout"),
    path("session/", views.session_view, name="api-session"),
    path("whoami/", views.whoami_view, name="api-whoami"),
]
