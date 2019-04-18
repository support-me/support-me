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
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='fittings', null=True, blank=True)
    bra_size = models.CharField(max_length=10, blank=True, null=True)
    band_measurement = models.DecimalField(help_text='Enter in inches measurment under bust', max_digits=5, decimal_places=2)
    band_size = models.IntegerField(blank=True)
    bust_measurement = models.DecimalField(help_text='Enter measurement in inches for bust', max_digits=5, decimal_places=2)
    cup_size = models.CharField(max_length=10, blank=True)
    bust_circumference = models.BooleanField(help_text='You may measure your bust all the way around. That is ok! Just click here', blank=True, default=False)
    date_sized = models.DateField(verbose_name='Date of Bra Fitting', auto_now_add=True, null=True, blank=True)
    # http://www.learningaboutelectronics.com/Articles/How-to-create-a-drop-down-list-in-a-Django-form.php
    class Meta:
        ordering = ['date_sized']

    def save(self, currently_wearing, band_measurement, bust_measurement, bust_circumference, *args, **kwargs):
        self.band_size = self.calculate_band_size(band_measurement)
        self.bust_measurement = self.calculate_circumference(currently_wearing, bust_circumference, bust_measurement)
        self.cup_size = self.calculate_cup_size(self.band_size)
        self.calculate_bra_size(self.band_size, self.cup_size)

        super().save(*args, **kwargs)

    CURRENTLY_WEARING_CHOICES = (
        ('None', 'None'),
        ('SportsBra', 'Sports Bra'),
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
        band_measurement_int = math.floor(int(band_measurement))

        if band_measurement_int % 2 == 0:
            self.band_size = (band_measurement_int + 4)
        else:
            self.band_size = (band_measurement_int + 5)
        return self.band_size
    
    def calculate_circumference(self, currently_wearing, bust_circumference, bust_measurement):
        self.bust_measurement = int(bust_measurement)
        if not bust_circumference:
            self.bust_measurement = self.bust_measurement * 2
        # Account for what is currently being worn below    
        if currently_wearing in ['None', 'Bralette', 'SportsBra']:
            # breakpoint()
            self.bust_measurement = (self.bust_measurement + 1)
        elif currently_wearing == 'PushUp':
            # breakpoint()
            self.bust_measurement = (self.bust_measurement - 1)
        else:
            self.bust_measurement = self.bust_measurement
        return self.bust_measurement

    def calculate_cup_size(self, band_size):
        """
        Calculates cup_size based on bust_measurement and band_size.
        """
        CUP_OPTIONS = {
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
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='suggestions', null=True, blank=True)
    bra_suggestion = models.CharField(verbose_name='Suggested Bra Types', max_length=100)
    breast_symmetry = models.BooleanField(verbose_name='Symmetry', blank=True, default=True)
    
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

    def save(self, *args, **kwargs):
        self.bra_suggestion = self.get_suggestion(self.breast_symmetry, self.breast_tissue, self.breast_placement, self.bra_padding, self.bra_frame)
        super().save(*args, **kwargs)

    def get_suggestion(self, breast_symmetry, breast_tissue, breast_placement, bra_padding, bra_frame):
        self.bra_suggestion = f'{bra_padding} + {bra_frame}'
        if self.breast_symmetry in ['Yes', 'Unknown']:
            print('this aint working')
            if self.breast_tissue == 'Teardrop':
                if self.self.breast_placement == 'Near':
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Demi'
                    print(bra_padding, bra_frame)
                else:
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Demi'
                    print(bra_padding, bra_frame)
                    return f'{bra_padding} + {bra_frame}'
            elif self.breast_tissue == 'Round':
                if self.breast_placement == 'Near':
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Plunge'
                    print(bra_padding, bra_frame)
                else:
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Plunge'
                    print(bra_padding, bra_frame)
            else:
                if self.breast_placement == 'Near':
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Plunge'
                    print(bra_padding, bra_frame)
                else:
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Plunge'
                    print(bra_padding, bra_frame)
        else:
            if self.breast_tissue == 'Teardrop':
                if self.breast_placement == 'Near':
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Demi'
                    print(bra_padding, bra_frame)
                else:
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Demi'
                    print(bra_padding, bra_frame)
            elif self.breast_tissue == 'Round':
                if self.breast_placement == 'Near':
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Plunge'
                    print(bra_padding, bra_frame)
                else:
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Plunge'
                    print(bra_padding, bra_frame)
            else:
                if self.breast_placement == 'Near':
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Plunge'
                    print(bra_padding, bra_frame)
                else:
                    self.bra_padding = 'PushUp'
                    self.bra_frame = 'Plunge'
                    print(bra_padding, bra_frame)
        return self.bra_suggestion
