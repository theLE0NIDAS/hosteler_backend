# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# from .models import Supervisor, Student

# User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user

# class SupervisorSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Supervisor
#         fields = ('user',)  # Add additional fields for supervisor if needed

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = User.objects.create_user(**user_data)
#         supervisor = Supervisor.objects.create(user=user, **validated_data)
#         return supervisor

# class StudentSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Student
#         fields = ('user',)  # Add additional fields for student if needed

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = User.objects.create_user(**user_data)
#         student = Student.objects.create(user=user, **validated_data)
#         return student
