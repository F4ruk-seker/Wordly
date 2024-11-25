import pygame
import sys
import json
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 1920 // 1.5, 1080 // 1.5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordly")

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
    width = width + len(text) * 0.5 if len(text) > 15 else width
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
button_width, button_height = 200, 50
button_spacing = 20
total_width = len(options) * button_width + (len(options) - 1) * button_spacing
start_x = (WIDTH - total_width) // 2
button_y = HEIGHT // 2 + 50
buttons = []

for i in range(len(options)):
    button_x = start_x + i * (button_width + button_spacing)
    buttons.append(pygame.Rect(button_x, button_y, button_width, button_height))

def shake_screen():
    """Ekranı kısa bir süre sallar."""
    for _ in range(5):  # 5 tekrar yap
        for dx, dy in [(5, 0), (-5, 0), (0, 5), (0, -5)]:
            screen.blit(background_image, (dx, dy))
            pygame.display.flip()
            pygame.time.delay(50)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Tıklamayı kontrol et
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, button_rect in enumerate(buttons):
                if button_rect.collidepoint(mouse_pos):
                    if i == correct_index:
                        print("Doğru!")
                        score += 10
                    else:
                        print("Yanlış!")
                        hp -= 10
                        shake_screen()  # Sallama efekti

                    # Yeni soru oluştur
                    selected_word, options, correct_index = generate_question()

    # Arka planı çiz
    screen.blit(background_image, (0, 0))

    # HP barını çiz
    pygame.draw.rect(screen, GRAY, (20, 20, 200, 25))
    pygame.draw.rect(screen, GREEN, (20, 20, hp * 2, 25))  # HP'yi yüzdeye göre ayarlayın
    hp_label = font.render(f"HP: {hp}", True, WHITE)
    screen.blit(hp_label, (20, 50))

    score_label = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_label, (WIDTH - 150, 20))

    word_label = large_font.render(selected_word['word'], True, WHITE)
    word_rect = word_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(word_label, word_rect)

    buttons = []
    for i, option in enumerate(options):
        button_x = start_x + i * (button_width + button_spacing)
        buttons.append(pygame.Rect(button_x, button_y, button_width, button_height))
        draw_button(option, button_x, button_y, button_width, button_height, GRAY, BLACK)

    pygame.display.flip()

    if hp <= 0:
        print("Oyun bitti!")
        running = False

pygame.quit()
sys.exit()
