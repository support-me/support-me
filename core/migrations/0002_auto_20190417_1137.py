# Generated by Django 2.2 on 2019-04-17 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brafitting',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fittings', to='core.Profile'),
        ),
        migrations.AlterField(
            model_name='brafitting',
            name='bust_circumference',
            field=models.BooleanField(blank=True, default=False, help_text='You may measure your bust all the way around. That is ok! Just click here'),
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bra_suggestion', models.CharField(max_length=100, verbose_name='Suggested Bra Types')),
                ('breast_symmetry', models.BooleanField(blank=True, default=True, null=True, verbose_name='Symmetry')),
                ('breast_tissue', models.CharField(choices=[('Teardrop', 'Teardrop'), ('Round', 'Round'), ('None', 'None')], default='None', max_length=30)),
                ('breast_placement', models.CharField(choices=[('Near', 'Near'), ('Far', 'Far')], default='Close', max_length=30)),
                ('bra_wire', models.BooleanField(blank=True, default=True, verbose_name='Underwire')),
                ('bra_padding', models.CharField(choices=[('PushUp', 'Push-Up'), ('Lightly-Lined', 'Lightly-Lined'), ('Unlined', 'Unlined'), ('Removable', 'Removable')], default='Lightly-Lined', max_length=30)),
                ('bra_frame', models.CharField(choices=[('Plunge', 'Plunge'), ('Demi', 'Demi'), ('Full', 'Full')], default='Demi', max_length=30)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggestions', to='core.Profile')),
            ],
        ),
    ]
