from django.db import models

# Create your models here.

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

    buyer = models.ForeignKey(verbose_name="Закупщик", to=Buyer, null=True, on_delete=models.SET_NULL, default=None)

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
    def _subs_price(self) -> int:
        '''
        цена вступивших по данной ссылке
        '''
        if self.ads_price is not None and self._subs > 0:

            return self.ads_price/self._subs

        return None
    

    @property
    def _write_price(self) -> int:
        '''
        цена тех кто написал по данной ссылке
        '''
        if self.ads_price is not None and self._write > 0:

            return self.ads_price/self._write

        return None

    @property
    def _join_vip_price(self) -> int:
        '''
        цена тех кто вступил в вип по данной ссылке
        '''
        if self.ads_price is not None and self._join_vip > 0:

            return self.ads_price/self._join_vip

        return None


class BaseTable(models.Model):
    '''
    все вступления юзеров по ссылкам
    '''
    class Meta:
        abstract = False
        verbose_name = "База"
        verbose_name_plural = "База"
    
    date = models.DateTimeField("Дата Вступления", auto_now=True)
    user = models.ForeignKey(verbose_name="Юзер", to=User, on_delete=models.CASCADE)
    link = models.ForeignKey(verbose_name="Ссылка", to=Link, on_delete=models.CASCADE)
    write = models.BooleanField("Написал", default=False)
    join_chat = models.BooleanField("Вступил в VIP", default=False)


    def make_write(self) -> None:
        '''
        '''
        if not self.write:
            self.write = True
            self.save(update_fields=["write"])
    

    def make_join_VIP(self) -> None:
        '''
        '''
        if not self.join_chat:
            self.join_chat = True
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
    

    date = models.DateField("Дата", unique=True)


    @property
    def _write(self) -> int:
        '''
        '''
        return BaseTable.objects.filter(
            date__date=self.date,
            write=True,
        ).count()

    