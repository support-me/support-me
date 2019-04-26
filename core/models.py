from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import math
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AnonymousUser
# Create your models here.

class Profile(models.Model):
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    site_user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=True, blank=True)
    # add favorites field?

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(site_user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.site_user.username
    

class BraFitting(models.Model):
    """
    Model for main feature of our site. Getting user input to find bra size.
    """
    fitting_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='fittings', blank=True, null=True)
    bra_size = models.CharField(max_length=10, blank=True, null=True)
    band_measurement = models.DecimalField(help_text='Enter in inches measurment under bust', max_digits=5, decimal_places=2)
    band_size = models.IntegerField(blank=True)
    bust_measurement = models.DecimalField(help_text='Enter measurement in inches for bust', max_digits=5, decimal_places=2)
    cup_size = models.CharField(max_length=10, blank=True)
    date_sized = models.DateField(verbose_name='Date of Bra Fitting', auto_now_add=True, null=True, blank=True)
    # http://www.learningaboutelectronics.com/Articles/How-to-create-a-drop-down-list-in-a-Django-form.php


    class Meta:
        ordering = ['date_sized']


    def save(self, fitting_user, currently_wearing, band_measurement, bust_measurement, bust_circumference, *args, **kwargs):
        self.band_size = self.calculate_band_size(band_measurement)
        self.bust_measurement = self.calculate_circumference(currently_wearing, bust_circumference, bust_measurement)
        self.cup_size = self.calculate_cup_size(self.band_size)
        self.calculate_bra_size(self.band_size, self.cup_size)
        self.fitting_user = fitting_user
        super().save(*args, **kwargs)

    CURRENTLY_WEARING_CHOICES = (
        ('None', 'No Bra'),
        ('Unlined', 'Unlined Bra'),
        ('SportsBra', 'Sports Bra'),
        ('Bralette', 'Bralette'),
        ('PushUp', 'Push-Up Bra'),
        ('LightlyLined', 'Lightly-Lined Bra'),
    )
    currently_wearing = models.CharField(
        max_length=20,
        choices=CURRENTLY_WEARING_CHOICES,
        default='None',
    )

    BUST_CIRCUMFERENCE_CHOICES = (
        ('Half', 'Half Way Around'),
        ('AllWay', 'All The Way Around'),
    )
    bust_circumference = models.CharField(
        max_length=25,
        choices=BUST_CIRCUMFERENCE_CHOICES,
        default='Half',
    )

    def calculate_band_size(self, band_measurement):
        """
        Calculates band_size based on user input for band_measurent
        """
        band_measurement_int = math.floor(float(band_measurement))

        if band_measurement_int % 2 == 0:
            self.band_size = (band_measurement_int + 4)
        else:
            self.band_size = (band_measurement_int + 5)
        return self.band_size
    

    def calculate_circumference(self, currently_wearing, bust_circumference, bust_measurement):
        if self.bust_measurement:
            self.bust_measurement = round(float(bust_measurement))
        if bust_circumference == 'Half':
            self.bust_measurement = self.bust_measurement * 2
        # Account for what is currently being worn below    
        if currently_wearing in ['None', 'Unlined', 'Bralette', 'SportsBra']:
            self.bust_measurement = (self.bust_measurement + 1)
        elif currently_wearing == 'PushUp':
            self.bust_measurement = (self.bust_measurement - 1)
        else:
            self.bust_measurement = self.bust_measurement
        return self.bust_measurement


    def calculate_cup_size(self, band_size):
        """
        Calculates cup_size based on bust_measurement and band_size.
        """
        CUP_OPTIONS = {
            -6:'AA',
            -5:'AA',
            -4:'AA',
            -3:'AA',
            -2:'AA',
            -1:'AA',
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
            14:'N',
            15:'O',
        }
        # https://stackoverflow.com/questions/11041405/why-dict-getkey-instead-of-dictkey
        cup_size_number = self.bust_measurement - int(band_size)
        self.cup_size = CUP_OPTIONS.get(cup_size_number)
        return self.cup_size 


    def calculate_bra_size(self, band_size, cup_size):
        self.bra_size = (f'{band_size}{cup_size}')


    def __str__(self):
        return self.bra_size


    def get_absolute_url(self):
        # enter name of html as argument here... calling the html 'fitting' for now
        return reverse('fitting')
    
class Suggestion(models.Model):
    """
    Model for creating suggestions based on bra size and questions from SuggestionForm.
    """
    fitting_session = models.ForeignKey(to=BraFitting, on_delete=models.CASCADE, related_name='suggestions', blank=True)
    bra_suggestion = models.CharField(verbose_name='Suggested Bra Types', max_length=100)
    
    SHAPE_CHOICES = (
        ('Teardrop', 'Teardrop'),
        ('Round', 'Round'),
        ('None', 'Other'),
    )
    breast_shape = models.CharField(max_length=30, choices=SHAPE_CHOICES, default='None')

    PLACEMENT_CHOICES = (
        ('Near', 'Near'),
        ('Far', 'Far'),
    )
    breast_placement = models.CharField(max_length=30, choices=PLACEMENT_CHOICES, default='Near')

    WIRE_CHOICES = (
        ('Underwire', 'Underwire'),
        ('Wireless', 'Wireless')
    )
    bra_wire = models.CharField(max_length=20, choices=WIRE_CHOICES, default='Underwire')

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


    def save(self, fitting_session, breast_shape, bra_padding, *args, **kwargs):
        self.fitting_session = fitting_session
        self.bra_suggestion = self.get_suggestion(breast_shape, bra_padding)
        super().save(*args, **kwargs)
    

    def get_suggestion(self, breast_shape, bra_padding):
        if breast_shape in ['None', 'Round']:
            self.bra_frame = 'Full'
        else:
            self.bra_frame = 'Demi'
        self.bra_suggestion = f'{self.bra_frame} {bra_padding}'
        return self.bra_suggestion

    def __str__(self):
        return self.bra_suggestion
    
        
class Resource(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    url = models.URLField(blank=False)
    category_type = models.CharField(max_length=100, default='All')

    def __str__(self):
        return self.title
