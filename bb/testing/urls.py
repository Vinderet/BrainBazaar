from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('tests/<int:test_id>/', views.test, name='test'),
    path('marks/', views.marks, name='marks'),
    path('tests_management/', views.test_management, name='test_management'),
    path('tests/<int:test_id>/add_question/', views.add_question, name='add_question'),
    path('questions/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('questions/<int:question_id>/answers/add/', views.add_answer, name='add_answer'),
    path('answers/<int:answer_id>/delete/', views.delete_answer, name='delete_answer'),
    path('answers/<int:answer_id>/edit/', views.edit_answer, name='edit_answer'),
]