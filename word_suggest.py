import Levenshtein

def suggest_words(input_word, valid_words):
    suggestions = []
    for word in valid_words:
        distance = Levenshtein.distance(input_word, word)
        if distance <= 2:  # Adjust the threshold as needed
            suggestions.append((word, distance))
    suggestions.sort(key=lambda x: x[1])  # Sort suggestions by distance
    return [word for word, _ in suggestions]

valid_words = ["আম", "কলা", "কমলা", "আঙ্গুর", "পেঁপে", "আনারস"]
input_word = "আপেল"  # Misspelled word

suggested_words = suggest_words(input_word, valid_words)
print(suggested_words)
