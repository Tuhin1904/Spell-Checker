# import time
import datetime
from textblob import TextBlob
# import Levenshtein
import numpy as np
import re

MAX_SUGGESTIONS = 5
MAX_SUGGESTION_DISTANCE = 2
dictionary_location = "./bangla_words3.txt"

input_text = "  গোরু প্রায় ২০ | ২৫  বছর বাঁচে | গোরু অত্যন্ত উপকারী জীব | গোরুর দুধ থেকে দই, ছানা, মিষ্টি, মাখন, ঘি ইত্যাদি তৈরি হয় ৷ গোরুর মলকে গোবর বলে | গোবর থেকে ঘুঁটে, সার ইত্যাদি তৈরি হয় | গোরু এত উপকারী বলে হিন্দুরা একে দেবতাজ্ঞানে পূজাে করে ৷ বোমা হামলার পর ঘটনাস্থল থেকে পালিয়ে গিয়ে ঝিনাইদহ সদরে জঙ্গি ক্যাম্পে কিছুদিন ছিলেন তুহিন।এরপর মামলা ও গ্রেফতারি পরোয়ানা হলে কিছুদিনের মধ্যে তিনি পালিয়ে ঢাকায় চলে আসেন।"
# input_text="কাহদেবে তাহদ্ব"


# input_text= "ভালবাসির লকাতা আলকাটা ভালবাসিব গরুর গৃহপালিত প্রাণী  গরুর চারটি পা, দুটি "

# input_text=  "আলকাটা'"

# input_text="কষ্ট না করলে কেষ্ট মেলে না"

# input_text="এলোপাতাড়ি বোমা হামলার পর তারা বিভিন্ন দিকে দৌড়ে পালিয়ে যান। বোমা হামলার পর ঘটনাস্থল থেকে পালিয়ে গিয়ে ঝিনাইদহ সদরে জঙ্গি ক্যাম্পে কিছুদিন ছিলেন তুহিন। এরপর মামলা ও গ্রেফতারি পরোয়ানা হলে কিছুদিনের মধ্যে তিনি পালিয়ে ঢাকায় চলে আসেন। প্রথমে তিনি যাত্রাবাড়ী, পরবর্তীতে খিলগাঁও, উত্তরা, মহাখালীসহ বিভিন্ন জায়গায় স্থান পরিবর্তন করে বসবাস করে আসছিলেন। গ্রেফতার হওয়ার ভয়ে তিনি বিভিন্ন সময় বাসা পরিবর্তন করে ভিন্ন ভিন্ন জায়গায় বসবাস শুরু করেন। "
# input_text="এলোপাতাড়ি বোমা হামলার পর তারা বিভিন্ন দিকে দৌড়ে পালিয়ে যান।"

# input_text="এলোপাতাড়ি বোমা হামলার পর তারু বিভিন্ন দিকে দৌড়ে পালিয়ে যান।"





def get_dictionary_words():
    with open(dictionary_location, 'r', encoding='utf-8') as file:
        return file.read().splitlines()
    return []

def check_word_in_file(word, filename):
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if word in line:
                return True
    return False

def is_word_in_dictionary(word):
    return check_word_in_file(word, dictionary_location)

def remove_all_bengali_numeric_characters(text):
    return re.sub(r'[০১২৩৪৫৬৭৮৯]', '', text)

def sanitize_input(text):
    punctuations = ['-', ',', '।', '!', '?', ',', '(', ')', '{', '}', '[', ']', ':', ';', '‘', '’', '“', '”', '—', '–', '…', '।', '॥', 'ঃ', 'ঽ', '্', '|', '৷', '৸', '৹', '৺', '৻', 'ৼ', '৽', '৾', '৿', '၊', '။', '።', '፧', '፨', '᙮', '၎', '၍', '၌', '။', '၊', '၉', '၈', '၇', '၆', '၅', '၄', '၃', '၂', '၁', '၀', '፬', '፫', '፪', '፩', '፨', '፧', '፦', '፥', '፤', '፣', '።', '፡', '፠', '፟', '፞', '፝', '፜', '፛', 'ፚ', 'ፙ', 'ፘ', 'ፗ', 'ፖ', 'ፕ', 'ፔ', 'ፓ', 'ፒ', 'ፑ', 'ፐ', 'ፏ', 'ፎ', 'ፍ', 'ፌ', 'ፋ', 'ፊ', 'ፉ', 'ፈ', 'ፇ', 'ፆ', 'ፅ', 'ፄ', 'ፃ', 'ፂ', 'ፁ', 'ፀ', 'ዿ', 'ዾ', 'ዽ', 'ዼ', 'ዻ', 'ዺ', 'ዹ', 'ዸ', 'ዷ', 'ዶ', 'ድ', 'ዴ', 'ዳ', 'ዲ', 'ዱ', 'ደ', 'ዯ', 'ዮ', 'ይ', 'ዬ', 'ያ', 'ዪ', 'ዩ', 'የ', 'ዧ', 'ዦ']
    sanitized_text = remove_all_bengali_numeric_characters(text)

    for punctuation in punctuations:
        sanitized_text = sanitized_text.replace(punctuation, ' ')
    sanitized_text = re.sub(r'\s+', ' ', sanitized_text)

    return sanitized_text


def bengali_levenshtein_distance(word1, word2):
    m = len(word1)
    n = len(word2)
    dp = np.zeros((m + 1, n + 1), dtype=int)

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]


def split_words(text):
    return text.split()


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    text = sanitize_input(input_text)
    words = split_words(text)

    correct_words = []
    incorrect_words = []

    dictionary_words = get_dictionary_words()

    for word in words:
        if is_word_in_dictionary(word):
            if word not in correct_words:
                correct_words.append(word)
        else:
            if word not in incorrect_words:
                incorrect_words.append(word)

    print(f"Found {len(incorrect_words)} incorrect words")

    incorrect_word_suggestion_index = 1
    for word in incorrect_words:
        suggestions = []
        for correct_word in correct_words:
            if bengali_levenshtein_distance(word, correct_word) <= MAX_SUGGESTION_DISTANCE:
                suggestions.append(correct_word)
            if len(suggestions) == MAX_SUGGESTIONS:
                break

        if len(suggestions) < MAX_SUGGESTIONS:
            for dictionary_word in dictionary_words:
                if bengali_levenshtein_distance(word, dictionary_word) <= MAX_SUGGESTION_DISTANCE:
                    suggestions.append(dictionary_word)
                    if len(suggestions) == MAX_SUGGESTIONS:
                        break
        print(f"Incorrect word({incorrect_word_suggestion_index}/{len(incorrect_words)}): {word}, Suggestions: {suggestions}")
        incorrect_word_suggestion_index += 1
    print(f"Found {len(incorrect_words)} incorrect words")
    print("Time taken to provide suggestion: ", datetime.datetime.now() - start_time)
