import math
import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .utils import *
from .consts import *
from .settings import *

User = get_user_model()


class DiscountManager(models.Manager):

    def check_code(self, code, user_id, amount=None, **kwargs):
        """ Will check code, and find proper discount for it,
        then will do some validations if this code is valid for
        this user and this item or not. Then will calculate total
        discount for amount of transaction.

        :arg amount:    if amount set, we should calc discount based on it,
                        for percent and calculation better to send amount value
        """

        # First check if this discount item do exist
        # discount = self.filter(code=code).prefetch_related('items').first()
        discount = self.filter(code=code).first()
        if not discount:
            return False, 0, _('Discount code is not valid.')

        is_available, msg = discount.is_available(user_id)
        if not is_available:
            return False, 0, msg

        # # Now verify if the item_type and item_id items do exist in list if DiscountItems
        # status, msg = discount.check_if_item_allowed(item_type, item_id)
        # if not status:
        #     return False, 0, msg

        discount_amount = 0
        if amount:
            if amount < discount.min_invoice_amount:
                return False, 0, 'حداقل میزان تراکنش برای اعمال این کد تخفیف {} تومان است.'.format(
                    price_beautifier(discount.min_invoice_amount)
                )

            discount_amount = discount.calc_discount(amount)
        return True, discount_amount, _('it is valid.')


class Discount(models.Model):
    user = models.ForeignKey(
        User,
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='discounts',
        verbose_name=_('Specific user to use this discount'),
        help_text=_('When empty discount will be used for everyone and should not be any duplicates. '
                    'But if User set it can have discount\'s with different users and duplicate codes. '
                    'And that specific discount will only be available for that user.')
    )
    title = models.CharField(
        max_length=100,
        verbose_name=_('Title')
    )
    code = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name=_('Code')
    )

    # Discount amount to apply
    type = models.CharField(
        max_length=10,
        default='percent',
        choices=DISCOUNT_TYPES,
        verbose_name=_('Discount type'),
    )
    value = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Discount value')
    )

    # Limitations
    min_invoice_amount = models.IntegerField(
        default=10000,
        verbose_name='حداقل مبلغ فاکتور برای اعمال تخفیف',
    )
    max_amount = models.IntegerField(
        default=100000,
        verbose_name='حداکثر میزان تخفیف',
        help_text='در صورتی که میزان تخفیف بیش از این عدد شود،'
                  ' تنها این میزان اعمال خواهد شد.'
    )

    # Usage Parameters
    usage_limit = models.IntegerField(
        default=50,
        verbose_name='حداکثر تعداد دفعاتی که این کد تخفیف قابل استفاده است.'
    )
    usage_limit_per_user = models.IntegerField(
        default=1,
        verbose_name=_('Maximum usage for each user')
    )
    total_usages = models.IntegerField(
        default=0,
        verbose_name='تعداد دفعات استفاده شده'
    )
    # included_items = models.TextField(
    #     default='', verbose_name=_('Included Items'),
    #     help_text=_('If empty, will be applied on all items')
    # )       # include_items sample:     [{'type': 0, 'id': 1}, ...] as string
    # excluded_items = models.TextField(
    #     default='', verbose_name=_('Excluded Items'),
    #     help_text=_('If empty, will not exclude any item')
    # )       # excluded_items sample:    [{'type': 0, 'id': 1}, ...] as string

    # Date attributes
    start_date = models.DateTimeField(
        null=True, blank=True,
        verbose_name='زمان شروع تخفیف',
        help_text='در صورت خالی بودن زمان شروع حال در نظر گرفته می‌شود.'
    )
    expire_date = models.DateTimeField(
        null=True, blank=True,
        verbose_name='زمان پایان اعتبار کد تخفیف',
        help_text='در صورتی که خالی تعریف شد، کد تخفیف منقضی نخواهد شد.'
    )

    # Extra Attributes
    case_sensitive = models.BooleanField(
        default=True,
        verbose_name=_('Case Sensitive')
    )

    # Accessibility Attributes
    is_active = models.BooleanField(
        default=True,
        verbose_name='وضعیت فعال بودن کد تخفیف'
    )
    not_active_reason = models.CharField(
        default='',
        max_length=100,
        verbose_name='علت غیرفعال بودن', blank=True
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="حذف شد",
    )

    objects = DiscountManager()

    def __str__(self):
        return '{}, {}'.format(self.title, self.code)

    class Meta:
        db_table = 'discount'
        verbose_name = 'Discount'
        verbose_name_plural = _('Discount')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # If no start date, set it to current datetime now()
        if not self.start_date:
            self.start_date = datetime.datetime.now()

        # If no expire_date, set DISCOUNT_DEFAULT_DURATION days from now
        if not self.expire_date:
            d = datetime.timedelta(days=DISCOUNT_DEFAULT_DURATION)
            self.expire_date = self.start_date + d

        if self.expire_date <= self.start_date:
            raise ValueError(_('Expire date can\'t be before Start Date of discount.'))

        # Here will check for duplicate scenarios
        if not self.pk:
            if self.user:
                # Only one instance with user=self.user and same code should exist
                if Discount.objects.filter(code=self.code, user=self.user).exists():
                    raise ValueError(_('This code already exist for this user.'))
            else:
                # There should not be any other instance without user and same code
                if Discount.objects.filter(code=self.code, user__isnull=True).exists():
                    raise ValueError(_('This code already exists'))

        # In percent type, value should be between 0 and 100
        if self.type == 'percent':
            if not 0 <= self.value <= 100:
                raise ValueError(_('Value should be between 0 and 100 for percent type.'))

        super(Discount, self).save()

    def is_available(self, user_id=None):
        """ This method will check if discount is valid to be used or not.
        It will do the followings:

        - Check activation of discount
        - check if total usages is not greater and usage-limit
        - check if started and not expired yet
        - if user_id provided, check if this user allowed to use it or not
        """
        if not self.is_active:
            msg = _('Discount code is not active.')
            return False, msg

        if self.total_usages >= self.usage_limit:
            msg = _('Discount code is expired.')
            self.deactivate(msg, True)
            return False,

        now = datetime.datetime.now()
        if now < self.start_date:
            msg = _('Time to use discount code is not started yet!')
            return False, msg

        if now > self.expire_date:
            msg = _('Discount code is expired.')
            self.deactivate(msg, True)
            return False, msg

        # Now check if user is already used this discount code or not!
        # if count bigger than max usage it ignore system
        if user_id:
            # First check if self.user is valid
            if self.user:
                if user_id != self.user_id:
                    return False, _('User is not valid.')

            # Now check if user already used it or not!
            count_discount = UsedDiscount.objects.filter(
                user_id=user_id,
                discount_id=self.id
            ).count()
            if count_discount >= self.usage_limit_per_user:
                msg = 'شما از این کد تخفیف {} استفاده کرده‌اید واین حدکثر تعداد مجاز برای شماست.'.format(count_discount)
                return False, msg

        return True, ''

    def deactivate(self, msg='', commit=True):
        self.is_active = False
        if msg:
            self.not_active_reason = msg
        if commit:
            self.save()

    def calc_discount(self, amount):
        """ Will calculate how much value of discount will be if is applied on amount. """
        if self.type == 'percent':
            discount = math.ceil(amount * self.value / 100)
        else:
            discount = self.value
        if discount > self.max_amount:
            discount = self.max_amount
        if discount < 0:
            discount = 0
        return discount

    # def check_if_item_allowed(self, item_type, item_id):
    #     item = self.items.filter(type=item_type).first()
    #     if not item:
    #         return False, 'کد تخفیف برای این آیتم تعریف نشده است.'
    #     if not item.id_list or item_id in item.id_list:
    #         return True, ''
    #     return False, 'کد تخفیف برای این آیتم تعریف نشده است.'


# class DiscountItem(models.Model):
#     """ Model will hold items and their list of item IDs.
#     So whenever we want to validate a discount code on an item,
#     Will check it's type and id with this model. """
#     discount = models.ForeignKey(
#         Discount,
#         on_delete=models.CASCADE,
#         related_name='items'
#     )
#     type = models.CharField(
#         choices=DISCOUNT_ITEM_TYPES,
#         default='hotel', max_length=10,
#         verbose_name='نوع آیتمی که کد می‌تواند بر روی آن اعمال شود.'
#     )
#     id_list = ArrayField(
#         models.IntegerField(null=True, blank=True), default=list, blank=True,
#         verbose_name='لیست آی‌دی‌های این نوع آیتم که بر روی آن‌ها قابل اعمال است.',
#         help_text='در صورتی که خالی باشد بر روی تمامی آیتم‌های این نوع قابل استفاده است.'
#     )
#
#     def __str__(self):
#         return '{} {}'.format(
#             self.get_type_display(),
#             self.discount.__str__()
#         )
#
#     class Meta:
#         db_table = 'discount_item'
#         verbose_name_plural = 'آیتم‌های کد تخفیف'
#
#     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
#         """
#         if discount not exist will be added but if discount and type exist will be update this discount id
#         :param force_insert:
#         :param force_update:
#         :param using:
#         :param update_fields:
#         :return:
#         """
#         if not self.pk:
#             dis_val = DiscountItem.objects.filter(
#                 discount=self.discount,
#                 type=self.type
#             )
#             if len(dis_val) > 0:
#                 DiscountItem.objects.filter(id=dis_val[0].id).update(id_list=self.id_list)
#                 return "update:{}".format(dis_val[0])
#             # raise ValueError('این نوع آیتم قبلا تعریف شده است.')
#             # super(DiscountItem,self).update()
#             else:
#                 super(DiscountItem, self).save()
#         # super(DiscountItem, self).save()


class UsedDiscount(models.Model):
    """ Whenever a user try to use a discount code,
    And purchase or own that item, it's better to keep
    record of that purchase in this model for later reports.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='used_discounts',
        verbose_name=_('User who used discount code')
    )
    discount = models.ForeignKey(
        Discount, null=False,
        related_name='usages',
        on_delete=models.CASCADE,
        verbose_name=_('Discount')
    )
    code = models.CharField(
        null=True, blank=True, max_length=20,
        verbose_name='Code used in that moment'
    )
    item_type = models.CharField(
        max_length=10,
        default='hotel',
        choices=DISCOUNT_ITEM_TYPES,
        verbose_name=_('Item type which user is trying to purchase or own'),
    )
    item_id = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('Type of item to purchase or own')
    )

    def __str__(self):
        return "{},{}".format(self.discount.title, self.item_id)

    class Meta:
        db_table = 'discount_used_record'
        verbose_name = 'Used Discount'
        verbose_name_plural = _('Used Discount')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.code:
            self.code = self.discount.code
        super(UsedDiscount, self).save()
