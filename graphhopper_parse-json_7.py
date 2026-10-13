import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "a4e0fa61-126f-4249-bc8a-9a177475a304"  ### Tu API Key de Graphhopper

# Precios promedio de combustible por litro ($ CLP)
PRECIOS_COMBUSTIBLE = {
    "93": 1250.00,
    "95": 1310.00,
    "97": 1380.00,
    "diesel": 1050.00
}
RENDIMIENTO_PROMEDIO_KM_L = 12.0  # Consumo promedio: 12 km por litro

def geocoding(location, key):
    while location == "":
        location = input("Enter the location again: ")
    
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
            
        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name
            
        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Geocode API status: " + str(json_status) + "\nError message: " + json_data.get("message", "Error de geocodificación"))
            
    return json_status, lat, lng, new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles available on Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]
    vehicle = input("Enter a vehicle profile from the list above: ").strip().lower()
    
    if vehicle == "quit" or vehicle == "q":
        break
    elif vehicle not in profile:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")

    # Selección de tipo de bencina/combustible (solo si el vehículo es automóvil)
    tipo_bencina = "95"
    if vehicle == "car":
        print("\nTipos de combustible disponibles: 93, 95, 97, diesel")
        bencina_input = input("Seleccione tipo de bencina: ").strip().lower()
        if bencina_input in PRECIOS_COMBUSTIBLE:
            tipo_bencina = bencina_input
        else:
            print("Tipo no válido. Se usará 95 octanos por defecto.")
        
    loc1 = input("Starting Location: ")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)
    
    loc2 = input("Destination: ")
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)
    
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print("=================================================")
        print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
        print("=================================================")
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            
            # Requerimiento: Distancia en km con 2 decimales
            print("Distance Traveled: {0:.2f} km ({1:.2f} miles)".format(km, miles))
            print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            
            # Requerimiento: Cálculo del precio del viaje con 2 decimales
            if vehicle == "car":
                precio_litro = PRECIOS_COMBUSTIBLE[tipo_bencina]
                litros_consumidos = km / RENDIMIENTO_PROMEDIO_KM_L
                costo_viaje = litros_consumidos * precio_litro
                print("Tipo de Bencina Seleccionada: {0}".format(tipo_bencina))
                print("Precio estimado del viaje: ${0:.2f} CLP (Consumo: {1:.2f} L)".format(costo_viaje, litros_consumidos))
            else:
                print("Precio estimado del viaje: $0.00 CLP (Vehículo no motorizado)")

            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.2f} km / {2:.2f} miles )".format(path, distance / 1000, distance / 1000 / 1.61))
            print("=================================================")
        else:
            print("Error message: " + paths_data.get("message", "Error en consulta de ruta"))
            print("*************************************************")
