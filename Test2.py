from django.db import models
from django.utils.timezone import now

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cover_image = models.ImageField(upload_to="book_covers", default="")

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reviewer = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField()
    date_posted = models.DateTimeField(default=now)

    def __str__(self):
        return f"Review of {self.book.title} by {self.reviewer}"

class LibraryMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name

class BorrowRecord(models.Model):
    member = models.ForeignKey(LibraryMember, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.name} borrowed {self.book.title}"

    @property
    def is_overdue(self):
        if self.return_date:
            return self.return_date < now()
        return False

    @property
    def total_days_borrowed(self):
        if self.return_date:
            return (self.return_date - self.borrow_date).days
        return (now() - self.borrow_date).days
