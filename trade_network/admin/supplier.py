from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from ..models import Supplier, Contact, Product


class ContactsInline(admin.StackedInline):
    model = Contact
    fields = (
        'email',
        'country',
        'city',
        'street',
        'house_number',
    )
    extra = 0


class ContactsCityFilter(admin.SimpleListFilter):
    title = 'Город'
    parameter_name = 'city'
    template = 'trade_network/dropdown_filter.html'

    def lookups(self, request, model_admin):
        # TODO: can be optimized (eg. db View-table or using Country -> City tables)
        cities = Contact.objects.values("city").distinct()

        return [(city['city'], city['city']) for city in cities]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(contacts__city=self.value())
        return queryset


@admin.action(description="Обнулить задолженость")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


# Register your models here.
@admin.register(Supplier)
class SupplierModelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'supplier_change',
        'debt',
    )

    @admin.display(
        description=Supplier._meta.get_field('supplier').verbose_name
    )
    def supplier_change(self, obj: Supplier):
        if obj.supplier is None:
            return '-'
        edit_url = reverse(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change",
            args=(obj.supplier.pk,),
        )
        return mark_safe(
            f'<a class="grp-button" href="{edit_url}" target="blank">{obj.supplier.name}</a>'
        )

    readonly_fields = ('hierarchy_level',)
    list_filter = (ContactsCityFilter,)
    actions = (clear_debt,)
    inlines = (ContactsInline,)
    filter_horizontal = ('products',)
