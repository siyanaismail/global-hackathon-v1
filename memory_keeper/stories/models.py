from django.db import models

class Memory(models.Model):
    story_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.story_text[:100] # Return first 100 characters of the story.