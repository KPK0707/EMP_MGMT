from django.urls import path
from . import views

urlpatterns= [
    path('create_employee/',views.create_employee,name='new_employee'),
    path('get_employee/',views.get_employees,name='employees_list'),
    path('employee_info/<str:pk>/', views.employee_info,name='employee_details'),

]