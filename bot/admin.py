from django.contrib import admin
from django.db.models import Count

from django.urls import reverse
from django.utils.html import format_html

from admin_extra_buttons.api import ExtraButtonsMixin, button
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
# Register your models here.

from bot.models import User, Link, BaseTable, DaysSummary, Buyer, DaysRangeSummary, LinkFilter



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
    list_editable=[
        "ads_price",
        "date",
        "buyer",
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
        'buyer',
        ]
    
    list_filter = [
        'buyer',
        #"invite_link",
        #'name',
        ]
    

    def save_model(self, request, obj: Link, form, change):
        '''
        перезаписываем метод сохранения модели
        '''

        admin_link = super().save_model(request, obj, form, change)
        
        if obj.date is not None:
            DaysSummary.objects.get_or_create(date=obj.date)

        return admin_link
    

    @admin.display(
            description='Подписалось',)
    def subs(self, obj: Link) -> str:
        '''
        подписалось
        '''
        return obj._subs


    @admin.display(description='Написало')
    def write(self, obj: Link) -> str:
        '''
        Написало
        '''
        return obj._write

    @admin.display(description='Вступило в VIP')
    def join_vip(self, obj: Link) -> str:
        '''
        Вступило
        '''
        return obj._join_vip


    @admin.display(description='Цена ПДП')
    def subs_price(self, obj: Link) -> str:
        '''
        подписалось
        '''
        return obj._subs_price


    @admin.display(description="Цена Написало")
    def write_price(self, obj: Link) -> str:
        '''
        подписалось
        '''
        return obj._write_price


    @admin.display(description="Цена Вступило в VIP")
    def join_vip_price(self, obj: Link) -> str:
        '''
        подписалось
        '''
        return obj._join_vip_price


class BaseTableAdmin(admin.ModelAdmin):
    
    date_hierarchy = 'date'

    readonly_fields = [
        ]
    
    search_fields = [
        'link__name',
        'link__invite_link',
        'user__user_id',
        'user__user_name',
        ]
    
    exclude = []
    list_display_links = ["id", "date",]
    list_editable=[
        "write",
        "join_chat",
        ]
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
    
    @admin.display(description='Юзер', ordering='user')
    def user_link(self, obj: BaseTable):

        link = reverse("admin:bot_user_change", args=[obj.user.user_id])
        return format_html('<a href="{}">{}</a>', link, str(obj.user))

    @admin.display(description='Ссылка', ordering='link')
    def link_link(self, obj: BaseTable):

        link = reverse("admin:bot_link_change", args=[obj.link.id])
        return format_html('<a href="{}">{}</a>', link, str(obj.link))


class DaysSummaryAdmin(admin.ModelAdmin):

    
    date_hierarchy = 'date'
    ordering = ['-date']
    readonly_fields = [
        #'date',
        
        'buy_summa',
        'PDP_summa',
        'PDP_total_price',
        'write_summa',
        'write_total_price',
        'VIP_summa',
        'VIP_total_price',
        'PDP_total_summa',
        ]
    exclude = []
    search_fields = [
        ]
    list_display = [
        'date',
        "buyers_admin",
        'buy_summa',
        'PDP_summa',
        'PDP_total_price',
        'write_summa',
        'write_total_price',
        'VIP_summa',
        'VIP_total_price',
        'PDP_total_summa',
        ]
    
    list_filter = [
        ]
    

    @admin.display(
            description='Закупщики',)
    def buyers_admin(self, obj: DaysSummary) -> int:

        if obj.buyers.exists():
            s = '<ol>'
            for b in obj.buyers.all():
                link = reverse("admin:bot_buyer_change", args=[b.id])
                s += "<li><a href='%s'>%s</a></li>" % (link, str(b.name))
            s += "</ol>"
            return format_html(s)
        return "Все"


    @admin.display(
            description='Сума закупа',)
    def buy_summa(self, obj: DaysSummary) -> int:

        return obj._buy_summa
    
    @admin.display(description='ПДП')
    def PDP_summa(self, obj: DaysSummary) -> int:

        return obj._PDP_summa
    
    @admin.display(description='Написало')
    def write_summa(self, obj: DaysSummary) -> int:

        return obj._write_summa
    
    @admin.display(description='VIP')
    def VIP_summa(self, obj: DaysSummary) -> int:

        return obj._VIP_summa
    
    @admin.display(description='ПДП база')
    def PDP_total_summa(self, obj: DaysSummary) -> int:

        return obj._PDP_total_summa
    

    @admin.display(description='Стоимость')
    def PDP_total_price(self, obj: DaysSummary) -> int:

        return obj._PDP_total_price
    
    @admin.display(description='Стоимость')
    def write_total_price(self, obj: DaysSummary) -> int:

        return obj._write_total_price
    
    @admin.display(description='Стоимость')
    def VIP_total_price(self, obj: DaysSummary) -> int:

        return obj._VIP_total_price


class DaysRangeSummaryAdmin(admin.ModelAdmin):

    list_display_links = [
        'date_from',
        'date_to',
        'buy_summa',
        'PDP_summa',
        'PDP_total_price',
        'write_summa',
        'write_total_price',
        'VIP_summa',
        'VIP_total_price',
        'PDP_total_summa',
    ]
    readonly_fields = [
        'buy_summa',
        'PDP_summa',
        'PDP_total_price',
        'write_summa',
        'write_total_price',
        'VIP_summa',
        'VIP_total_price',
        'PDP_total_summa',
        ]
    exclude = []
    search_fields = [
        ]
    list_display = [
        'date_from',
        'date_to',
        'buyers_admin',
        'buy_summa',
        'PDP_summa',
        'PDP_total_price',
        'write_summa',
        'write_total_price',
        'VIP_summa',
        'VIP_total_price',
        'PDP_total_summa',
        ]
    
    list_filter = [
        ]
    

    @admin.display(
            description='Закупщики',)
    def buyers_admin(self, obj: DaysSummary) -> int:

        if obj.buyers.exists():
            s = '<ol>'
            for b in obj.buyers.all():
                link = reverse("admin:bot_buyer_change", args=[b.id])
                s += "<li><a href='%s'>%s</a></li>" % (link, str(b.name))
            s += "</ol>"
            return format_html(s)
        return "Все"


    @admin.display(
            description='Сума закупа',)
    def buy_summa(self, obj: DaysSummary) -> int:

        return obj._buy_summa
    
    @admin.display(description='ПДП')
    def PDP_summa(self, obj: DaysSummary) -> int:

        return obj._PDP_summa
    
    @admin.display(description='Написало')
    def write_summa(self, obj: DaysSummary) -> int:

        return obj._write_summa
    
    @admin.display(description='VIP')
    def VIP_summa(self, obj: DaysSummary) -> int:

        return obj._VIP_summa
    
    @admin.display(description='ПДП база')
    def PDP_total_summa(self, obj: DaysSummary) -> int:

        return obj._PDP_total_summa
    

    @admin.display(description='Стоимость')
    def PDP_total_price(self, obj: DaysSummary) -> int:

        return obj._PDP_total_price
    
    @admin.display(description='Стоимость')
    def write_total_price(self, obj: DaysSummary) -> int:

        return obj._write_total_price
    
    @admin.display(description='Стоимость')
    def VIP_total_price(self, obj: DaysSummary) -> int:

        return obj._VIP_total_price


class BuyerAdmin(admin.ModelAdmin):
    
    readonly_fields = [
        ]

    exclude = []
    search_fields = [
        'name',
        ]
    list_display = [
        'name',
        ]
    
    list_filter = [
        ]


class LinkFilterAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    
    date_hierarchy = 'date'

    readonly_fields = [
        'subs',
        "write",
        "join_vip",
        'ads_price',
        "subs_price",
        "write_price",
        "join_vip_price",
        'date',
        'buyer',
        ]

    exclude = []
    search_fields = [
        'invite_link__name',
        'invite_link__invite_link',
        ]

    
    list_display = [
        'invite_link',
        'subs',
        "write",
        "join_vip",
        'ads_price',
        "subs_price",
        "write_price",
        "join_vip_price",
        'date',
        'buyer',
        ]
    
    list_filter = [
        'buyer',
        "date",
        #'name',
        ]
    @button(html_attrs={'style': 'background-color:#88FF88;color:black'})
    def refresh_data(self, request):

        try:
            for link in Link.objects.all():
                link_filter, is_new = LinkFilter.objects.get_or_create(invite_link=link)
                link_filter.refresh()
            self.message_user(request, 'Данные обновлены', level="SUCCESS")
        except Exception as e:
            self.message_user(request, f'Данные не обновлены: {repr(e)}', level="ERROR")

        return HttpResponseRedirectToReferrer(request)
    



admin.site.register(Buyer, BuyerAdmin)
admin.site.register(DaysSummary, DaysSummaryAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(LinkFilter, LinkFilterAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(BaseTable, BaseTableAdmin)
admin.site.register(DaysRangeSummary, DaysRangeSummaryAdmin)
