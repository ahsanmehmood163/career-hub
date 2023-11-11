from django.contrib import admin
from .models import Author, Tag, Post, Comment, StudentDetail, User, Course, Instructor, Album


class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "date", "tags",)
    list_display = ("title", "date", "author",)
    prepopulated_fields = {'slug': ("title", )}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post")


admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(StudentDetail)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Album)
