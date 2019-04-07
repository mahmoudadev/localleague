from django.db import models


class SponsorshipPackge(models.Model):
    name = models.CharField(max_length=1024, null=True, blank=True)
    Type = models.CharField(blank=True, null=True, max_length=30,
                            choices=(
                                ('golden', 'GOLDEN'),
                                ('silver', 'SILVER'),

                            )
                            )

    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
