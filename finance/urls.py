from django.urls import path
from . import views

urlpatterns = [

    # Dashboard
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # Add
    path(
        'add-earning/',
        views.add_earning,
        name='add_earning'
    ),

    path(
        'add-expense/',
        views.add_expense,
        name='add_expense'
    ),

    # View
    path(
        'earning/view/<int:id>/',
        views.view_earning,
        name='view_earning'
    ),

    path(
        'expense/view/<int:id>/',
        views.view_expense,
        name='view_expense'
    ),

    # Edit
    path(
        'earning/edit/<int:id>/',
        views.edit_earning,
        name='edit_earning'
    ),

    path(
        'expense/edit/<int:id>/',
        views.edit_expense,
        name='edit_expense'
    ),

    # Delete
    path(
        'earning/delete/<int:id>/',
        views.delete_earning,
        name='delete_earning'
    ),

    path(
        'expense/delete/<int:id>/',
        views.delete_expense,
        name='delete_expense'
    ),

    path(
    'edit-salary/',
    views.edit_salary,
    name='edit_salary'
),
]