from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from reports.models import Category


class Stencil(models.Model):
    """Stores template of Report which can be used to create Reports faster.

    Attributes:
        name (str): Name for given Stencil.
        description (Optional(str)): Description for Stencil which should
            describe why this Stencil exists or add additional informations.
        categories (List(Category)): Categories which are used in creating
            Report from this Stencil.
    """

    name = models.CharField(max_length=100, unique=True,)
    description = models.TextField(max_length=500, null=True, blank=True,)
    categories = models.ManyToManyField(Category)

    def clean(self, *args, **kwargs):
        self.name = self.name.lstrip().rstrip()
        if self.name == '':
            raise ValidationError(_('Stencil name is not valid.'))

        same_stencil = Stencil.objects.filter(name__iexact=self.name).all()
        if same_stencil:
            raise ValidationError(_('Stencil with same name already exists.'))

        super(Stencil, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Stencil, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)
