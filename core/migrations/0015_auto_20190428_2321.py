# Generated by Django 2.2 on 2019-04-29 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_resource_category_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='bra_padding',
            field=models.CharField(choices=[('Lightly-Lined', 'Lightly-Lined'), ('PushUp', 'Push-Up'), ('Unlined', 'Unlined'), ('Removable', 'Removable')], default='Lightly-Lined', max_length=30),
        ),
    ]
