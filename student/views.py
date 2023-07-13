from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from base.middleware import admin_required, student_required, admin_or_student_required
from django.db.models import Q
from .forms import StudentForm
from .models import Student
from .serializers import StudentSerializer
from django.contrib.auth.models import User
from django.http import HttpResponse

# @api_view(['GET'])
# def api_student_list(request):
#         if not admin_required(request):
#           return HttpResponse('Unauthorized', status=401)
#     if isinstance(request , HttpResponse):
#         return HttpResponse(request)

#     students = Student.objects.all()
#     if students:
#         serializer = StudentSerializer(students, many=True)
#         return Response(serializer.data)
#     return Response({'message': 'No students found'}, status=404)
# # api_view(admin_required(api_student_list))

@api_view(['GET'])
def api_student_list(request):
    if not admin_required(request):
        return HttpResponse('Unauthorized', status=401)
        
    students = Student.objects.all()
    if students:
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    return Response({'message': 'No students found'}, status=404)
# api_view(admin_required(api_student_list))

@api_view(['GET'])
def api_student_search(request):
    if not admin_required(request):
        return HttpResponse('Unauthorized', status=401)

    q = request.data.get('q') 
    if q:
        students = Student.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email_address__icontains=q) |
            Q(roll_number__icontains=q) |
            Q(contact_number__icontains=q)
        )
        if students:
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)
        return Response({'message': 'No students found'}, status=404)

@api_view(['GET'])
def api_student_detail(request, roll_number):
    request = admin_or_student_required(request)
    student = get_object_or_404(Student, roll_number=roll_number)
    serializer = StudentSerializer(student)
    return Response(serializer.data)

@api_view(['POST'])
def api_student_create(request):
    if not admin_required(request):
        return HttpResponse('Unauthorized', status=401)
    form = StudentForm(request.data)
    # password = request.data.get('password')
    if User.objects.filter(username=request.data.get('roll_number')).exists():
        return Response({'message': 'Username already exists'}, status=400)
    elif form.is_valid():
        student = form.save()
        user = User.objects.create_user(username=student.roll_number, password=student.roll_number, is_staff=False)
        user.save()
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=201)
    return Response(form.errors, status=400)

@api_view(['PUT'])
def api_student_update(request, roll_number):
    if not admin_required(request):
        return HttpResponse('Unauthorized', status=401)
    student = get_object_or_404(Student, roll_number=roll_number)
    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def api_student_delete(request, roll_number):
    if not admin_required(request):
        return HttpResponse('Unauthorized', status=401)
    student = get_object_or_404(Student, roll_number=roll_number)
    student.delete()
    return Response(status=204)
