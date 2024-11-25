
pyload : list[dict] = [
    {"word": "big", "answer": "büyük"},
    {"word": "small", "answer": "küçük"},
    {"word": "little", "answer": "küçük"},
    {"word": "fast", "answer": "hızlı"},
    {"word": "slow", "answer": "yavaş"},
    {"word": "good", "answer": "iyi"},
    {"word": "bad", "answer": "kötü"},
    {"word": "expensive", "answer": "pahalı"},
    {"word": "cheap", "answer": "ucuz"},
    {"word": "thick", "answer": "kalın"},
    {"word": "thin", "answer": "ince"},
    {"word": "narrow", "answer": "dar"},
    {"word": "wide", "answer": "geniş"},
    {"word": "broad", "answer": "geniş"},
    {"word": "loud", "answer": "gürültülü"},
    {"word": "quiet", "answer": "sessiz"},
    {"word": "intelligent", "answer": "zeki"},
    {"word": "stupid", "answer": "aptal"},
    {"word": "wet", "answer": "ıslak"},
    {"word": "dry", "answer": "kuru"},
    {"word": "heavy", "answer": "ağır"},
    {"word": "light", "answer": "hafif"},
    {"word": "hard", "answer": "sert"},
    {"word": "soft", "answer": "yumuşak"},
    {"word": "shallow", "answer": "sığ"},
    {"word": "deep", "answer": "derin"},
    {"word": "easy", "answer": "kolay"},
    {"word": "difficult", "answer": "zor"},
    {"word": "weak", "answer": "zayıf"},
    {"word": "strong", "answer": "güçlü"},
    {"word": "rich", "answer": "zengin"},
    {"word": "poor", "answer": "fakir"},
    {"word": "young", "answer": "genç"},
    {"word": "old", "answer": "yaşlı"},
    {"word": "long", "answer": "uzun"},
    {"word": "short", "answer": "kısa"},
    {"word": "high", "answer": "yüksek"},
    {"word": "low", "answer": "alçak"},
    {"word": "generous", "answer": "cömert"},
    {"word": "mean", "answer": "acımasız"},
    {"word": "true", "answer": "gerçek/doğru"},
    {"word": "false", "answer": "sahte/yanlış"},
    {"word": "beautiful", "answer": "güzel"},
    {"word": "ugly", "answer": "çirkin"},
    {"word": "new", "answer": "yeni"},
    {"word": "old", "answer": "eski"},
    {"word": "happy", "answer": "mutlu"},
    {"word": "sad", "answer": "mutsuz"}
]


for _ in pyload:
    _["fail"] = 0

print(pyload)

import json

with open('words.json', 'r', encoding='utf-8') as df:
    raw = json.loads(df.read())

words: list = raw.get('words')
words.append(pyload)
raw['words'] = words



with open('words.json', 'w', encoding='utf-8') as df:
    df.write(json.dumps(raw))


# print(json.dumps(pyload))