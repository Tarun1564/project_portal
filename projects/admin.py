from django.contrib import admin
from .models import *
admin.site.register(Batch)
admin.site.register(Project)
admin.site.register(AcademicYear)
admin.site.register(Coordinator)
admin.site.register(Student)
admin.site.register(Feedback)
admin.site.register(Graduation)
admin.site.register(Course)
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "feedback_uuid")
    readonly_fields = ("feedback_uuid",)
