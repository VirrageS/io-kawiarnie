from django.core.exceptions import ValidationError
from django.db import models
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

    name = models.CharField(max_length=100,)
    description = models.TextField(max_length=500, null=True, blank=True,)
    categories = models.ManyToManyField(Category)
    caffe = models.ForeignKey(
        'caffe.Caffe',
        null=True,
        blank=False,
        default=None
    )

    class Meta:
        ordering = ('name', 'description')
        default_permissions = ('add', 'change', 'delete', 'view')

    def clean(self, *args, **kwargs):
        """Clean data and check validation."""

        self.name = self.name.lstrip().rstrip()
        if self.name == '':
            raise ValidationError(_('Stencil name is not valid.'))

        query = Stencil.objects.filter(
            name__iexact=self.name,
            caffe=self.caffe
        ).all()

        if self.pk:
            query = query.exclude(pk=self.pk)

        if query.exists():
            raise ValidationError(_('Stencil with same name already exists.'))

        super(Stencil, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Save model into the database."""

        self.full_clean()
        super(Stencil, self).save(*args, **kwargs)

        if self.categories is not None:
            for category in self.categories.all():
                if self.caffe != category.caffe:
                    raise ValidationError(
                        _('Kawiarnia i kawiarnia kategorii nie zgadza się.')
                    )

    def __str__(self):
        return '{}'.format(self.name)
