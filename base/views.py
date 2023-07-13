from django.contrib.auth.models import User
from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.middleware import admin_required, student_required, admin_or_student_required
from django.shortcuts import get_object_or_404
# from django.contrib.auth import login, logout, authenticate
import jwt
from datetime import datetime , timedelta , timezone

@api_view(['POST'])
def api_admin_create(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'message': 'Username already exists'}, status=400)
    else:
        user = User.objects.create_user(username=username, password=password, is_staff=True)
        user.save()
        return Response({'message': 'Admin created successfully'}, status=201)

@api_view(['PUT'])
def api_admin_update_password(request, username):
    if not admin_required(request):
        return HttpResponse('Unauthorized', status=401)
    user = get_object_or_404(User, username=username)
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password updated successfully'})
    return Response({'message': 'Invalid credentials'}, status=400)

@api_view(['PUT'])
def api_student_update_password(request, roll_number):
    if not student_required(request):
        return HttpResponse('Unauthorized', status=401)
    student = get_object_or_404(Student, roll_number=roll_number)
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if student.user.check_password(old_password):
        student.user.set_password(new_password)
        student.user.save()
        return Response({'message': 'Password updated successfully'})
    return Response({'message': 'Invalid credentials'}, status=400)

####################################################################################
#Login/Logout Api's
####################################################################################

@api_view(['POST'])
def api_admin_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = get_object_or_404(User, username=username, is_staff=True)
    if user.check_password(password):
        # user = authenticate(request, username=username, password=password)
        # login(request, user)
        token = jwt.encode({'username': username, 'is_staff':user.is_staff , "exp": datetime.now(tz=timezone.utc) + timedelta(weeks=1)}, 'secret', algorithm='HS256')
        return Response({'message': 'Admin logged in successfully', 'token': token}, status=200)
    return Response({'message': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def api_student_login(request):
    roll_number = request.data.get('roll_number')
    password = request.data.get('password') 
    user = get_object_or_404(User, username=roll_number, is_staff=False)
    if user.check_password(password):
        # login(request, user)
        token = jwt.encode({'username': roll_number, 'is_staff':user.is_staff , "exp": datetime.now(tz=timezone.utc) + timedelta(weeks=1)}, 'secret', algorithm='HS256')
        return Response({'message': 'Student logged in successfully', 'token': token}, status=200)
    return Response({'message': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def api_logout(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})