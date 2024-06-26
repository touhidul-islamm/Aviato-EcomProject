# Generated by Django 4.2.11 on 2024-04-21 06:38

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0004_remove_order_ordered_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, default=None, editable=False, null=True, populate_from='name', unique=True),
        ),
    ]
