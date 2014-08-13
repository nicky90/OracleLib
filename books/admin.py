from django.contrib import admin

from books.models import Book, Record

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'name', 'author', 'publisher', 'status')
    search_fields = ['identifier', 'name', 'author', 'publisher', 'status']

class RecordAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'sdate', 'edate')
    search_fields = ['book', 'user']

admin.site.register(Book, BookAdmin)
admin.site.register(Record, RecordAdmin)
