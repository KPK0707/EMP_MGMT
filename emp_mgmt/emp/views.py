
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.pagination import PageNumberPagination


@authentication_classes(['IsAuthenticated'])
@api_view(['POST'])
def create_employee(request):

        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes(['IsAuthenticated'])
@api_view(['GET'])   
def get_employees(request):
        
        employees =Employee.objects.all()
        if employees:
            paginator=PageNumberPagination()
            paginator.page_size = 10
            paginated_employees=paginator.paginate_queryset(employees,request)
            serializer=EmployeeSerializer(paginated_employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message':'No employees found'},status=status.HTTP_404_NOT_FOUND)
    

@authentication_classes(['IsAuthenticated'])
@api_view(['GET','PUT','DELETE'])
def employee_info(request,pk):
    try:
        employee = Employee.objects.get(pk=pk)
        
    except Employee.DoesNotExist:
        return Response({'message': "Employee Not Found"},status=status.HTTP_404_NOT_FOUND)
    
    if request.method =='GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    if request.method =='PUT':
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    if request.method =='DELETE':
        employee.delete()
        return Response({'message':'Employee Deleted'},status= status.HTTP_204_NO_CONTENT)


        # Create your views here.
    
