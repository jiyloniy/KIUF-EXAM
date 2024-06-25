from django.db import models
from UserType.models import CustomUser, Student, Teacher,UquvBoshqarmasi,Fakultet
from django.utils.translation import gettext_lazy as _


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Group name'))
    fakultet = models.ForeignKey(Fakultet, verbose_name=_('Fakultet'), on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, verbose_name=_('Students'))
    additional_students = models.ManyToManyField(Student, verbose_name=_('Additional students'), related_name='additional_students')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        db_table = 'groups'


class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Subject name'))
    fakultet = models.ForeignKey(Fakultet, verbose_name=_('Fakultet'), on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, verbose_name=_('Teacher'), on_delete=models.CASCADE)
    group = models.ForeignKey(Group, verbose_name=_('Group'), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')
        db_table = 'subjects'


