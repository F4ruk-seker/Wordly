import time

import pygame
import sys
import json
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Oyun Arayüzü")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Yazı tipleri
font = pygame.font.Font(pygame.font.get_default_font(), 24)
large_font = pygame.font.Font(pygame.font.get_default_font(), 32)

# Arka plan resmi
background_image = pygame.image.load("assets/bg.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


# Buton oluşturma fonksiyonu
def draw_button(text, x, y, width, height, color, text_color):
    # width = width + len(text) * 1.5 if len(text) > 15 else width
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, label_rect)


# JSON'dan verileri yükleme
with open('words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

WORDS = data.get('words', [])
ANSWERS = [word.get('answer') for word in WORDS]


# Ağırlık hesaplama fonksiyonu
def calculate_percentage_weights(words):
    total_fail = sum(word.get('fail', 0) for word in words)
    if total_fail == 0:
        return [1 / len(words) for _ in words]
    return [word.get('fail', 0) / total_fail for word in words]


# Oyun için başlangıç değişkenleri
hp = 100
score = 0
selected_word = None
options = []
correct_index = -1
combo = 0
is_shaking = False  # Sallanma sırasında tıklamaları engellemek için bayrak

sounds = {
    1: pygame.mixer.Sound("assets/sounds/v1.mp3"),
    2: pygame.mixer.Sound("assets/sounds/v2.mp3"),
    3: pygame.mixer.Sound("assets/sounds/v3.mp3"),
    4: pygame.mixer.Sound("assets/sounds/v4.mp3"),
    5: pygame.mixer.Sound("assets/sounds/v5.mp3"),
    -1: pygame.mixer.Sound("assets/sounds/off.mp3"),
    -2: pygame.mixer.Sound("assets/sounds/wasted.mp3"),
}


def generate_question():
    """Yeni bir soru oluşturur ve gerekli verileri döndürür."""
    weights = calculate_percentage_weights(WORDS)
    selected = random.choices(WORDS, weights=weights, k=1)[0]
    wrongs = random.sample([answer for answer in ANSWERS if answer != selected['answer']], k=3)
    answer_index = random.randint(0, len(wrongs))
    wrongs.insert(answer_index, selected['answer'])
    return selected, wrongs, answer_index


# İlk soruyu oluştur
selected_word, options, correct_index = generate_question()

# Ana döngü
running = True
button_width, button_height = 250, 60
button_spacing = 20
total_width = len(options) * button_width + (len(options) - 1) * button_spacing
start_x = (WIDTH - total_width) // 2
button_y = HEIGHT // 2 + 50
buttons = []

for i in range(len(options)):
    button_x = start_x + i * (button_width + button_spacing)
    buttons.append(pygame.Rect(button_x, button_y, button_width, button_height))


def shake_screen(message: str = 'MAL'):
    """Ekranı kısa bir süre sallar."""
    global is_shaking
    is_shaking = True  # Sallanma işlemi sırasında tıklamaları engelle
    for _ in range(5):  # 5 tekrar yap
        for dx, dy in [(5, 0), (-5, 0), (0, 5), (0, -5)]:
            screen.blit(background_image, (dx, dy))
            word_label = large_font.render(message, True, WHITE)
            word_rect = word_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(word_label, word_rect)
            pygame.display.flip()
            pygame.time.delay(50)
    is_shaking = False  # Sallanma işlemi bittiğinde tıklamaları tekrar aktif et


while running:
    for event in pygame.event.get():
        if event.type == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.QUIT:
            running = False

        # Tıklamayı kontrol et (sallanma sırasında engelle)
        if event.type == pygame.MOUSEBUTTONDOWN and not is_shaking:
            mouse_pos = pygame.mouse.get_pos()
            for i, button_rect in enumerate(buttons):
                if button_rect.collidepoint(mouse_pos):
                    if i == correct_index:
                        print("Doğru!")
                        score += 10
                        combo += 1
                        match combo:
                            case 1:
                                sounds[1].play()  # v1.mp3 sesini çal
                            case 2:
                                sounds[2].play()  # v2.mp3 sesini çal
                            case 3:
                                sounds[3].play()  # v3.mp3 sesini çal
                            case 4:
                                sounds[4].play()  # v4.mp3 sesini çal
                            case 5:
                                sounds[5].play()  # v5.mp3 sesini çal
                                combo = 0  # Combo'yu sıfırla
                                if not hp >= 100:
                                    hp += 5
                                shake_screen(f'HELALLLLS!!!')  # Sallama efekti
                    else:
                        print("Yanlış!")
                        hp -= 10
                        sounds[-1].play()  # v5.mp3 sesini çal
                        shake_screen(f'{options[correct_index]}')  # Sallama efekti

                    # Yeni soru oluştur
                    selected_word, options, correct_index = generate_question()

    # Arka planı çiz
    screen.blit(background_image, (0, 0))

    # HP barını çiz
    pygame.draw.rect(screen, GRAY, (20, 20, 200, 25))
    pygame.draw.rect(screen, GREEN, (20, 20, hp * 2, 25))  # HP'yi yüzdeye göre ayarlayın
    hp_label = font.render(f"HP: {hp}", True, WHITE)
    screen.blit(hp_label, (20, 50))

    # Skor göstergesini çiz
    score_label = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_label, (WIDTH - 150, 20))

    # Ortadaki kelimeyi çiz
    word_label = large_font.render(selected_word['word'], True, WHITE)
    word_rect = word_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(word_label, word_rect)

    # Şıkları çiz
    buttons = []
    for i, option in enumerate(options):
        button_x = start_x + i * (button_width + button_spacing)
        buttons.append(pygame.Rect(button_x, button_y, button_width, button_height))
        draw_button(option, button_x, button_y, button_width, button_height, GRAY, BLACK)

    # Ekranı güncelle
    pygame.display.flip()

    # Oyunu sonlandırma koşulu
    if hp <= 0:
        print("Oyun bitti!")
        sounds[-2].set_volume(0.1)
        sounds[-2].play()
        time.sleep(4)
        running = False

# Pygame'den çık
pygame.quit()
sys.exit()
