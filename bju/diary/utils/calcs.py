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