from django.db import models
from accounts.models import CustomUser
import uuid
from django.conf import settings
import os
from django.utils.text import slugify
import datetime
class Graduation(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
class Course(models.Model):
    graduation = models.ForeignKey(
        Graduation,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ("graduation", "name")

    def __str__(self):
        return f"{self.graduation.name} - {self.name}"
class Branch(models.Model):
    graduation = models.ForeignKey(
        Graduation,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="branches"
    )

    feedback_uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ("graduation", "course", "name")

    def __str__(self):
        if self.course:
            return f"{self.course.name} - {self.name}"
        return f"{self.graduation.name} - {self.name}"




class AcademicYear(models.Model):
    year = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.year



class Coordinator(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="coordinator_profile"
    )
    name=models.CharField(max_length=100,default='')
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user.username

class Batch(models.Model):
    number= models.IntegerField(default=1)
    graduation= models.ForeignKey(Graduation, on_delete=models.CASCADE,default=None,null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,default=None,null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    members = models.ManyToManyField(
        'Student',
        related_name='member_of_batches' 
    )
    guide =models.CharField(max_length=100,default='')
    coordinator = models.ForeignKey(Coordinator, on_delete=models.SET_NULL, null=True, blank=True)

    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.number.__str__() + " - " + self.branch.name + " - " + self.academic_year.year
from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField


# 🔥 Common path builder
def build_path(instance, file_type):
    graduation = slugify(instance.batch.graduation.name if instance.batch.graduation else "unknown")
    branch = slugify(instance.batch.branch.name if instance.batch.branch else "unknown")
    year = slugify(instance.batch.academic_year.year if instance.batch.academic_year else "unknown")
    batch_no = instance.batch.number

    return f"projects/{graduation}/{branch}/{year}/{file_type}/{batch_no}"


# ✅ Individual public_id functions (Cloudinary requires single-arg callable)
def abstract_id(instance):
    return build_path(instance, "abstract")

def documentation_id(instance):
    return build_path(instance, "documentation")

def presentation_id(instance):
    return build_path(instance, "presentation")

def nptel_id(instance):
    return build_path(instance, "nptel")

def paper_id(instance):
    return build_path(instance, "research_paper")


class Project(models.Model):
    batch = models.OneToOneField('Batch', on_delete=models.CASCADE, related_name='project')
    title = models.CharField(max_length=255)

    abstract = CloudinaryField(resource_type='raw', public_id=abstract_id,folder=abstract_id)
    documentation = CloudinaryField(resource_type='raw', public_id=documentation_id,folder=documentation_id)
    presentation = CloudinaryField(resource_type='raw', public_id=presentation_id,folder=presentation_id)
    nptel = CloudinaryField(resource_type='raw', public_id=nptel_id, null=True, blank=True,folder=nptel_id)
    paper = CloudinaryField(resource_type='raw', public_id=paper_id, null=True, blank=True,folder=paper_id)

    coordinator_approved = models.BooleanField(default=False)
    rating = models.FloatField(null=True, blank=True, default=0)

    def delete(self, *args, **kwargs):
        self.batch.is_submitted = False
        self.batch.save(update_fields=['is_submitted'])

        if self.abstract: self.abstract.delete(save=False)
        if self.documentation: self.documentation.delete(save=False)
        if self.presentation: self.presentation.delete(save=False)
        if self.nptel: self.nptel.delete(save=False)
        if self.paper: self.paper.delete(save=False)

        super().delete(*args, **kwargs)


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    graduation= models.ForeignKey(Graduation, on_delete=models.SET_NULL, null=True)
    course=models.ForeignKey(Course,on_delete=models.SET_NULL,null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)
    guide=models.CharField(max_length=100,default='')
    coordinator = models.ForeignKey(Coordinator, on_delete=models.SET_NULL, null=True)
    batch = models.ForeignKey(
    Batch,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='students'
)

    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"
class Feedback(models.Model):
    project= models.ForeignKey(Project, on_delete=models.CASCADE, related_name='feedbacks')
    evaluator_name=models.CharField(max_length=255,default='')
    evaluator_id=models.CharField(max_length=100,default='')
    rating=models.FloatField(default=0)
