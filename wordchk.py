def check_word_in_file(word, filename):
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if word in line:
                return True
    return False

# Example usage
word_to_check = input("Enter a word to check: ")
file_to_search = "bangla_words.txt"  # Replace with your file name or path

if check_word_in_file(word_to_check, file_to_search):
    print("The word is present in the file.")
else:
    print("The word is not present in the file.")
