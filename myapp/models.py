from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.search}"

    class Meta:
        verbose_name_plural = "Searches"
