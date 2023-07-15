import Levenshtein

def suggest_words(input_word, valid_words):
    suggestions = []
    for word in valid_words:
        distance = Levenshtein.distance(input_word, word)
        if distance <= 2:  # Adjust the threshold as needed
            suggestions.append((word, distance))
    suggestions.sort(key=lambda x: x[1])  # Sort suggestions by distance
    return [word for word, _ in suggestions]

def load_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()
    return words

# Example usage
valid_words = load_dictionary('bangla_words.txt')  # Replace with your own Bangla dictionary file path
input_word = 'কমপটার'  # Misspelled Bangla word

suggested_words = suggest_words(input_word, valid_words)
print(suggested_words)
