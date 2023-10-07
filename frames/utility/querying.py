from typing import List,Dict,Tuple,Any
import requests


def search_for_food(search_term = "boneless skinless chicken breast") -> Tuple[List[Tuple[str,str]], Dict[str, Dict[str,Any]]]:
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={search_term}&search_simple=1&action=process&json=1"
    response = requests.get(url,timeout=10)

    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        name_id_tuples = []
        products_dict = {}

        lim = min(20, len(products))  # The limit is the minimum between 20 and the actual number of products retrieved
        for i in range(lim):
            product = products[i]
            product_id = product.get('code', 'Unknown ID')
            name = product.get('product_name', 'Unknown Product Name')
            quantity = product.get('quantity', 'Unknown Quantity')
            
            nutriments = product.get('nutriments', {})
            serving_size = product.get('serving_size', '0g')  # Fallback to 100g if serving size is not available.

            energy_serving = nutriments.get('energy_serving', nutriments.get('energy_100g', 0))
            energy_serving_kcal = 'Unknown calories'
            if energy_serving is not None:
                energy_serving_kcal = energy_serving / 4.184  # Convert kJ to kcal
                energy_str = f"{energy_serving_kcal:.2f} kcal"
            else:
                energy_str = 'Unknown Energy Content'
            
            fats_serving = nutriments.get('fat_serving', nutriments.get('fat_100g', 0))
            proteins_serving = nutriments.get('proteins_serving', nutriments.get('proteins_100g', 0))
            carbohydrates_serving = nutriments.get('carbohydrates_serving', nutriments.get('carbohydrates_100g', 0))

            name_id_tuple = (name,product_id)
            name_id_tuples.append(name_id_tuple)
            products_dict[product_id] = {
                'name' : name,
                'quantity' : quantity,
                'nutriments': nutriments,
                'servingsize': serving_size,
                'energy_serving_kcal' : energy_serving_kcal,
                'fats_serving' : fats_serving,
                'proteins_serving' : proteins_serving,
                'carbohydrates_serving' : carbohydrates_serving,
                'sugars_serving' : nutriments.get('sugars_serving',0)
            }
            

            
            # print(f"Name: {name}\nQuantity: {quantity}\nServing Size: {serving_size}\nEnergy per serving: {energy_str}\nFats per serving: {fats_serving}g\nProteins per serving: {proteins_serving}g\nCarbohydrates per serving: {carbohydrates_serving}g\n---")
        if name_id_tuples:
            return (name_id_tuples,products_dict)
        print("No products found from search")
        return ([],{})
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return ([],{})



