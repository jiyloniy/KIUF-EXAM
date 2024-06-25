from django.contrib import admin
from Exam.models import Answer, Question,  WrittenQuestion, TestPage, Test\

# admin.site.register(Answer)
admin.site.register(Question)

admin.site.register(WrittenQuestion)
admin.site.register(TestPage)
admin.site.register(Test)

# What is the purpose of this code?
#
# A. To register the models with the Django admin site
# class Answer for admin site
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer', 'is_correct']

admin.site.register(Answer, AnswerAdmin)