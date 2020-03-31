""" View for the catalog page """
import datetime

from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from catalog.models import Book, Author, BookInstance, Genre, OCRImage
from catalog.forms import RenewBookForm, OCRImageForm

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_books_with_the = Book.objects.filter(title__icontains='the').count()
    num_genres_with_s = Genre.objects.filter(name__icontains='s').count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_the': num_books_with_the,
        'num_genres_with_s': num_genres_with_s,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

    # If this is a POST request, then process the Form data


#class HomeView(LoginRequiredMixin, generic.View):

class BookListView(LoginRequiredMixin, generic.ListView):
    """ A class to handle a view of sets of books and information about them """
    model = Book
    paginate_by = 10

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    """ A class to handle a view of a specific book's details """
    model = Book

class AuthorListView(LoginRequiredMixin, generic.ListView):
    """ A class to handle a view of sets of authors and information about them """
    model = Author
    paginate_by = 10

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    """ A class to handle a view of a specific book's details """
    model = Author

class OCRImageListView(LoginRequiredMixin, generic.ListView):
    """ A class to handle a view of sets of ocr images and information about them """
    model = OCRImage
    paginate_by = 10

class OCRImageDetailView(LoginRequiredMixin, generic.DetailView):
    """ A class to handle a view of a specific ocr image's details """
    model = OCRImage

def ocrimage_upload(request):
    """ A function to upload images to process with OCR """
    if request.method == 'POST':
        form = OCRImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ocrimages'))
    else:
        form = OCRImageForm()
    return render(request, 'ocrimage_upload_form.html', {'form' : form})


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back') # pylint: disable=line-too-long

class LoanedBooksStaffView(PermissionRequiredMixin, generic.ListView):
    """" Generic class-based view listing all books on loan. """
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_staff.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back') # pylint: disable=line-too-long

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)



class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
