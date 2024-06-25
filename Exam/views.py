from django.shortcuts import render
from Exam.er import Questions,StudentTests,Answers,WrittenQuestions,Tests,TestPages
from Exam.models import TestPage,Test,Answer,Question,StudentTest,WrittenQuestion
# Create your views here.
from rest_framework import viewsets
class TestPageView(viewsets.ModelViewSet):
    queryset = TestPage.objects.all()
    serializer_class = TestPages


class Questionsview(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = Questions

class StudentTestView(viewsets.ModelViewSet):
    queryset = StudentTest.objects.all()
    serializer_class = StudentTests



class AnswersView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = Answers



class WrittenQuestionsView(viewsets.ModelViewSet):
    queryset = WrittenQuestion.objects.all()
    serializer_class = WrittenQuestions


class TestsView(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = Tests


