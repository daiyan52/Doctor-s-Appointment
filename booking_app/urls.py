from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view, name='home_view'),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("book-slot/", views.book_slot, name="book_slot"),
    path("add-center/", views.add_center, name="add_center"),
    path("success/", views.success_page, name="success_page"),
    path("search-centers/", views.search_centers, name="search_centers"),
    path("dosage-details/", views.dosage_details, name="dosage_details"),
    path('dashboard/', views.dashboard, name='dashboard'),

]

