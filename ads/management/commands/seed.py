from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.apps import apps
from ads.models import Ad, ExchangeProposal, CategoryChoices, ConditionChoices, ProposalStatusChoices
from faker import Faker
import random

fake = Faker()
User = get_user_model()


def clear_database():
    for model in apps.get_models():
        model.objects.all().delete()


class Command(BaseCommand):
    help = "Заполняет тестовыми данными"

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Количество пользователей')
        parser.add_argument('--cleardb', action='store_true', help='Очистить базу данных перед заполнением')

    def handle(self, *args, **options):
        user_count = options['users']
        if options['cleardb']:
            clear_database()

        self.stdout.write(self.style.NOTICE("Создаём пользователей и объявления..."))

        all_ads = []
        users = []

        for num in range(1, user_count + 1):
            user = User.objects.create(
                username=f"user_{num}",
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=make_password("barter_1234"),
            )
            users.append(user)

            for _ in range(10):
                ad = Ad.objects.create(
                    user=user,
                    title=fake.catch_phrase(),
                    description=fake.text(max_nb_chars=200),
                    image_url=fake.image_url(),
                    category=random.choice([choice[0] for choice in CategoryChoices.choices]),
                    condition=random.choice([choice[0] for choice in ConditionChoices.choices]),
                )
                all_ads.append(ad)

        self.stdout.write(self.style.NOTICE("Создаём предложения обмена..."))

        for user in users:
            user_ads = Ad.objects.filter(user=user)
            other_ads = Ad.objects.exclude(user=user)

            for _ in range(5):
                if not user_ads or not other_ads:
                    continue

                ad_sender = random.choice(user_ads)
                ad_receiver = random.choice(other_ads)

                ExchangeProposal.objects.create(
                    ad_sender=ad_sender,
                    ad_receiver=ad_receiver,
                    comment=random.choice([fake.sentence(), ""]),
                    status=random.choice([choice[0] for choice in ProposalStatusChoices.choices]),
                )

        self.stdout.write(
            self.style.SUCCESS(f"Успешно создано {user_count} пользователей с объявлениями и предложениями обмена"))
