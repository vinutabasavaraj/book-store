from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify


class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=2)
    
    def __str__(self):
        return f"{self.name}, {self.code}"
    
    class Meta:
        verbose_name_plural = "Countries"


class Address(models.Model):
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.street}, {self.postal_code}, {self.city}"
    
    class Meta:
        verbose_name_plural = "Address Enteries"

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE,related_name="author",null=True)
    
    
    def full_name(self):
        return f"{self.first_name} ({self.last_name})"
    
    def __str__(self):
        return self.full_name()
        

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50) #for string field
    rating = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True,related_name="books")
    is_bestSelling = models.BooleanField(default=False)
    slug = models.SlugField(default="",blank=True,null=False,db_index=True)#Harry Potter 1 to harry-potter-1
    published_countries = models.ManyToManyField(Country,related_name="books")
    
    #built in method to get the url of particular book
    def get_absolute_url(self):
        return reverse('book-detail', args=[self.slug])
    
    #To overwrite builtin save method
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.rating})"
    
