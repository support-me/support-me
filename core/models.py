from django.db import models
from django.contrib.auth.models import User
import math

# Create your models here.

class Profile(models.Model):
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # add favorites field?

class BraFitting(models.Model):
    """
    Model for main feature of our site. Getting user input to find bra size.
    """
    bra_size = models.CharField(max_length=10, blank=True, null=True)
    band_measurement = models.DecimalField(help_text='Enter in inches measurment under bust', max_digits=5, decimal_places=2)
    band_size = models.IntegerField(blank=True)
    bust_measurement = models.DecimalField(help_text='Enter measurement in inches for bust', max_digits=5, decimal_places=2)
    cup_size = models.CharField(blank=True)
    bust_circumference = models.BooleanField(help_text='Did you measure all the way around?', blank=True, default=False)
    # http://www.learningaboutelectronics.com/Articles/How-to-create-a-drop-down-list-in-a-Django-form.php
    CURRENTLY_WEARING_CHOICES = (
        ('None', 'None'),
        ('Sports', 'Sports'),
        ('Bralette', 'Bralette'),
        ('PushUp', 'Push-Up'),
        ('LightlyLined', 'Lightly-Lined'),
    )
    currently_wearing = models.CharField(
        choices=CURRENTLY_WEARING_CHOICES,
        default='None'
    )

    def calculate_band_size(self, band_size, band_measurement):
        """
        Calculates band_size based on user input for band_measurent
        """
        band_measurement_int = math.floor(band_measurement)

        if band_measurement_int % 2 == 0:
            self.band_size = (band_measurement_int + 4)
            return self.band_size
        else:
            self.band_size = (band_measurement_int + 5)
            return self.band_size           

    def calculate_cup_size(self, band_size, bust_measurement):
        """
        Calculates cup_size based on bust_measurement and band_size.
        """
        CUP_OPTIONS = {
            0:'AA',
            1:'A',
            2:'B',
            3:'C',
            4:'D',
            5:'DD/E',
            6:'DDD/F',
            7:'G',
            8:'H',
            9:'I',
            10:'J',
            11:'K',
            12:'L',
            13:'M',
        }
        cup_size_number = int(bust_measurement - band_size)
        self.cup_size = CUP_OPTIONS.get(cup_size_number)

