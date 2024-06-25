from django.shortcuts import render
from django.shortcuts import render
# use rest_framework, permissions, authentication, status, viewsets, filters, serializers, generics, mixins, decorators
# user jwt 
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from UserType.serializers import UserLoginSerializer,StudentSerializer,CustomUserSerializer,TeacherSerializer,FakultetSerializer,UquvBoshqarmasiSerializer
from UserType.models import CustomUser, Student, Teacher, UquvBoshqarmasi, Fakultet
from UserType.utilits import IsFakultet, IsStudent, IsTeacher, IsUquvBoshqarmasi, IsFakUquvBoshqarmasi,IsStudentFakultetUquvBoshqarmasi,IsStudentTeacherFakultetUquvBoshqarmasi,IsFakTeachUquv
from education.models import Group, Subject
from rest_framework import permissions
# raiser exception
from rest_framework.exceptions import APIException
from education.serializers import GroupSerializer, SubjectSerializer
def raise_exception(message):
    raise ValidationError(message)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
    def get_queryset(self):
        is_fakultet = IsFakultet()
        if is_fakultet.has_permission(self.request, self):
            return Group.objects.filter(fakultet__user=self.request.user)
        return Group.objects.all()
    # permissions
    def has_permission(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [IsStudentFakultetUquvBoshqarmasi]
        if self.action == 'create':
            return [permissions.IsAuthenticated,IsFakUquvBoshqarmasi]
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            return [permissions.IsAuthenticated, IsFakUquvBoshqarmasi]
        # extra actions
        return raise_exception('Permission denied')
    

    def get_permissions(self):
        return [permission() for permission in self.has_permission()]
    
    # drf_yasg for create group
    @swagger_auto_schema(
        operation_summary='Create group',
        operation_description='Create group',
        responses={
            201: openapi.Response('Group created', GroupSerializer),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsFakUquvBoshqarmasi]
    )
    def create(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'fakultet': request.data.get('fakultet'),
            'students': request.data.get('students'),
            'additional_students': request.data.get('additional_students'),
        }
        serializer = GroupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # drf_yasg for update group
    @swagger_auto_schema(
        operation_summary='Update group',
        operation_description='Update group',
        responses={
            200: openapi.Response('Group updated', GroupSerializer),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsFakUquvBoshqarmasi]
    )
    def update(self, request, *args, **kwargs):
        group = self.get_object()
        data = {
            'name': request.data.get('name'),
            'fakultet': request.data.get('fakultet'),
            'students': request.data.get('students'),
            'additional_students': request.data.get('additional_students'),
        }
        serializer = GroupSerializer(group, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # drf_yasg for delete group
    @swagger_auto_schema(
        operation_summary='Delete group',
        operation_description='Delete group',
        responses={
            204: 'Group deleted',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsFakUquvBoshqarmasi]
    )
    def destroy(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # drf_yasg for get group
    @swagger_auto_schema(
        operation_summary='Get group',
        operation_description='Get group',
        responses={
            200: openapi.Response('Group', GroupSerializer),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsStudentFakultetUquvBoshqarmasi]
    )
    def retrieve(self, request, *args, **kwargs):
        # faqat manashu fakultetga tegishli guruhlar chiqadi
        group = self.get_object()
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # drf_yasg for get all groups
    @swagger_auto_schema(
        operation_summary='Get all groups',
        operation_description='Get all groups',
        responses={
            200: openapi.Response('Groups', GroupSerializer(many=True)),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsStudentFakultetUquvBoshqarmasi]
    )
    def list(self, request, *args, **kwargs):
        # faqat manashu fakultetga tegishli guruhlar chiqadi
        groups = self.get_queryset()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # drf_yasg for get all groups
  


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    def get_queryset(self):
        is_fakultet = IsFakultet()
        if is_fakultet.has_permission(self.request, self):
            return Group.objects.filter(fakultet__user=self.request.user)
        return Group.objects.all()
    # permissions
    def has_permission(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [IsStudentTeacherFakultetUquvBoshqarmasi]
        if self.action == 'create':
            return [permissions.IsAuthenticated,IsFakTeachUquv]
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            return [permissions.IsAuthenticated, IsFakTeachUquv]
        # extra actions
        return raise_exception('Permission denied')
    
    def get_permissions(self):
        return [permission() for permission in self.has_permission()]
    
    # drf_yasg for create subject
    @swagger_auto_schema(
        operation_summary='Create subject',
        operation_description='Create subject',
        responses={
            201: openapi.Response('Subject created', SubjectSerializer),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsFakTeachUquv]
    )
    def create(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'fakultet': request.data.get('fakultet'),
            'teacher': request.data.get('teacher'),
            'group': request.data.get('group'),
        }
        serializer = SubjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # drf_yasg for update subject
    @swagger_auto_schema(
        operation_summary='Update subject',
        operation_description='Update subject',
        responses={
            200: openapi.Response('Subject updated', SubjectSerializer),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsFakTeachUquv]
    )
    def update(self, request, *args, **kwargs):
        subject = self.get_object()
        data = {
            'name': request.data.get('name'),
            'fakultet': request.data.get('fakultet'),
            'teacher': request.data.get('teacher'),
            'group': request.data.get('group'),
        }
        serializer = SubjectSerializer(subject, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # drf_yasg for delete subject
    @swagger_auto_schema(
        operation_summary='Delete subject',
        operation_description='Delete subject',
        responses={
            204: 'Subject deleted',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsFakTeachUquv]
    )
    def destroy(self, request, *args, **kwargs):
        subject = self.get_object()
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # drf_yasg for get subject
    @swagger_auto_schema(
        operation_summary='Get subject',
        operation_description='Get subject',
        responses={
            200: openapi.Response('Subject', SubjectSerializer),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsStudentTeacherFakultetUquvBoshqarmasi]
    )
    def retrieve(self, request, *args, **kwargs):
        # faqat manashu fakultetga tegishli fanlar chiqadi
        subject = self.get_object()
        serializer = SubjectSerializer(subject)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # drf_yasg for get all subjects

    @swagger_auto_schema(
        operation_summary='Get all subjects',
        operation_description='Get all subjects',
        responses={
            200: openapi.Response('Subjects', SubjectSerializer(many=True)),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsStudentTeacherFakultetUquvBoshqarmasi]
    )
    def list(self, request, *args, **kwargs):
        # faqat manashu fakultetga tegishli fanlar chiqadi
        subjects = self.get_queryset()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # partial update
    @swagger_auto_schema(
        operation_summary='Partial update subject',
        operation_description='Partial update subject',
        responses={
            200: openapi.Response('Subject updated', SubjectSerializer),
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsFakTeachUquv]
    )
    def partial_update(self, request, *args, **kwargs):
        subject = self.get_object()
        data = {
            'name': request.data.get('name'),
            'fakultet': request.data.get('fakultet'),
            'teacher': request.data.get('teacher'),
            'group': request.data.get('group'),
        }
        serializer = SubjectSerializer(subject, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # extra actions
    @swagger_auto_schema(
        operation_summary='Extra action',
        operation_description='Extra action',
        responses={
            200: 'Extra action',
            400: 'Bad request',
            401: 'Unauthorized',
            403: 'Permission denied',
        },
        permission_classes=[IsFakTeachUquv]
    )
    def extra_action(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)