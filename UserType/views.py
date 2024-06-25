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
def raise_exception(message):
    raise ValidationError(message)

def index(request):
    return render(request, 'index.html')


class UserLoginView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={200: openapi.Response('Successfully logged in', TokenObtainPairSerializer)}
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        user_type = CustomUser.objects.get(username=serializer.validated_data['username']).user_type

        if user is None:
            raise NotAuthenticated('Invalid username or password')
        refresh = RefreshToken.for_user(user)
        userype = 'student' if user_type == 1 else 'teacher' if user_type == 2 else 'fakultet' if user_type == 3 else 'uquv boshqarmasi'
        refresh['user_type'] = userype
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })



class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def has_permission(self):
        print(self.action)
        if self.action == 'create':
            return [IsFakUquvBoshqarmasi]
        elif self.action == 'update':
            return [IsStudentFakultetUquvBoshqarmasi]
        elif self.action == 'destroy':
            return [IsFakUquvBoshqarmasi]
        elif self.action == 'list':
            return [IsStudentTeacherFakultetUquvBoshqarmasi]
        elif self.action == 'retrieve':
            return [IsStudentFakultetUquvBoshqarmasi]
        elif self.action == 'partial_update':
            return [IsStudentFakultetUquvBoshqarmasi]
        return raise_exception('Permission denied')
    
    def get_permissions(self):
        return [permission() for permission in self.has_permission()]
    
    @swagger_auto_schema(
        operation_summary="List all students",
        operation_description="Lists all student instances",
        responses={
            200: openapi.Response("List of students", StudentSerializer(many=True)),
        },
        permission_classes=[IsStudentTeacherFakultetUquvBoshqarmasi],
    )
    def list(self, request, *args, **kwargs):
        # is_archived = request.query_params.get('is_archived', False)
        queryset = self.queryset.filter(is_archive=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="Create a student",
        operation_description="Create a student instance",
        request_body=StudentSerializer,
        responses={
            201: openapi.Response("Student created", StudentSerializer),
        },
        permission_classes=[IsFakUquvBoshqarmasi],
    )
    def create(self, request, *args, **kwargs):
        try:
            user_data = {
                'username': request.data.get('username'),
                'password': request.data.get('password'),
                'passwordinfo': request.data.get('password'),
                'user_type': 1,
                'is_active': True,
            }
            user_serializer = CustomUserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            student_data = {
                'name': request.data.get('name'),
                'surname': request.data.get('surname'),
                'age': request.data.get('age'),
                'phone': request.data.get('phone'),
                'studentid': request.data.get('studentid'),
                'address': request.data.get('address'),
                'user': user.pk,
            }
            student_serializer = self.get_serializer(data=student_data)
            student_serializer.is_valid(raise_exception=True)
            self.perform_create(student_serializer)
            return Response(student_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # delete user if student creation fails
            user.delete()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        serializer.save()

    @swagger_auto_schema(
        operation_summary="Update a student",
        operation_description="Update a student instance",
        request_body=StudentSerializer,
        responses={
            200: openapi.Response("Student updated", StudentSerializer),
        },
        permission_classes=[IsStudentFakultetUquvBoshqarmasi],
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'passwordinfo': request.data.get('password'),
            'user_type': 1,
            'is_active': True,
        }
        user_serializer = CustomUserSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        student_data = {
            'name': request.data.get('name'),
            'surname': request.data.get('surname'),
            'age': request.data.get('age'),
            'phone': request.data.get('phone'),
            'studentid': request.data.get('studentid'),
            'address': request.data.get('address'),
            'user': user.pk,
        }
        student_serializer = self.get_serializer(instance, data=student_data)
        student_serializer.is_valid(raise_exception=True)
        self.perform_update(student_serializer)
        return Response(student_serializer.data, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        serializer.save()

    @swagger_auto_schema(
        operation_summary="Delete a student",
        operation_description="Delete a student instance",
        responses={
            204: openapi.Response("Student deleted", None),
        },
        permission_classes=[IsFakUquvBoshqarmasi],
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archived = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        operation_summary="Retrieve a student",
        operation_description="Retrieve a student instance",
        responses={
            200: openapi.Response("Student retrieved", StudentSerializer),
        },
        permission_classes=[IsStudentFakultetUquvBoshqarmasi],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="Partial update a student",
        operation_description="Partial update a student instance",
        request_body=StudentSerializer,
        responses={
            200: openapi.Response("Student updated", StudentSerializer),
        },
        permission_classes=[IsStudentFakultetUquvBoshqarmasi],
    )
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user_data = {
            'username': request.data.get('username', user.username),
            'password': request.data.get('password', user.password),
            'passwordinfo': request.data.get('password', user.password),
            'user_type': 1,
            'is_active': True,
        }
        user_serializer = CustomUserSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        student_data = {
            'name': request.data.get('name', instance.name),
            'surname': request.data.get('surname', instance.surname),
            'age': request.data.get('age', instance.age),
            'phone': request.data.get('phone', instance.phone),
            'studentid': request.data.get('studentid', instance.studentid),
            'address': request.data.get('address', instance.address),
            'user': user.pk,
        }
        student_serializer = self.get_serializer(instance, data=student_data)
        student_serializer.is_valid(raise_exception=True)
        self.perform_update(student_serializer)
        return Response(student_serializer.data, status=status.HTTP_200_OK)
    
    
    
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    
    def has_permission(self):
        print(self.action)
        if self.action == 'create':
            return [IsFakUquvBoshqarmasi]
        elif self.action == 'update':
            return [IsFakTeachUquv]
        elif self.action == 'destroy':
            return [IsFakUquvBoshqarmasi]
        elif self.action == 'list':
            return [IsStudentTeacherFakultetUquvBoshqarmasi]
        elif self.action == 'retrieve':
            return [IsFakTeachUquv]
        elif self.action == 'partial_update':
            return [IsFakTeachUquv]
        return raise_exception('Permission denied')
    
    def get_permissions(self):
        return [permission() for permission in self.has_permission()]
    
    @swagger_auto_schema(
        operation_summary="List all teachers",
        operation_description="Lists all teacher instances",
        responses={
            200: openapi.Response("List of teachers", TeacherSerializer(many=True)),
        },
        permission_classes=[IsStudentTeacherFakultetUquvBoshqarmasi],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_archive=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="Create a teacher",
        operation_description="Create a teacher instance",
        request_body=TeacherSerializer,
        responses={
            201: openapi.Response("Teacher created", TeacherSerializer),
        },
        permission_classes=[IsFakUquvBoshqarmasi],
    )
    def create(self, request, *args, **kwargs):
        try:
            user_data = {
                'username': request.data.get('username'),
                'password': request.data.get('password'),
                'passwordinfo': request.data.get('password'),
                'user_type': 2,
                'is_active': True,
            }
            user_serializer = CustomUserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            teacher_data = {
                'name': request.data.get('name'),
                'surname': request.data.get('surname'),
                'age': request.data.get('age'),
                'phone': request.data.get('phone'),
                'teacherid': request.data.get('teacherid'),
                'address': request.data.get('address'),
                'user': user.pk,
            }
            teacher_serializer = self.get_serializer(data=teacher_data)
            teacher_serializer.is_valid(raise_exception=True)
            self.perform_create(teacher_serializer)
            return Response(teacher_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # delete user if teacher creation fails
            user.delete()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
    @swagger_auto_schema(
        operation_summary='Update Teacher',
        operation_description='Update Teacher instance',
        request_body=TeacherSerializer,
        responses={
            200: openapi.Response('Teacher updated', TeacherSerializer),
        },
        permission_classes=[IsFakTeachUquv],
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'passwordinfo': request.data.get('password'),
            'user_type': 2,
            'is_active': True,
        }
        user_serializer = CustomUserSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        teacher_data = {
            'name': request.data.get('name'),
            'surname': request.data.get('surname'),
            'age': request.data.get('age'),
            'phone': request.data.get('phone'),
            'teacherid': request.data.get('teacherid'),
            'address': request.data.get('address'),
            'user': user.pk,
        }
        teacher_serializer = self.get_serializer(instance, data=teacher_data)
        teacher_serializer.is_valid(raise_exception=True)
        self.perform_update(teacher_serializer)
        return Response(teacher_serializer.data, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        serializer.save()

    @swagger_auto_schema(
        operation_summary='Delete Teacher',
        operation_description='Delete Teacher instance',
        responses={
            204: openapi.Response('Teacher deleted', None),
        },
        permission_classes=[IsFakUquvBoshqarmasi],
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archive = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        operation_summary='Retrieve Teacher',
        operation_description='Retrieve Teacher instance',
        responses={
            200: openapi.Response('Teacher retrieved', TeacherSerializer),
        },
        permission_classes=[IsFakTeachUquv],
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary='Partial update Teacher',
        operation_description='Partial update Teacher instance',
        request_body=TeacherSerializer,
        responses={
            200: openapi.Response('Teacher updated', TeacherSerializer),
        },
        permission_classes=[IsFakTeachUquv],
    )
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user_data = {
            'username': request.data.get('username', user.username),
            'password': request.data.get('password', user.password),
            'passwordinfo': request.data.get('password', user.password),
            'user_type': 2,
            'is_active': True,
        }
        user_serializer = CustomUserSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        teacher_data = {
            'name': request.data.get('name', instance.name),
            'surname': request.data.get('surname', instance.surname),
            'age': request.data.get('age', instance.age),
            'phone': request.data.get('phone', instance.phone),
            'teacherid': request.data.get('teacherid', instance.teacherid),
            'address': request.data.get('address', instance.address),
            'user': user.pk,
        }
        teacher_serializer = self.get_serializer(instance, data=teacher_data)
        teacher_serializer.is_valid(raise_exception=True)
        self.perform_update(teacher_serializer)
        return Response(teacher_serializer.data, status=status.HTTP_200_OK)
    
class FakultetViewSet(viewsets.ModelViewSet):
    queryset = Fakultet.objects.all()
    serializer_class = FakultetSerializer
    
    def has_permission(self):
        print(self.action)
        if self.action == 'create':
            return [IsUquvBoshqarmasi]
        elif self.action == 'update':
            return [IsFakUquvBoshqarmasi]
        elif self.action == 'destroy':
            return [IsUquvBoshqarmasi]
        elif self.action == 'list':
            return [IsStudentTeacherFakultetUquvBoshqarmasi]
        elif self.action == 'retrieve':
            return [IsFakUquvBoshqarmasi]
        elif self.action == 'partial_update':
            return [IsFakTeachUquv]
        return raise_exception('Permission denied')
    
    def get_permissions(self):
        return [permission() for permission in self.has_permission()]
    
    @swagger_auto_schema(
        operation_summary="List all fakultets",
        operation_description="Lists all fakultet instances",
        responses={
            200: openapi.Response("List of fakultets", FakultetSerializer(many=True)),
        },
        permission_classes=[IsStudentTeacherFakultetUquvBoshqarmasi],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(is_archive=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="Create a fakultet",
        operation_description="Create a fakultet instance",
        request_body=FakultetSerializer,
        responses={
            201: openapi.Response("Fakultet created", FakultetSerializer),
        },
        permission_classes=[IsUquvBoshqarmasi],
    )
    def create(self, request, *args, **kwargs):
        # user_data = {
        #     'username': request.data.get('username'),
        #     'password': request.data.get('password'),
        #     'passwordinfo': request.data.get('password'),
        #     'user_type': 3,
        #     'is_active': True,
        # }
        # user_serializer = CustomUserSerializer(data=user_data)
        # user_serializer.is_valid(raise_exception=True)
        # user = user_serializer.save()
        # fakultet_data = {
        #     'name': request.data.get('name'),
        #     'fakultetid': request.data.get('fakultetid'),
        #     'user': user.pk,
        # }
        # fakultet_serializer = self.get_serializer(data=fakultet_data)
        # fakultet_serializer.is_valid(raise_exception=True)
        # self.perform_create(fakultet_serializer)
        # return Response(fakultet_serializer.data, status=status.HTTP_201_CREATED)
        try:
            user_data = {
                'username': request.data.get('username'),
                'password': request.data.get('password'),
                'passwordinfo': request.data.get('password'),
                'user_type': 3,
                'is_active': True,
            }
            user_serializer = CustomUserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            fakultet_data = {
                'name': request.data.get('name'),
                'fakultetid': request.data.get('fakultetid'),
                'user': user.pk,
            }
            fakultet_serializer = self.get_serializer(data=fakultet_data)
            fakultet_serializer.is_valid(raise_exception=True)
            self.perform_create(fakultet_serializer)
            return Response(fakultet_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # delete user if fakultet creation fails
            user.delete()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        serializer.save()

    @swagger_auto_schema(
        operation_summary='Update Fakultet',
        operation_description='Update Fakultet instance',
        request_body=FakultetSerializer,
        responses={
            200: openapi.Response('Fakultet updated', FakultetSerializer),
        },
        permission_classes=[IsFakUquvBoshqarmasi],
    )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'passwordinfo': request.data.get('password'),
            'user_type': 3,
            'is_active': True,
        }
        user_serializer = CustomUserSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        fakultet_data = {
            'name': request.data.get('name'),
            'fakultetid': request.data.get('fakultetid'),
            'user': user.pk,
        }
        fakultet_serializer = self.get_serializer(instance, data=fakultet_data)
        fakultet_serializer.is_valid(raise_exception=True)
        self.perform_update(fakultet_serializer)
        return Response(fakultet_serializer.data, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        serializer.save()

    @swagger_auto_schema(
        operation_summary='Delete Fakultet',
        operation_description='Delete Fakultet instance',
        responses={
            204: openapi.Response('Fakultet deleted', None),
        },
        permission_classes=[IsUquvBoshqarmasi],
    )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_archive = True
        instance.save()
        return Response(
            data={
                'message': 'Fakultet deleted successfully'

            },
            status=status.HTTP_204_NO_CONTENT
        )
    
    @swagger_auto_schema(
        operation_summary='Retrieve Fakultet',
        operation_description='Retrieve Fakultet instance',
        responses={
            200: openapi.Response('Fakultet retrieved', FakultetSerializer),
        },
        permission_classes=[IsFakUquvBoshqarmasi],
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary='Partial update Fakultet',
        operation_description='Partial update Fakultet instance',
        request_body=FakultetSerializer,
        responses={
            200: openapi.Response('Fakultet updated', FakultetSerializer),
        },
        permission_classes=[IsFakUquvBoshqarmasi],
    )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user_data = {
            'username': request.data.get('username', user.username),
            'password': request.data.get('password', user.password),
            'passwordinfo': request.data.get('password', user.password),
            'user_type': 3,
            'is_active': True,
        }
        user_serializer = CustomUserSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        fakultet_data = {
            'name': request.data.get('name', instance.name),
            'fakultetid': request.data.get('fakultetid', instance.fakultetid),
            'user': user.pk,
        }
        fakultet_serializer = self.get_serializer(instance, data=fakultet_data)
        fakultet_serializer.is_valid(raise_exception=True)
        self.perform_update(fakultet_serializer)
        return Response(fakultet_serializer.data, status=status.HTTP_200_OK)

# uquvbo'limi faqat update va partial update qilish  va retrieve qilish mumkin

class UquvBoshqarmasiViewSet(viewsets.ModelViewSet):
    queryset = UquvBoshqarmasi.objects.all()
    serializer_class = UquvBoshqarmasiSerializer
    
    def has_permission(self):
        print(self.action)
        
        if self.action == 'update':
            return [IsUquvBoshqarmasi]
        
        elif self.action == 'retrieve':
            return [IsUquvBoshqarmasi]
        elif self.action == 'partial_update':
            return [IsUquvBoshqarmasi]
        return raise_exception('Permission denied')
    
    def get_permissions(self):
        return [permission() for permission in self.has_permission()]
    
    # update uquv boshqarmasi
    @swagger_auto_schema(
        operation_summary='Update UquvBoshqarmasi',
        operation_description='Update UquvBoshqarmasi instance',
        request_body=UquvBoshqarmasiSerializer,
        responses={
            200: openapi.Response('UquvBoshqarmasi updated', UquvBoshqarmasiSerializer),
        },
        permission_classes=[IsUquvBoshqarmasi],
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'passwordinfo': request.data.get('password'),
            'user_type': 4,
            'is_active': True,
        }
        user_serializer = CustomUserSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        uquvboshqarmasi_data = {
            'name': request.data.get('name'),
            'user': user.pk,
        }
        uquvboshqarmasi_serializer = self.get_serializer(instance, data=uquvboshqarmasi_data)
        uquvboshqarmasi_serializer.is_valid(raise_exception=True)
        self.perform_update(uquvboshqarmasi_serializer)
        return Response(uquvboshqarmasi_serializer.data, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        serializer.save()

    # retrieve uquv boshqarmasi
    @swagger_auto_schema(
        operation_summary='Retrieve UquvBoshqarmasi',
        operation_description='Retrieve UquvBoshqarmasi instance',
        responses={
            200: openapi.Response('UquvBoshqarmasi retrieved', UquvBoshqarmasiSerializer),
        },
        permission_classes=[IsUquvBoshqarmasi],
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # partial update uquv boshqarmasi
    @swagger_auto_schema(
        operation_summary='Partial update UquvBoshqarmasi',
        operation_description='Partial update UquvBoshqarmasi instance',
        request_body=UquvBoshqarmasiSerializer,
        responses={
            200: openapi.Response('UquvBoshqarmasi updated', UquvBoshqarmasiSerializer),
        },
        permission_classes=[IsUquvBoshqarmasi],
    )
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user_data = {
            'username': request.data.get('username', user.username),
            'password': request.data.get('password', user.password),
            'passwordinfo': request.data.get('password', user.password),
            'user_type': 4,
            'is_active': True,
        }
        user_serializer = CustomUserSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        uquvboshqarmasi_data = {
            'name': request.data.get('name', instance.name),
            
            'user': user.pk,
        }
        uquvboshqarmasi_serializer = self.get_serializer(instance, data=uquvboshqarmasi_data)
        uquvboshqarmasi_serializer.is_valid(raise_exception=True)
        self.perform_update(uquvboshqarmasi_serializer)
        return Response(uquvboshqarmasi_serializer.data, status=status.HTTP_200_OK)
    

   
    
    
    
