# emp/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Employee
from django.contrib.auth.models import User

class EmployeeAPITests(APITestCase):

    def setUp(self):
        # Create a user and obtain JWT tokens
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        # Define the employee data
        self.employee_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'department': 'IT',
            'roles': 'Developer'
        }

    def test_create_employee(self):
        # Test creating an employee
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(reverse('new_employee'), self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, 'John Doe')

    def test_get_employees(self):
        # Test getting a list of employees
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        Employee.objects.create(**self.employee_data)  # Create an employee
        response = self.client.get(reverse('employees_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_employee_info(self):
        # Test getting, updating, and deleting employee info
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        employee = Employee.objects.create(**self.employee_data)
        url = reverse('employee_details', kwargs={'pk': employee.id})

        # Test GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')

        # Test PUT
        updated_data = {'name': 'Jane Doe'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.get().name, 'Jane Doe')

        # Test DELETE
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

# Note: Make sure to run your tests with the command below:
# python manage.py test emp
