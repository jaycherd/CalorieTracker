import requests

search_term = "boneless skinless chicken breast"
url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={search_term}&search_simple=1&action=process&json=1"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    products = data.get('products', [])
    
    lim = min(10, len(products))  # The limit is the minimum between 20 and the actual number of products retrieved
    for i in range(lim):
        product = products[i]
        name = product.get('product_name', 'Unknown Product Name')
        quantity = product.get('quantity', 'Unknown Quantity')
        
        nutriments = product.get('nutriments', {})
        serving_size = product.get('serving_size', '100g')  # Fallback to 100g if serving size is not available.

        energy_serving = nutriments.get('energy_serving', nutriments.get('energy_100g', None))
        if energy_serving is not None:
            energy_serving_kcal = energy_serving / 4.184  # Convert kJ to kcal
            energy_str = f"{energy_serving_kcal:.2f} kcal"
        else:
            energy_str = 'Unknown Energy Content'
        
        fats_serving = nutriments.get('fat_serving', nutriments.get('fat_100g', 'Unknown'))
        proteins_serving = nutriments.get('proteins_serving', nutriments.get('proteins_100g', 'Unknown'))
        carbohydrates_serving = nutriments.get('carbohydrates_serving', nutriments.get('carbohydrates_100g', 'Unknown'))
        
        print(f"Name: {name}\nQuantity: {quantity}\nServing Size: {serving_size}\nEnergy per serving: {energy_str}\nFats per serving: {fats_serving}g\nProteins per serving: {proteins_serving}g\nCarbohydrates per serving: {carbohydrates_serving}g\n---")
else:
    print(f"Failed to retrieve data: {response.status_code}")


