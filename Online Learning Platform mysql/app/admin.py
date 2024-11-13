from django.contrib import admin
from .models import *

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    inlines = [ModuleInline]
    list_display = ['title', 'is_active', 'created_at']
    search_fields = ['title', 'description']

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'answer_text']
    search_fields = ['user__username', 'question__text']

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'completed', 'completed_at']
    list_filter = ['completed', 'completed_at']
    search_fields = ['user__username', 'module__title']

admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Question)
admin.site.register(UserAnswer, UserAnswerAdmin)
