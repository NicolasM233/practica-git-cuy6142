import requests

while True:
    pokemon = input("\nIngrese el nombre de un Pokémon (o 'q' para salir): ").strip().lower()
    
    if pokemon == "q" or pokemon == "quit":
        print("Saliendo de la aplicación.")
        break
        
    if not pokemon:
        print("Por favor, ingrese un nombre válido.")
        continue

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        print(f"\n=========================================")
        print(f"INFORMACIÓN DE: {datos['name'].upper()}")
        print(f"=========================================")
        print(f"ID: {datos['id']}")
        print(f"Altura: {datos['height']} decímetros")
        print(f"Peso: {datos['weight']} hectogramos")
        
        habilidades = [h['ability']['name'] for h in datos['abilities']]
        print(f"Habilidades: {', '.join(habilidades)}")
        
        tipos = [t['type']['name'] for t in datos['types']]
        print(f"Tipo(s): {', '.join(tipos)}")
        print(f"=========================================")
    else:
        print(f"Error {respuesta.status_code}: No se encontró el Pokémon '{pokemon}'. Intente de nuevo.")
