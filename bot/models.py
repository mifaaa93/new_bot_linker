from django.db import models
from django.db.models import Sum
from django.db.models.query import QuerySet

# Create your models here.
# сколько знаков после запятой
ndigits = 2

class Buyer(models.Model):
    '''
    Закупщик
    '''
    class Meta:
        abstract = False
        verbose_name = "Закупщик"
        verbose_name_plural = "Закупщик"

    name = models.CharField("Имя", max_length=64, blank=False, editable=True, null=False)


    def __str__(self):

        return f"{self.name}"
    

class User(models.Model):
    '''
    юзер тг
    '''
    class Meta:
        abstract = False
        verbose_name = "Юзер телеграм"
        verbose_name_plural = "Юзер телеграм"

    user_id = models.IntegerField("ID", primary_key=True, unique=True, editable=False)
    first_name = models.CharField("Имя", max_length=64, blank=False, editable=False)
    
    user_name = models.CharField("Юзернейм", max_length=32, blank=True, null=True, editable=False, default=None)
    last_name = models.CharField("Фамилия", max_length=64, blank=True, null=True, editable=False, default=None)

    registratin_date = models.DateTimeField("Дата Первого Вступления", auto_now_add=True, editable=False)

    def __str__(self):
        if self.user_name is not None:
            s = f"@{self.user_name}"
        else:
            s = f"{self.first_name}"
        
        return f"{s} {self.user_id}"


    @property
    def username_or_empty(self) -> str:
        '''
        '''
        if self.user_name is not None:
            return f"@{self.user_name}"
        return ''
    
    
    @property
    def names(self) -> str:
        '''
        '''
        if self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        return f"{self.first_name}"


class Link(models.Model):
    '''
    ссылки для вступления в канал
    '''
    class Meta:
        abstract = False
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"
        unique_together = ('invite_link', 'name')
    
    invite_link = models.CharField("Ссылка", max_length=512, editable=False)
    name = models.CharField("Название", max_length=256, null=True, blank=True, editable=False, default=None)

    ads_price = models.IntegerField("Цена Рекламы", default=None, null=True, blank=True)
    date = models.DateField("Дата", default=None, null=True, blank=True)

    buyer = models.ForeignKey(
        verbose_name="Закупщик",
        to=Buyer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None)

    def __str__(self):

        if not self.name:
            return self.invite_link
        
        return f"{self.name} {self.invite_link}"
    

    @property
    def _subs(self) -> int:
        '''
        количество вступивших по данной ссылке
        '''
        return BaseTable.objects.filter(link=self).count()
    
    @property
    def _write(self) -> int:
        '''
        количество тех кто написал по данной ссылке
        '''
        return BaseTable.objects.filter(link=self, write=True).count()

    @property
    def _join_vip(self) -> int:
        '''
        количество тех кто вступил в вип по данной ссылке
        '''
        return BaseTable.objects.filter(link=self, join_chat=True).count()

    @property
    def _subs_price(self) -> float:
        '''
        цена вступивших по данной ссылке
        '''
        if self.ads_price is not None and self._subs > 0:

            return round(self.ads_price/self._subs, ndigits)

        return None
    

    @property
    def _write_price(self) -> float:
        '''
        цена тех кто написал по данной ссылке
        '''
        if self.ads_price is not None and self._write > 0:

            return round(self.ads_price/self._write, ndigits)

        return None

    @property
    def _join_vip_price(self) -> int:
        '''
        цена тех кто вступил в вип по данной ссылке
        '''
        if self.ads_price is not None and self._join_vip > 0:

            return round(self.ads_price/self._join_vip, ndigits)

        return None


class BaseTable(models.Model):
    '''
    все вступления юзеров по ссылкам
    '''
    class Meta:
        abstract = False
        verbose_name = "База"
        verbose_name_plural = "База"
    
    date = models.DateTimeField("Дата Вступления", auto_now_add=True)
    user = models.ForeignKey(verbose_name="Юзер", to=User, on_delete=models.CASCADE)
    link = models.ForeignKey(verbose_name="Ссылка", to=Link, on_delete=models.CASCADE)
    write = models.BooleanField("Написал", default=False)
    join_chat = models.BooleanField("Вступил в VIP", default=False)


    @property
    def to_text_links(self) -> str:
        '''
        31/02/2033 | 1150564331 - ТЕСТ Сергеевич111
        '''
        return f"{self.date_str} {self.user.user_id} {self.link.name}"
    
    
    @property
    def to_text_names(self) -> str:
        '''
        31/02/2033 | 1150564331 - ТЕСТ Сергеевич111
        '''
        return f"{self.date_str} {self.user.user_id} {self.user.names}"
    
    @property
    def to_text_usernames(self) -> str:
        '''
        31/02/2033 | 1150564331 - ТЕСТ Сергеевич111
        '''
        return f"{self.date_str} {self.user.user_id} {self.user.username_or_empty}"


    @property
    def date_str(self) -> str:
        '''
        25/02/2033
        '''
        return self.date.strftime("%d/%m/%Y")


    def make_write(self, val: bool=True) -> None:
        '''
        '''
        if self.write != val:
            self.write = val
            self.save(update_fields=["write"])
    

    def make_join_VIP(self, val: bool=True) -> None:
        '''
        '''
        if self.join_chat != val:
            self.join_chat = val
            self.save(update_fields=["join_chat"])


    def __str__(self):

        return f"{self.user} - {self.link}"


class DaysSummary(models.Model):
    '''
    статистика по дням
    '''
    class Meta:
        abstract = False
        verbose_name = "Дни"
        verbose_name_plural = "Дни"
    

    date = models.DateField("Дата", blank=False, null=False)
    buyers = models.ManyToManyField(to=Buyer, verbose_name="Закупщики", blank=True)


    @property
    def get_all_links(self) -> QuerySet[Link]:
        '''
        все ссылки за указаную дату
        '''
        if self.buyers.exists():
            return Link.objects.filter(
            date=self.date,
            buyer__in=self.buyers.all()
        )
        return Link.objects.filter(
            date=self.date
        )


    @property
    def _buy_summa(self) -> int:
        '''
        сумма закупов ссылок по дате
        '''
        return self.get_all_links.filter(
            ads_price__isnull=False
        ).aggregate(Sum("ads_price")).get("ads_price__sum", 0) or 0
    

    @property
    def _PDP_summa(self) -> int:
        '''
        количество подписчиков по ссылкам с этой датой
        '''
        return sum([link._subs for link in self.get_all_links])
    
    @property
    def _PDP_total_price(self) -> float:
        '''
        количество подписчиков по ссылкам с этой датой
        '''
        _PDP_summa = self._PDP_summa
        if not _PDP_summa:
            return 0
        
        return round(self._buy_summa/_PDP_summa, ndigits)
    
    @property
    def _write_total_price(self) -> float:
        '''
        количество кто написал по ссылкам с этой датой
        '''
        _PDP_summa = self._PDP_summa
        if not _PDP_summa:
            return 0
        
        return round(self._write_summa/_PDP_summa, ndigits)

    @property
    def _VIP_total_price(self) -> float:
        '''
        количество кто написал по ссылкам с этой датой
        '''
        _PDP_summa = self._PDP_summa
        if not _PDP_summa:
            return 0
        
        return round(self._VIP_summa/_PDP_summa, ndigits)
    

    @property
    def _write_summa(self) -> int:
        '''
        количество кто написал по ссылкам с этой датой
        '''
        return sum([link._write for link in self.get_all_links])
    
    @property
    def _VIP_summa(self) -> int:
        '''
        количество кто вступил в вип по ссылкам с этой датой
        '''
        return sum([link._join_vip for link in self.get_all_links])


    @property
    def _PDP_total_summa(self) -> int:
        '''
        количество подписчиков за этот день
        '''
        return BaseTable.objects.filter(
            date__date=self.date
        ).count()
    


class DaysRangeSummary(models.Model):
    '''
    статистика по периодам
    '''
    class Meta:
        abstract = False
        verbose_name = "Период"
        verbose_name_plural = "Период"
    

    date_from = models.DateField("Дата от", null=True, default=None, blank=True)
    date_to = models.DateField("Дата до", null=True, default=None, blank=True)
    buyers = models.ManyToManyField(to=Buyer, verbose_name="Закупщики", blank=True)


    def __str__(self):
        
        return f"{self.date_from or '-'} {self.date_to or '-'}"

    @property
    def get_all_links(self) -> QuerySet[Link]:
        '''
        все ссылки за указаный период дат
        '''
        qweryset = Link.objects.all()
        if self.buyers.exists():
            qweryset = qweryset.filter(buyer__in=self.buyers.all())
        if self.date_from is not None:
            qweryset = qweryset.filter(date__gte=self.date_from)
        if self.date_to is not None:
            qweryset = qweryset.filter(date__lte=self.date_to)
        return qweryset


    @property
    def _buy_summa(self) -> int:
        '''
        сумма закупов ссылок по дате
        '''
        return self.get_all_links.filter(
            ads_price__isnull=False
        ).aggregate(Sum("ads_price")).get("ads_price__sum", 0) or 0
    

    @property
    def _PDP_summa(self) -> int:
        '''
        количество подписчиков по ссылкам с этой датой
        '''
        return sum([link._subs for link in self.get_all_links])
    
    @property
    def _PDP_total_price(self) -> float:
        '''
        количество подписчиков по ссылкам с этой датой
        '''
        _PDP_summa = self._PDP_summa
        if not _PDP_summa:
            return 0
        
        return round(self._buy_summa/_PDP_summa, ndigits)
    
    @property
    def _write_total_price(self) -> float:
        '''
        количество кто написал по ссылкам с этой датой
        '''
        _PDP_summa = self._PDP_summa
        if not _PDP_summa:
            return 0
        
        return round(self._write_summa/_PDP_summa, ndigits)

    @property
    def _VIP_total_price(self) -> float:
        '''
        количество кто написал по ссылкам с этой датой
        '''
        _PDP_summa = self._PDP_summa
        if not _PDP_summa:
            return 0
        
        return round(self._VIP_summa/_PDP_summa, ndigits)
    

    @property
    def _write_summa(self) -> int:
        '''
        количество кто написал по ссылкам с этой датой
        '''
        return sum([link._write for link in self.get_all_links])
    
    @property
    def _VIP_summa(self) -> int:
        '''
        количество кто вступил в вип по ссылкам с этой датой
        '''
        return sum([link._join_vip for link in self.get_all_links])


    @property
    def _PDP_total_summa(self) -> int:
        '''
        количество подписчиков за этот день
        '''
        qweryset = BaseTable.objects.all()
        if self.date_from is not None:
            qweryset = qweryset.filter(date__date__gte=self.date_from)
        if self.date_to is not None:
            qweryset = qweryset.filter(date__date__lte=self.date_to)
        return qweryset.count()

    


class LinkFilter(models.Model):
    '''
    ссылки для вступления в канал
    '''
    class Meta:
        abstract = False
        verbose_name = "Ссылка (сорт)"
        verbose_name_plural = "Ссылки (сорт)"
    
    invite_link = models.ForeignKey(to=Link, on_delete=models.CASCADE, verbose_name="Ссылка", null=False)

    ads_price = models.IntegerField("Цена Рекламы", default=None, null=True, blank=True, editable=False)
    date = models.DateField("Дата", default=None, null=True, blank=True)

    buyer = models.ForeignKey(
        verbose_name="Закупщик",
        to=Buyer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        default=None,
        editable=False)


    subs = models.IntegerField("Подписалось", default=None, null=True, blank=True, editable=False)
    write = models.IntegerField("Написало", default=None, null=True, blank=True, editable=False)
    join_vip = models.IntegerField("Вступило в VIP", default=None, null=True, blank=True, editable=False)
    subs_price = models.FloatField("Цена ПДП", default=None, null=True, blank=True, editable=False)
    write_price = models.FloatField("Цена Написало", default=None, null=True, blank=True, editable=False)
    join_vip_price = models.FloatField("Цена Вступило в VIP", default=None, null=True, blank=True, editable=False)


    def refresh(self) -> None:
        '''
        '''
        invite_link: Link = self.invite_link
        self.ads_price = invite_link.ads_price
        self.date = invite_link.date
        self.buyer = invite_link.buyer
        self.subs = invite_link._subs
        self.write = invite_link._write
        self.join_vip = invite_link._join_vip
        self.subs_price = invite_link._subs_price
        self.write_price = invite_link._write_price
        self.join_vip_price = invite_link._join_vip_price

        self.save()


    def __str__(self):


        return f"{self.invite_link}"