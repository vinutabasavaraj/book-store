from django.shortcuts import render
from django.http import Http404
from .models import Book
from django.db.models import Avg

# Create your views here.
def index(request):
    books = Book.objects.all().order_by("-title")
    num_of_books = books.count()
    avg_rating = books.aggregate(Avg("rating"))
    return render(request, "book_outlet/index.html",
                  {"books":books,
                   "total_no_of_books":num_of_books,
                   "average_rating": avg_rating})
    
def book_detail(request,slug):
    try:
        book = Book.objects.get(slug=slug)
    except:
        raise Http404()
    return render(request,"book_outlet/book_details.html",{
        "title" :book.title,
        "author":book.author,
        "rating":book.rating,
        "is_bestseller":book.is_bestSelling
    })
    