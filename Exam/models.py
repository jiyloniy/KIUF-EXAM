from django.db import models
"""I want to create a website where I can take exams, i.e. online tests, I need to create a model that stores test questions. here it happens that the teacher takes the questions and assigns them to groups and sets a date and event. There are 2 types of questions. 1. There are always 4 answers. time, test page and other things will be attached, the second one will have a test page, it will store questions, for example, if there are 26 selectable questions, 4 written questions, or else, create a model with the most optimal and modern solution, another thing is to save the student's results. the student should not be able to retake the test after solving it. and in written tests, it should be visible to the student after the teacher has checked it, make a model of it"""
from UserType.models import Student, Teacher
from education.models import Group

class Answer(models.Model):
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer
    
class Question(models.Model):
    question = models.CharField(max_length=255)
    answers = models.ManyToManyField(Answer)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class WrittenQuestion(models.Model):
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class TestPage(models.Model):
    questions = models.ManyToManyField(Question)
    mark = models.IntegerField(default=0)
    writtenquestions = models.ManyToManyField(WrittenQuestion)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.questions.count()} questions and {self.writtenquestions.count()} written questions'
    

class Test(models.Model):
    test_page = models.ForeignKey(TestPage, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    event = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event
    


class StudentTest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student} got {self.result} on {self.test}'
