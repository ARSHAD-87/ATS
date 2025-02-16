from djongo import models

class JobListing(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True, null=True)  # New field for salary
    link = models.URLField(unique=True)

    def __str__(self):
        return self.title
