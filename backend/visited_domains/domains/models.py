from django.db import models


class Domain(models.Model):
    name = models.CharField(
        'Name',
        max_length=150,
        blank=False,
        null=False
    )
    created = models.DateTimeField(
        'Created',
        auto_now_add=True,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'

    def __str__(self):
        return f'{self.created} {self.name}'
