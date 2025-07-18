from django.contrib.auth.models import User
from django.db import models
from django.db.models import SET_NULL, CASCADE, BooleanField
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Flat(models.Model):
    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True)

    description = models.TextField('Текст объявления', blank=True)
    price = models.IntegerField('Цена квартиры', db_index=True)

    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True)
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное')
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4')
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж')

    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True)
    living_area = models.IntegerField(
        'количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True)

    has_balcony = models.BooleanField(
        'Наличие балкона',
        null=True, blank=True,
        db_index=True
    )

    active = models.BooleanField('Активно ли объявление', db_index=True)
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True)

    new_building = models.BooleanField(
        null=True,
        db_index=True,
        verbose_name='Является ли новостройкой'
    )
    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name="liked_flats",
        verbose_name='Количество лайков'
    )

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'


class Complaint(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        related_name='complaints',
    )
    flat = models.ForeignKey(
        Flat,
        on_delete=CASCADE,
        related_name='complaints',
    )
    complaint_text = models.TextField(max_length=2000)

    def __str__(self):
        return f'Жалоба от {self.complaint_author} на квартиру {self.flat}'


class Owner(models.Model):
    owner = models.CharField('ФИО владельца', max_length=200)
    owner_pure_phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name='Номер владельца в формате +7ХХХХХХХХХХ'
    )
    flats = models.ManyToManyField(
        "Flat",
        verbose_name="Квартиры в собственности",
        related_name="owners",
        blank=True
    )

    def __str__(self):
        return f'Собственник {self.owner}'
