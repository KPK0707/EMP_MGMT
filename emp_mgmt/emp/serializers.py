

from rest_framework import serializers

from .models import Employee
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

import re


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields= ('id','name','email','department','roles','date_joined')

    def validate_name(self,value):

        # Check if the name is empty or contains only empty spaces

        name_regex=r'^[A-Za-z]+(\.?[A-Za-z]+)*$'

        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty or white space only")
        
        # Regular Expression: Allows alphabetic characters, spaces, and single periods
        # Prevents sequences of multiple dots or a name consisiting only of dots.
        if not re.match(name_regex, value.replace(" ", "")):
            raise serializers.ValidationError(
                "Name must contain only alphabetic characters, spaces, and single periods between names."
            )

        return value


    def validate_email(self,value):


        
        valid_domains = {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com", "example.com"}
        domain = value.split("@")[-1]

        if domain not in valid_domains:
            raise serializers.ValidationError('The Domain is not a valid domain')
        
        if not value:
            raise serializers.ValidationError("Email cannot be empty")
        

        
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists")
        
        try:
            validate_email(value)
        
        except DjangoValidationError as e:
            raise serializers.ValidationError ("enter a valid email address")
        
        # email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        # if not re.match(email_regex, value):
        #     raise serializers.ValidationError("Enter a valid email address")
        
        return value
    

    def create(self, validated_data):

        # emp= Employee.objects.create(
        #     name=self.validated_data['name'],
        #     email=self.validated_data['email'],
        #     department=self.validated_data['department'],
        #     roles = self.validated_data['roles'],
        #     date_joined = self.validated_data['date_joined']
        # )
        # emp.save()
        emp = Employee.objects.create(**validated_data)
        emp.save()
        return emp
    
    def update(self, instance, data):
        print(data)
        employee=Employee.objects.get(id=instance.id)
        employee.name=data.get('name', employee.name)
        employee.email=data.get('email', employee.email)
        employee.department=data.get('department', employee.department)
        
        employee.save()

        return employee



        

