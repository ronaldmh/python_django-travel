from django import forms
from django.forms import ModelForm
from .models import *

# Client form 
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'  

# Trip form
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'  
        
# Reservation form
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        
# Traveler form
class TravelerForm(forms.ModelForm):
    class Meta:
        model = Traveler
        fields = '__all__'
        
# Flight form
class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = '__all__'
        
# Hotel form
class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'
        

# Fare form
class FareForm(forms.ModelForm):
    class Meta:
        model = Fare
        fields = '__all__'