import json
import random
import sys

# Dosyayı okuma
with open(file='words.json', mode='r', encoding='utf-8') as df:
    data = json.loads(df.read())

# 'words' listesi ve 'answers' listesi
WORDS: list[dict] = data.get('words', [])

ANSWERS: list[str] = [word.get('answer') for word in WORDS]

# Yüzdelik ağırlık hesaplama


def calculate_percentage_weights(words: list[dict]):
    total_fail = sum(word.get('fail', 0) for word in words)  # Toplam `fail` puanı
    if total_fail == 0:  # Eğer toplam `fail` sıfırsa, eşit dağılım yap
        return [1 / len(words) for _ in words]
    return [word.get('fail', 0) / total_fail for word in words]


while True:
    sys.stdout.flush()
    # Ağırlıkların hesaplanması
    weights = calculate_percentage_weights(WORDS)

    # Rastgele bir kelime seçimi
    selected_word = random.choices(WORDS, weights=weights, k=1)[0]

    # Yanlış cevapların rastgele seçilmesi
    wrongs: list = random.sample([answer for answer in ANSWERS if answer != selected_word['answer']], k=3)

    answer_index = random.randint(0, len(wrongs))

    wrongs.insert(answer_index, selected_word.get('answer'))

    # Sonuçların yazdırılması

    print("\rSeçilen kelime:", selected_word.get('word'), end=" ")

    for index, value in zip(range(len(wrongs)), wrongs):
        print(f'{index}: {value}')

    user_answer: str = input(': ')
    if user_answer.lower() == "q":
        break

    if int(user_answer) == answer_index:
        print('Doğru ')
    else:
        print('yanlış')


