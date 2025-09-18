from django.conf import settings
from django.db import models


class Link(models.Model):
    """Model for storing shortened URLs.

    Short codes are derived from the ID primary key using Sqids.

    Attributes:
        id (int): The primary key.
        long_url (str): The original URL to be shortened.
    """

    id = models.BigAutoField(primary_key=True)
    long_url = models.URLField(max_length=2048)

    @property
    def short_code(self):
        """Generate a short code from the link's ID."""
        return settings.DEFAULT_SQID.encode([self.id])

