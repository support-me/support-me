# Generated by Django 2.2 on 2019-04-24 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190421_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brafitting',
            name='currently_wearing',
            field=models.CharField(choices=[('None', 'No Bra'), ('Unlined', 'Unlined Bra'), ('SportsBra', 'Sports Bra'), ('Bralette', 'Bralette'), ('PushUp', 'Push-Up Bra'), ('LightlyLined', 'Lightly-Lined Bra')], default='None', max_length=20),
        ),
    ]
