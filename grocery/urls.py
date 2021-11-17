from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("update/<int:id>", views.update, name="update"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("login", views.login_page, name="login"),
    path("logout", views.log_out, name="logout"),
    path("register", views.register_page, name="register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
