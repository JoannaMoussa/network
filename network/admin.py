from django.contrib import admin
from .models import User, Post, Connection

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")


class PostAdmin(admin.ModelAdmin): 
    list_display = ("creator", "content", "timestamp", "get_likers")
    
    def get_likers(self, obj):
        return "\n".join([r.username for r in obj.likers.all()])
    

class ConnectionAdmin(admin.ModelAdmin):
    list_display = ("origin", "target")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Connection, ConnectionAdmin)
