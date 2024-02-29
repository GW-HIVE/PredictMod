from django.urls import path, include


from . import views

import logging

logger = logging.getLogger()


# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r"", UserViewSet)
# router.register(r"login", views.login_view)
# router.register(r"whoami", views.whoami_view)

urlpatterns = [
    # path("api/users/", include(router.urls)),
    path("api/users/", views.UserListView.as_view()),
    path("api/create-user/", views.CreateUser.as_view()),
    path("api/update-user/", views.UpdateUser.as_view()),
    path("api/delete-user/", views.DeleteUser.as_view()),
    path("api/login/", views.login_view),
    path("api/logout/", views.logout_view),
    path("api/whoami/", views.whoami_view),
    # path("api/csrf/", views.get_csrf),
    # path("api/session/", views.session_view),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
