from django.db import models


class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)    
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=255)    
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.first_name

class Trip(models.Model):
    id_trip = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f"Trip to {self.destination}"

class Reservation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=255)
    service_id = models.PositiveIntegerField()
    reservation_date = models.DateField()

    def __str__(self):
        return f"Reservation for {self.client} - {self.service_type}"
    
    
class Traveler(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    is_adult = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    airline = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    def __str__(self):
        return self.flight_number


class Fare(models.Model):
    service = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    validity_date = models.DateField()

    def __str__(self):
        return f"Fare for {self.service}"
    
    
    
    
# Country - City - Airports - Hotels

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
            return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name   

    
class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    rooms = models.SmallIntegerField()
    services_available = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    photo1 = models.ImageField(upload_to='hotel_photos', blank=True)
    photo2 = models.ImageField(upload_to='hotel_photos', blank=True)
    photo3 = models.ImageField(upload_to='hotel_photos', blank=True)
    photo4 = models.ImageField(upload_to='hotel_photos', blank=True)
    photo5 = models.ImageField(upload_to='hotel_photos', blank=True)
        


class Airport(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    name_airp = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.city}, {self.country}, {self.name_airp} ({self.short_name})"


class Airlines(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name    
    

    