from rest_framework import serializers
from Exam.models import Answer,Group,Question,WrittenQuestion,TestPage,Test,StudentTest

class Answers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class Questions(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
    


class WrittenQuestions(serializers.ModelSerializer):
    class Meta:
        model = WrittenQuestion
        fields = '__all__'


    
class TestPages(serializers.ModelSerializer):
    class Meta:
        model = TestPage
        fields = '__all__'


class StudentTests(serializers.ModelSerializer):
    class Meta:
        model = StudentTest
        fields = '__all__'

class Tests(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

    
