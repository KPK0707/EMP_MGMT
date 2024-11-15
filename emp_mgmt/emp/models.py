from django.db import models
from django.contrib.auth.models import User

DEPARTMENT=[
    ('HR', 'Human Resources'),
    ('Finance', 'Finance'),
    ('Marketing', 'Marketing'),
    ('IT', 'Information Technology'),
    ('Sales', 'Sales'),
    ('Operations', 'Operations'),
    ('Admin', 'Admin')
]

ROLES = [
    ('Manager','Manager'),
    ('Developer','Developer'),
    ('Tester','Tester'),
    ('Project Manager','Project Manager'),
    ('Team Lead','Team Lead'),
    ('Designer','Designer'),
]
class Employee(models.Model):

    name=models.CharField(max_length=100, null=False)
    email=models.EmailField(max_length=100, null=False, unique=True)
    department=models.CharField(max_length=100, choices=DEPARTMENT)
    roles=models.CharField(max_length=100,choices=ROLES)
    date_joined=models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering =['id']

# Create your models here.
