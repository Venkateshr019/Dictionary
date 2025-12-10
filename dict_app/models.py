from django.db import models


class SearchHistory(models.Model):
    word = models.CharField(max_length=120)
    definition = models.TextField(blank=True)
    synonyms = models.TextField(blank=True)
    antonyms = models.TextField(blank=True)
    examples = models.TextField(blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)
    pronunciation = models.TextField(blank=True)

    class Meta:
        ordering = ['-searched_at']

    def __str__(self) -> str:
        return f"{self.word} @ {self.searched_at:%Y-%m-%d %H:%M}"
