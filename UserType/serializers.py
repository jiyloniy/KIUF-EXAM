from rest_framework import serializers
from UserType.models import  CustomUser, Fakultet, Student, Teacher,UquvBoshqarmasi

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'user_type', 'is_active', 'is_archive','passwordinfo']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_archive = validated_data.get('is_archive', instance.is_archive)
        instance.passwordinfo = validated_data.get('passwordinfo', instance.passwordinfo)
        instance.save()
        return instance

    
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'name',
            'user',
            'surname',
            'age',
            'phone',
            'studentid',
            'address',
        ]

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            'name',
            'user',
            'surname',
            'age',
            'phone',
            'teacherid',
            'address',
        ]

class FakultetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fakultet
        fields = [
            'id',
            'name',
            'user',
            'fakultetid',
        ]

class UquvBoshqarmasiSerializer(serializers.ModelSerializer):
    class Meta:
        model = UquvBoshqarmasi
        fields = [
            'id',
            'name',
            'user',
        ]

