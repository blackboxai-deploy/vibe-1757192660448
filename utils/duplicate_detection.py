from fuzzywuzzy import fuzz

def is_duplicate(apartment1, apartment2):
    # TODO: Implement the duplicate detection logic
    address_similarity = fuzz.token_set_ratio(apartment1['address'], apartment2['address'])
    description_similarity = fuzz.token_set_ratio(apartment1['description'], apartment2['description'])

    if address_similarity > 80 and description_similarity > 80:
        return True
    return False
