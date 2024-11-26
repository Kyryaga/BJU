def calculate_total_bju(enriched_products):
    total_bju = {
        'fats': 0,
        'carbos': 0,
        'prots': 0,
        'calories': 0,
    }
    
    for entry in enriched_products:
        total_bju['fats'] += entry['fats']
        total_bju['carbos'] += entry['carbos']
        total_bju['prots'] += entry['prots']
        total_bju['calories'] += entry['calories']

    return total_bju

def calculate_each_product_bju(products):
    enriched_products = []

    for entry in products:
        enriched_products.append({
            'entry_id': entry.id,
            'product': entry.product,
            'weight': entry.weight,
            'calories': entry.product.calories * entry.weight / 100,
            'prots': entry.product.prots * entry.weight / 100,
            'fats': entry.product.fats * entry.weight / 100,
            'carbos': entry.product.carbos * entry.weight / 100,
        })

    return enriched_products

def calc_rsk(enriched_products, rsk):
    for product_entry in enriched_products:
        product_entry['rsk'] = product_entry['calories'] / rsk * 100
