""" Functions for administration of the local library """
from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language, OCRImage
admin.site.register(Genre)
admin.site.register(Language)

class BookInline(admin.TabularInline):
    """ A class based view for administrating books inline."""
    model = Book
    extra = 0
# Define the admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """ A class based view for administrating authors."""
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

class BooksInstanceInline(admin.TabularInline):
    """ A class based view for administrating book instances inline."""
    model = BookInstance
    extra = 0
# Register the Admin classes for Book using the decorator

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """ A class based view for administrating books."""
    list_display = ('title', 'author', 'language', 'display_genre')
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """ A class based view for administrating book instances."""
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

@admin.register(OCRImage)
class OCRImageAdmin(admin.ModelAdmin):
    """ A class based view for administrating OCRImages."""
    list_display = ('file_name', 'text', 'photo')
