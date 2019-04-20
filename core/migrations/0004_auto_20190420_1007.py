# Generated by Django 2.2 on 2019-04-20 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190417_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('ur', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='brafitting',
            name='currently_wearing',
            field=models.CharField(choices=[('None', 'None'), ('SportsBra', 'Sports Bra'), ('Bralette', 'Bralette'), ('PushUp', 'Push-Up'), ('LightlyLined', 'Lightly-Lined')], default='None', max_length=20),
        ),
    ]