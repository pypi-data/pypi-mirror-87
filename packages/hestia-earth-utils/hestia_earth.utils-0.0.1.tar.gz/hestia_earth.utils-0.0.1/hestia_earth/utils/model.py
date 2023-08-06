def find_term_match(values: list, term_id: str, default_val={}):
    return next((v for v in values if v['term']['@id'] == term_id), default_val)


def find_primary_product(cycle: dict):
    products = cycle.get('products', [])
    return next((p for p in products if p.get('primary', False)), products[0]) if len(products) > 0 else None
