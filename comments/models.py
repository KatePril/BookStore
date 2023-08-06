from django.db import models
from shop.models import Book
from django.contrib.auth import get_user_model

# Create your models here.
class CommentBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='commentsBook')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='commentsBook')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.book.name} - {self.text}'
    
    class Meta:
        ordering = ['-created_at']