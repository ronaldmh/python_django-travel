import pandas as pd
import json
import os
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .models import *
from .forms import *
from django.core import serializers

from django.contrib import messages



def index(request):
    return render(request, 'clients/index.html')

def home(request):
    return render(request, 'clients/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Reemplaza 'home' con la URL a la que quieres redirigir después del inicio de sesión exitoso.
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'clients/index.html')  # Reemplaza 'login.html' con la plantilla de inicio de sesión que quieras utilizar.


def logout_view(request):
    logout(request)
    return redirect('index')

def client_list(request):
    clients = Client.objects.all()
    #cars = Car.objects.all()
    #form = SearchClientForm()
    return render(request, 'clients/client_list.html', {'clients': clients})


def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            # Extract client data from form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            
            # Search for client with matching email and phone number
            query = Q(email__exact=email.strip()) | Q(phone_number__exact=phone_number.strip())
            existing_client = Client.objects.filter(query).first()
            
            if existing_client:
                # Client already exists, show error message
                form.add_error('email', 'Client with this email/phone already exists.')
            else:
                # Client doesn't exist, save client to the database
                client = form.save()
                                
                # Redirect to home page
                return render(request, 'clients/home.html', {'form': form})
    else:
        form = ClientForm()
    
    # Render registration page with form
    return render(request, 'clients/register.html', {'form': form})



def client_detail(request, id_client):
    client = get_object_or_404(Client, pk=id_client)    
    services = Services.objects.filter(id_client=client)
    return render(request, 'clients/client_detail.html', {'client': client, 'cars': cars, 'services': services})
            
        
#view services

def services_view(request):
    services = Services.objects.all().select_related('id_client')
    context = {'services': services}
    return render(request, 'clients/services_view.html', context)



# Ok
def create_service(request, id_client):
    
    client = get_object_or_404(Client, pk=id_client)
    car = Car.objects.get(id_client=client)
    
    if request.method == 'POST':
        
        form = NewServiceForm(request.POST)
        
        if form.is_valid():
            # Crear un nuevo objeto Services utilizando los datos del formulario y el ID del cliente
            service = form.save(commit=False)
            service.id_car = car
            service.id_client = client
            service.save()
            
            # Mostrar un mensaje de confirmación al usuario
            messages.success(request, 'Service created successfully.')
            
            return redirect('client_detail', id_client=id_client)

           
    else:
        form = NewServiceForm()
    
    return render(request, 'clients/create_service.html', {'form': form, 'client': client, 'car': car})



def create_quote(request):
    if request.method == 'POST':
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        num_adults = int(request.POST.get('num_adults', 0))
        num_children = int(request.POST.get('num_children', 0))
        
        airline_departure = request.POST.get('airline_departure')
        dep_time = request.POST.get('dep_time')
        arr_time = request.POST.get('arr_time')
        
        airline_return = request.POST.get('airline_return')
        dep_time_return = request.POST.get('dep_time_return')
        arr_time_return = request.POST.get('arr_time_return')
        
        trip_cost = float(request.POST.get('trip_cost', 0))
        total_value = float(request.POST.get('total_value', 0))
        
        cost_by_person = total_value / (num_adults + num_children )    
        
        
        hotel_id = request.POST.get('hotel')
        
        # Obtén la información del hotel solo si se ha seleccionado uno
        if hotel_id:
            # Buscar el hotel en la base de datos o devolver None si no existe
            hotel = get_object_or_404(Hotel, pk=hotel_id)

            # Obtén la ruta de la carpeta de imágenes del hotel
            hotel_images_folder = f'static/images/hotel/{hotel_id}'

            try:
                # Intenta obtener la lista de rutas completas de las imágenes del hotel
                hotel_images = [f'{hotel_images_folder}/{image_filename}' for image_filename in os.listdir(hotel_images_folder)]
            except OSError as e:
                # Captura el error en caso de que ocurra
                print(f"Error al obtener las imágenes del hotel: {e}")
                hotel_images = []

            # Remover la palabra "static" de las rutas de imágenes
            hotel_images = [image_path.split('static/')[1] for image_path in hotel_images]

            # Serializar el objeto Hotel a JSON
            hotel_json = serializers.serialize('json', [hotel])

            # Convertir el JSON a un diccionario
            hotel_data = json.loads(hotel_json)
            hotel_dict = hotel_data[0]['fields']
        else:
            # Si no se selecciona un hotel, establecer hotel y hotel_images como None
            hotel = None
            hotel_dict = {}
            hotel_images = []

        
        # Diccionario de contexto
        context = {
            'origin': origin,
            'destination': destination,
            'start_date': start_date,
            'end_date': end_date,
            'num_adults': num_adults,
            'num_children': num_children,
            'airline_departure': airline_departure,
            'dep_time': dep_time,
            'arr_time': arr_time,
            'airline_return': airline_return,
            'dep_time_return': dep_time_return,
            'arr_time_return': arr_time_return,
            'hotel': hotel_dict,
            'hotel_images': hotel_images,
            'trip_cost' : trip_cost,
            'total_value' : total_value,
            'cost_by_person': cost_by_person          
        }
        
        print(cost_by_person)

        # Guardar el diccionario de contexto en la sesión
        request.session['quote_context'] = context

        # Renderizar la plantilla 'quote.html' con el mismo diccionario de contexto
        return render(request, 'clients/quote.html', context)
    else:
        # Obtener datos fijos de la base de datos: ciudades, hoteles, vuelos y aerolíneas
        cities = City.objects.all()
        airlines = Airlines.objects.all()
        city_hotels = {}
        
        for city in cities:
            hotels = Hotel.objects.filter(city=city)
            city_hotels[city.name] = list(hotels.values('id', 'name'))
            
        print(city_hotels)

        context = {
            'cities': cities,
            'airlines': airlines,
            'city_hotels_json': json.dumps(city_hotels),            
        }

        return render(request, 'clients/create_quote.html', context)

   

def quote_view(request):
    # Obtén el diccionario de contexto desde la vista original
    context = request.session.get('quote_context', {})

    return render(request, 'clients/quote.html', context)

    

def quote2_view(request):
    # Obtén el diccionario de contexto desde la vista original
    context = request.session.get('quote_context', {})

    return render(request, 'clients/quote2.html', context)



def quote3_view(request):
    # Obtén el diccionario de contexto desde la vista original
    context = request.session.get('quote_context', {})

    return render(request, 'clients/quote3.html', context)



def quote4_view(request):
    # Obtén el diccionario de contexto desde la vista original
    context = request.session.get('quote_context', {})

    return render(request, 'clients/quote4.html', context)


def quote5_view(request):
    # Obtén el diccionario de contexto desde la vista original
    context = request.session.get('quote_context', {})

    return render(request, 'clients/quote5.html', context)



def client_detail(request, id_client):
    client = get_object_or_404(Client, pk=id_client)
    return render(request, 'clients/client_detail.html', {'client': client})




# VISTAS DE CARGA DE DATOS

def load_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        try:
            df = pd.read_csv(csv_file)

            for _, row in df.iterrows():
                model_csv = Airport(
                    city=row.get('campo1', ''),
                    country=row.get('campo2', ''),
                    name_airp=row.get('campo3', ''),
                    short_name=row.get('campo4', ''),
                )
                model_csv.save()

            messages.success(request, "Archivo CSV cargado exitosamente.")
        
        except pd.errors.EmptyDataError:
            messages.error(request, "El archivo CSV está vacío.")
        except KeyError as e:
            messages.error(request, f"Campo '{e.args[0]}' no encontrado en el archivo CSV.")
        except Exception as e:
            messages.error(request, f"Error al cargar el archivo CSV: {str(e)}")
        
    return render(request, 'clients/load_csv.html')


# views.py


def load_cities(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        try:
            df = pd.read_csv(csv_file, encoding='utf-8', header=None)  # Abre el archivo en modo de texto y omite el encabezado

            # Iterar sobre el DataFrame y crear objetos City a partir de los datos del CSV
            for _, row in df.iterrows():
                city_name = row[0]
                country_name = row[1]

                # Verificar si la ciudad ya existe en la base de datos
                city, created = City.objects.get_or_create(name=city_name, country=country_name)

            # Mostrar mensaje de éxito
            success_message = "Ciudades y países cargados exitosamente."
            return render(request, 'clients/load_cities.html', {'success_message': success_message})
        
        except pd.errors.EmptyDataError:
            error_message = "El archivo CSV está vacío."
        except KeyError as e:
            error_message = f"Campo '{e.args[0]}' no encontrado en el archivo CSV."
        except Exception as e:
            error_message = f"Error al cargar el archivo CSV: {str(e)}"
        
        return render(request, 'clients/load_cities.html', {'error_message': error_message})

    return render(request, 'clients/load_cities.html')



def load_airlines(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        try:
            df = pd.read_csv(csv_file, encoding='utf-8', header=None)  # Omitir el encabezado del archivo CSV

            # Iterar sobre el DataFrame y crear objetos Airline a partir de los datos del CSV
            for _, row in df.iterrows():
                airline_name = row[0]

                # Verificar si la aerolínea ya existe en la base de datos
                airline, created = Airlines.objects.get_or_create(name=airline_name)

            # Mostrar mensaje de éxito
            success_message = "Aerolíneas cargadas exitosamente."
            return render(request, 'clients/load_airlines.html', {'success_message': success_message})
        
        except pd.errors.EmptyDataError:
            error_message = "El archivo CSV está vacío."
        except Exception as e:
            error_message = f"Error al cargar el archivo CSV: {str(e)}"
        
        return render(request, 'clients/load_airlines.html', {'error_message': error_message})

    return render(request, 'clients/load_airlines.html')




def load_hotels(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        try:
            df = pd.read_csv(csv_file, encoding='utf-8')

            # Iterar sobre el DataFrame y crear objetos Hotel a partir de los datos del CSV
            for _, row in df.iterrows():
                hotel_name = row['name']
                hotel_location = row['location']
                hotel_category = row['category']
                hotel_rooms = int(row['rooms'])
                hotel_services = row['services_available']
                hotel_city_name = row['city']  # Obtener el nombre de la ciudad del CSV

                # Verificar si la ciudad ya existe en la base de datos
                city, created = City.objects.get_or_create(name=hotel_city_name, country='')  # Puedes asignar un país si está disponible en el CSV

                # Crear el objeto Hotel y asignar la ciudad correspondiente
                hotel, hotel_created = Hotel.objects.get_or_create(
                    name=hotel_name,
                    location=hotel_location,
                    category=hotel_category,
                    rooms=hotel_rooms,
                    services_available=hotel_services,
                    city=city  # Asignar el objeto City al campo city de Hotel
                )

            # Mostrar mensaje de éxito
            success_message = "Hoteles cargados exitosamente."
            return render(request, 'clients/load_hotels.html', {'success_message': success_message})
        
        except pd.errors.EmptyDataError:
            error_message = "El archivo CSV está vacío."
        except Exception as e:
            error_message = f"Error al cargar el archivo CSV: {str(e)}"
        
        return render(request, 'clients/load_hotels.html', {'error_message': error_message})

    return render(request, 'clients/load_hotels.html')
