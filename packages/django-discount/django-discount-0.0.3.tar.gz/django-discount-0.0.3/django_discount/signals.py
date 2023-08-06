from django.db.models.signals import post_save

from .models import UsedDiscount


def used_discount_updated(**kwargs):
    used_discount = kwargs.get('instance')
    if kwargs['created']:
        discount = used_discount.discount
        discount.total_usages += 1
        discount.save()


post_save.connect(used_discount_updated, sender=UsedDiscount)
