from django.db import models
from django.urls import reverse
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
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='fittings')
    bra_size = models.CharField(max_length=10, blank=True, null=True)
    band_measurement = models.DecimalField(help_text='Enter in inches measurment under bust', max_digits=5, decimal_places=2)
    band_size = models.IntegerField(blank=True)
    bust_measurement = models.DecimalField(help_text='Enter measurement in inches for bust', max_digits=5, decimal_places=2)
    cup_size = models.CharField(max_length=10, blank=True)
    bust_circumference = models.BooleanField(help_text='You may measure your bust all the way around. That is ok! Just click here', blank=True, default=False)
    # http://www.learningaboutelectronics.com/Articles/How-to-create-a-drop-down-list-in-a-Django-form.php
    CURRENTLY_WEARING_CHOICES = (
        ('None', 'None'),
        ('Sports', 'Sports'),
        ('Bralette', 'Bralette'),
        ('PushUp', 'Push-Up'),
        ('LightlyLined', 'Lightly-Lined'),
    )
    currently_wearing = models.CharField(
        max_length=20,
        choices=CURRENTLY_WEARING_CHOICES,
        default='None',
    )

    def calculate_band_size(self, band_measurement):
        """
        Calculates band_size based on user input for band_measurent
        """
        band_measurement_int = math.floor(band_measurement)

        if band_measurement_int % 2 == 0:
            self.band_size = (band_measurement_int + 4)
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
        # https://stackoverflow.com/questions/11041405/why-dict-getkey-instead-of-dictkey
        cup_size_number = int(bust_measurement - band_size)
        self.cup_size = CUP_OPTIONS.get(cup_size_number)
        return self.cup_size

    def calculate_bra_size(self, band_size, cup_size):
        self.bra_size = (f'{band_size} {cup_size}')

    def __str__(self):
        return self.bra_size

    def get_absolute_url(self):
        # enter name of html as argument here... calling the html 'fitting' for now
        return reverse('fitting')
    
class Suggestion(models.Model):
    """
    Model for creating suggestions based on bra size and questions from SuggestionForm.
    """
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='suggestions')
    bra_suggestion = models.CharField(verbose_name='Suggested Bra Types', max_length=100)
    breast_symmetry = models.BooleanField(verbose_name='Symmetry', blank=True, null=True, default=True)
    
    SHAPE_CHOICES = (
        ('Teardrop', 'Teardrop'),
        ('Round', 'Round'),
        ('None', 'None'),
    )
    breast_tissue = models.CharField(max_length=30, choices=SHAPE_CHOICES, default='None')

    PLACEMENT_CHOICES = (
        ('Near', 'Near'),
        ('Far', 'Far')
    )
    breast_placement = models.CharField(max_length=30, choices=PLACEMENT_CHOICES, default='Close')
    bra_wire = models.BooleanField(verbose_name='Underwire', blank=True, default=True)

    BRA_PADDING_CHOICES = (
        ('PushUp', 'Push-Up'),
        ('Lightly-Lined', 'Lightly-Lined'),
        ('Unlined', 'Unlined'),
        ('Removable', 'Removable'),
    )
    bra_padding = models.CharField(max_length=30, choices=BRA_PADDING_CHOICES, default='Lightly-Lined')

    BRA_FRAME_CHOICES = (
        ('Plunge', 'Plunge'),
        ('Demi', 'Demi'),
        ('Full', 'Full'),
    )
    bra_frame = models.CharField(max_length=30, choices=BRA_FRAME_CHOICES, default='Demi')
