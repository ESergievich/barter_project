from django.db import models

class CategoryChoices(models.TextChoices):
    CLOTHING = 'clothing', 'Одежда'
    ELECTRONICS = 'electronics', 'Электроника'
    BOOKS = 'books', 'Книги'
    FURNITURE = 'furniture', 'Мебель'
    TOYS = 'toys', 'Игрушки'
    OTHER = 'other', 'Другое'


class ConditionChoices(models.TextChoices):
    NEW = 'new', 'Новый'
    USED = 'used', 'Б/у'


class ProposalStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Ожидает'
    ACCEPTED = 'accepted', 'Принята'
    REJECTED = 'rejected', 'Отклонена'