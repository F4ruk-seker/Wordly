import pygame
import sys

# Pygame'i başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 800, 600
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
background_image = pygame.image.load("assets/bg.jpg")  # Kendi resminizin yolunu buraya yazın
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Buton oluşturma fonksiyonu
def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, label_rect)

# Ana döngü
running = True
hp = 100
score = 0
word = "PYTHON"
options = ["Java", "Python", "C++", "Ruby"]

# Buton konumlarını hesapla
button_width, button_height = 150, 50
button_spacing = 20
total_width = len(options) * button_width + (len(options) - 1) * button_spacing
start_x = (WIDTH - total_width) // 2
button_y = HEIGHT // 2 + 50
buttons = []

for i in range(len(options)):
    button_x = start_x + i * (button_width + button_spacing)
    buttons.append(pygame.Rect(button_x, button_y, button_width, button_height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Tıklamayı kontrol et
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, button_rect in enumerate(buttons):
                if button_rect.collidepoint(mouse_pos):
                    print(f"{options[i]} butonuna tıkladınız!")
                    # Aksiyon ekle
                    if options[i].lower() == word.lower():
                        score += 10
                        print("Doğru cevap!")
                    else:
                        hp -= 10
                        print("Yanlış cevap!")

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
    word_label = large_font.render(word, True, WHITE)
    word_rect = word_label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(word_label, word_rect)

    # Şıkları çiz
    for i, option in enumerate(options):
        button_rect = buttons[i]
        draw_button(option, button_rect.x, button_rect.y, button_width, button_height, GRAY, BLACK)

    # Ekranı güncelle
    pygame.display.flip()

    # Oyunu sonlandırma koşulu
    if hp <= 0:
        print("Oyun bitti!")
        running = False

# Pygame'den çık
pygame.quit()
sys.exit()
