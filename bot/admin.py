from django.contrib import admin
from django.db.models import QuerySet, Count
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from datetime import date
from bot.models import User, Link, BaseTable


class DecadeBornListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ("decade born")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "decade"

    def lookups(self, request, model_admin: User):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ("80s", ("in the eighties")),
            ("90s", ("in the nineties")),
        ]

    def queryset(self, request, queryset: QuerySet[User]):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == "80s":
            return queryset.filter(
                registratin_date__gte=date(1980, 1, 1),
                registratin_date__lte=date(1989, 12, 31),
            )
        if self.value() == "90s":
            return queryset.filter(
                registratin_date__gte=date(1990, 1, 1),
                registratin_date__lte=date(1999, 12, 31),
            )


class DuplicatVideoFilter(admin.SimpleListFilter):
    """
        This filter is being used in django admin panel.
        """
    title = 'Дубликаты'
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        return (
            ('duplicates', 'Дубликаты юзеров'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'duplicates':
            dupes = BaseTable.objects.values('user').annotate(user_count=Count('user')).exclude(user_count=1)
            return queryset.filter(user__in=[item['user'] for item in dupes])


class UserAdmin(admin.ModelAdmin):
    

    readonly_fields = [
        'user_id',
        'user_name',
        'first_name',
        'last_name',
        'registratin_date',
        ]
    search_fields = [
        'user_id',
        'user_name',
        "first_name",
        ]
    
    exclude = []

    list_display = [
        'user_id',
        'user_name',
        'first_name',
        'last_name',
        'registratin_date',
        ]
    
    list_filter = [
        "registratin_date",
        #DecadeBornListFilter,
        ]


class LinkAdmin(admin.ModelAdmin):
    

    readonly_fields = [
        'invite_link',
        'name',
        ]

    exclude = []
    search_fields = [
        'name',
        'invite_link',
        ]
    list_display = [
        'invite_link',
        'name',
        'subs',
        "write",
        "join_vip",
        'ads_price',
        "subs_price",
        "write_price",
        "join_vip_price",
        'date',
        ]
    
    list_filter = [
        #DecadeBornListFilter,
        ]
    
    def subs(self, obj: Link) -> str:
        '''
        подписалось
        '''
        return obj._subs

    subs.short_description = "Подписалось"

    def write(self, obj: Link) -> str:
        '''
        Написало
        '''
        return obj._write

    write.short_description = "Написало"

    def join_vip(self, obj: Link) -> str:
        '''
        Вступило
        '''
        return obj._join_vip

    join_vip.short_description = "Вступило в VIP"


    def subs_price(self, obj: Link) -> str:
        '''
        подписалось
        '''
        return obj._subs_price

    subs_price.short_description = "Цена ПДП"

    def write_price(self, obj: Link) -> str:
        '''
        подписалось
        '''
        return obj._write_price

    write_price.short_description = "Цена Написало"

    def join_vip_price(self, obj: Link) -> str:
        '''
        подписалось
        '''
        return obj._join_vip_price

    join_vip_price.short_description = "Цена Вступило в VIP"
    

class BaseTableAdmin(admin.ModelAdmin):
    


    readonly_fields = [
        ]
    
    search_fields = [
        'link__name',
        'link__invite_link',
        'user__user_id',
        'user__user_name',
        ]
    
    exclude = []
    list_display_links = ["id", "date", "write", "join_chat",]

    list_display = [
        "id",
        "user_link",
        "link_link",
        "date",
        "write",
        "join_chat",
        ]
    
    list_filter = [
        DuplicatVideoFilter,
        "write",
        "join_chat",
        "date",
        ]
    
    def user_link(self, obj: BaseTable):

        link = reverse("admin:bot_user_change", args=[obj.user.user_id])
        return format_html('<a href="{}">{}</a>', link, str(obj.user))

    user_link.short_description = 'Юзер'
    user_link.admin_order_field = 'user'

    def link_link(self, obj: BaseTable):

        link = reverse("admin:bot_link_change", args=[obj.link.id])
        return format_html('<a href="{}">{}</a>', link, str(obj.link))

    link_link.short_description = 'Юзер'
    link_link.admin_order_field = 'user'


admin.site.register(Link, LinkAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(BaseTable, BaseTableAdmin)