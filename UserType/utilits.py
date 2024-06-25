# permissions for users
from rest_framework import permissions
from UserType.models import CustomUser, Student, Teacher, UquvBoshqarmasi, Fakultet

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1:
                return True
            return False
        except:
            return False
    
class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 2:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 2:
                return True
            return False
        except:
            return False
        
class IsFakultet(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 3:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 3:
                return True
            return False
        except:
            return False
        
class IsUquvBoshqarmasi(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 4:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 4:
                return True
            return False
        except:
            return False
        

class IsFakUquvBoshqarmasi(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 3 or user.user_type == 4:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 3 or user.user_type == 4:
                return True
            return False
        except:
            return False
        

class IsTeacherFakultet(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 2 or user.user_type == 3:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 2 or user.user_type == 3:
                return True
            return False
        except:
            return False
        

class IsTeacherUquvBoshqarmasi(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 2 or user.user_type == 4:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 2 or user.user_type == 4:
                return True
            return False
        except:
            return False
        

class IsStudentFakultet(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 3:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 3:
                return True
            return False
        except:
            return False
        

class IsStudentUquvBoshqarmasi(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 4:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 4:
                return True
            return False
        except:
            return False
        

class IsStudentTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 2:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 2:
                return True
            return False
        except:
            return False
        


class IsStudentTeacherFakultet(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 2 or user.user_type == 3:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 2 or user.user_type == 3:
                return True
            return False
        except:
            return False
        
class IsStudentTeacherUquvBoshqarmasi(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 2 or user.user_type == 4:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 2 or user.user_type == 4:
                return True
            return False
        except:
            return False
        
class IsStudentFakultetUquvBoshqarmasi(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 3 or user.user_type == 4:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 3 or user.user_type == 4:
                return True
            return False
        except:
            return False
        

class IsTeacherFakultetUquvBoshqarmasi(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 2 or user.user_type == 3 or user.user_type == 4:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 2 or user.user_type == 3 or user.user_type == 4:
                return True
            return False
        except:
            return False
        
class IsStudentTeacherFakultetUquvBoshqarmasi(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            print(user)
            if user.user_type == 1 or user.user_type == 2 or user.user_type == 3 or user.user_type == 4:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 2 or user.user_type == 3 or user.user_type == 4:
                return True
            return False
        except:
            return False
    
class IsFakTeachUquv(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = CustomUser.objects.get(username=request.user)
            print(user)
            if  user.user_type == 2 or user.user_type == 3 or user.user_type == 4:
                return True
            return False
        except:
            return False
    
    def has_object_permission(self, request, view, obj):
        try:
            user = CustomUser.objects.get(username=request.user)
            if user.user_type == 1 or user.user_type == 2 or user.user_type == 3 or user.user_type == 4:
                return True
            return False
        except:
            return False