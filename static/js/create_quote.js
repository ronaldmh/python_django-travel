
    // hour validation
    function validateTime(depTime, arrTime, errorMessage) {
        if (depTime >= arrTime) {
          alert(errorMessage);
          return false;
        }
        return true;
      }
    
      // form validation
      function validateForm() {
        // data
        const origin = document.getElementById("origin").value;
        const destination = document.getElementById("destination").value;
        const startDate = new Date(document.getElementById("start_date").value);
        const endDate = new Date(document.getElementById("end_date").value);
        const numAdults = parseInt(document.getElementById("num_adults").value);
        const numChildren = parseInt(document.getElementById("num_children").value);
        const depTime = document.getElementById("dep_time").value;
        const arrTime = document.getElementById("arr_time").value;
        const depTimeReturn = document.getElementById("dep_time_return").value;
        const arrTimeReturn = document.getElementById("arr_time_return").value;
    
        // valid dates
        const currentDate = new Date();
        currentDate.setHours(0, 0, 0, 0); // Ajustar a la medianoche del día actual
        if (startDate < currentDate || endDate < currentDate) {
          alert("Las fechas deben ser futuras o el día actual.");
          return false;
        }
    
        // cities
        if (origin === destination) {
          alert("La ciudad de destino debe ser diferente a la de origen.");
          return false;
        }
    
        // adults and children
        if (!Number.isInteger(numAdults) || !Number.isInteger(numChildren)) {
          alert("La cantidad de adultos y niños debe ser un número entero.");
          return false;
        }
    
        // hour validation
        if (!validateTime(depTime, arrTime, "La hora de llegada debe ser posterior a la hora de salida del vuelo de ida.")) {
          return false;
        }
    
        if (!validateTime(depTimeReturn, arrTimeReturn, "La hora de salida de vuelta debe ser posterior a la hora de llegada de ida.")) {
          return false;
        }
    
        // return tru if valid
        return true;
      }
    
        
        const destinationSelect = document.getElementById("destination");
        
        const hotelSelect = document.getElementById("hotel");
    
        // get JSON  cities and hotels hide field
        const cityHotelsData = document.getElementById("city-hotels-data").value;
        console.log("Contenido de cityHotelsData:", cityHotelsData); // Agregar esta línea
        const cityHotels = JSON.parse(cityHotelsData);
    
        // hotels by city
        function updateHotels() {
          console.log("Entrando en la función updateHotels()"); // Verificación de inicio de función
          const destination = destinationSelect.value;
          console.log("Ciudad destino seleccionada:", destination); // Verificación de la ciudad destino seleccionada
          hotelSelect.innerHTML = ""; // Limpiar opciones actuales
      
          
          const hotels = cityHotels[destination];
          console.log("Hoteles obtenidos:", hotels); // Verification
          if (hotels) {
            // add hotel options to select
            hotels.forEach((hotel) => {
              const option = document.createElement("option");
              option.value = hotel.id;
              option.textContent = hotel.name;
              hotelSelect.appendChild(option);
            });
          } else {
            // Mdisplay message
            const option = document.createElement("option");
            option.value = "";
            option.textContent = "No hay hoteles disponibles";
            hotelSelect.appendChild(option);
          }
        }
    
        // Event
        destinationSelect.addEventListener("change", updateHotels);
    
        updateHotels();