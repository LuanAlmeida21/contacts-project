import os
import sys
from datetime import datetime
from pathlib import Path
from random import choice

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBERS_CONTACTS = 1000

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ = False

django.setup()


if __name__ == '__main__':
    import faker

    from contact.models import Category, Contact

    Contact.objects.all().delete()
    Category.objects.all().delete()

    fake = faker.Faker('PT-br')
    categories = ['Family', 'Friend', 'Acquaintance']

    django_categories = [Category(name=name) for name in categories]

    for category in django_categories:
        category.save()

    django_contacts = []

    for _ in range(NUMBERS_CONTACTS):
        profile = fake.profile()
        email = profile['mail']
        phone = fake.phone_number()
        first_name, last_name = profile['name'].split(' ', 1)
        description = fake.text(max_nb_chars=100)
        created_contact: datetime = fake.date_this_year()
        category = choice(django_categories)

        django_contacts.append(
            Contact(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                description=description,
                created_contact=created_contact,
                category=category,
            )
        )

    if len(django_contacts) > 0:
        Contact.objects.bulk_create(django_contacts)
