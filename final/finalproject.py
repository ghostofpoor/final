# 要先安裝pygame 在終端機輸入 mac :python3 -m pip install -U pygame --user
# windows : py -m pip install -U pygame --user
# 導入函數庫
import pygame
import os
import random
import sys
import time
# 初始化pygame
def initialize_game():
    pygame.init()

# 顏色
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
SKYBLUE = pygame.Color(0, 127, 255)
# import 圖片檔案
BACKGROUND_LIST = [pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/background", "1.jpg")), pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/background", "2.jpg"))]
CHARACTOR_LIST = [pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/charactor", "Run1.png")),
                pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/charactor", "Run2.png"))]  # 跑步圖片大小 87*94
JUMPING_IMG = pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/charactor", "Jump.png"))  # 跳躍圖片大小 87*94
DUCKING_LIST = [pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/charactor", "Duck1.png")),
                pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/charactor", "Duck2.png"))]  #  蹲下大小 118*60
ITEM = [pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/item", "1.png")),
        pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/item", "2.png")),
        pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/item", "3.png"))]
#  大障礙物
LARGEOBSTACLE = [pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/largeobstacle", "obstacle1.png")),
             pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/largeobstacle", "obstacle2.png")),
             pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/largeobstacle", "obstacle3.png"))]
# 小障礙物
SMALLOBSTACLE = [pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/smallobstacle", "obstacle1.png")),
             pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/smallobstacle", "obstacle2.png"))]
FLYOBSTACLE = [pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/flyobstacle", "obstacle1.png")),
             pygame.image.load(os.path.join("Documents\\GitHub\\final\\image/flyobstacle", "obstacle2.png"))]
           #  小1：68*71 小2: 40*71 大1：105*95 大2：99*95 大3 48*95
# 建立視窗(背景長/寬 ＝ 1023/660)
window_height = 650
window_width = 1000
window = pygame.display.set_mode((window_width, window_height))
screen = pygame.display.set_mode((window_width, window_height))
#  難度
EASY = 1
MEDIUM = 2
HARD = 3
game_difficulty = EASY

# 文字處理
class Text:
    def __init__(self, text, size, color, position=(0, 0)):
        self.font = pygame.font.SysFont('freesansbold.ttf', size)  # 字體大小(參數)與字型
        self.surface = self.font.render(text, True, color)  # 印出的字串(參數)與呈現
        self.rect = self.surface.get_rect()  # 文字框起
        self.rect.center = position  # 文字的中心位置(參數)
    def draw(self, screen):
        screen.blit(self.surface, self.rect)
#  角色處理
class Charactor:
    x_ch_pos = 80
    y_ch_pos = 480
    y_ch_posduck = 510
    jump_val = 7
    def __init__(self):
         # 定義變數
        self.ch_duck = False
        self.ch_run = True
        self.ch_jump = False
        self.step_index = 0  # 腳步動畫
        self.jump_vel = self.jump_val  # 跳上、下的速度

        # 圖片
        self.duck_img_list = DUCKING_LIST
        self.run_img_list = CHARACTOR_LIST
        self.jump_img = JUMPING_IMG
        self.image = self.run_img_list[0]  

        # 把角色框列
        self.ch_rect = self.image.get_rect()
        self.ch_rect.x = self.x_ch_pos
        self.ch_rect.y = self.y_ch_pos
        self.invincible_timer = 0

    def run(self):
        self.image = self.run_img_list[self.step_index // 5]  # 依 step_index 跑步圖片，每五個step_index換一張圖
        self.ch_rect = self.image.get_rect()
        self.ch_rect.x = self.x_ch_pos
        self.ch_rect.y = self.y_ch_pos
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img_list[self.step_index // 5]  # 依 step_index 蹲下圖片，每五個step_index換一張圖
        self.ch_rect = self.image.get_rect()
        self.ch_rect.x = self.x_ch_pos
        self.ch_rect.y = self.y_ch_posduck
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.ch_jump:
            self.ch_rect.y -= self.jump_vel * 4  
            self.jump_vel -= 0.5  
        if self.jump_vel < - self.jump_val:
            self.ch_jump = False
            self.jump_vel = self.jump_val
    def update(self, user_input):
        if user_input[pygame.K_UP] or user_input[pygame.K_SPACE] and not self.ch_jump:
            self.ch_duck = False
            self.ch_run = False
            self.ch_jump = True
        elif user_input[pygame.K_DOWN] and not self.ch_jump:
            self.ch_duck = True
            self.ch_run = False
            self.ch_jump = False
        elif not (self.ch_jump or user_input[pygame.K_DOWN]):
            self.ch_duck = False
            self.ch_run = True
            self.ch_jump = False

    # 目前該做甚麼動作
        if self.ch_duck:
            self.duck()
        if self.ch_run:
            self.run()
        if self.ch_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
    def take_damage(self):  # 無敵狀態
        if self.invincible_timer <= 0:  # 如果不在無敵時間內
            self.invincible_timer = 30 
    def is_invincible(self):
        return self.invincible_timer > 0
    def draw(self, screen):
        screen.blit(self.image, (self.ch_rect.x, self.ch_rect.y))
#  障礙物處理
class Obstacle:
    def __init__(self, imageList : list, typeObject : int):
        self.image_list = imageList  # 以變數儲存障礙物類型
        self.type = typeObject  # 以變數儲存障礙物樣貌
        self.rect = self.image_list[self.type].get_rect()  # 將障礙物框起
        self.rect.x = window_width  # 障礙物X座標位置

    def update(self):
        self.rect.x -= game_speed

    def draw(self, screen : pygame.surface):
        screen.blit(self.image_list[self.type], (self.rect.x, self.rect.y))
class largeobs(Obstacle):
    def __init__(self, image_list : list):
        self.type = bg  # 不同背景不同種類的障礙物
        super().__init__(image_list, self.type)  # 繼承障礙物屬性與動作
        self.rect.y = 500  # Y座標位置
class smallobs(Obstacle):
    def __init__(self, image_list : list):
        self.type = bg  # 三種小仙人掌型態隨機選取一種
        super().__init__(image_list, self.type)  # 繼承障礙物屬性與動作
        self.rect.y = 500 # Y座標位置
class flyobs(Obstacle):
    def __init__(self, image_list : list):
        self.type = bg  # 三種小仙人掌型態隨機選取一種
        super().__init__(image_list, self.type)  # 繼承障礙物屬性與動作
        self.rect.y = 400 # Y座標位置
#  道具處理
class Heart:
    def __init__(self, image_list: list):
        self.image_list = image_list  # 道具圖片列表
        self.type = 0  # 道具類型，這裡預設為 0
        self.rect = self.image_list[self.type].get_rect()  # 道具的矩形區域
        self.rect.x = window_width  # 道具出現的 x 座標
        self.rect.y = random.randint(300, 500)  # 道具出現的 y 座標
    def update(self):
        self.rect.x -= game_speed  # 道具向左移動的速度
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image_list[self.type], (self.rect.x, self.rect.y))  # 繪製道具
class star:
    def __init__(self, image_list: list):
        self.image_list = image_list  # 道具圖片列表
        self.type = 2  # 道具類型，這裡預設為 0
        self.rect = self.image_list[self.type].get_rect()  # 道具的矩形區域
        self.rect.x = window_width  # 道具出現的 x 座標
        self.rect.y = random.randint(300, 500)  # 道具出現的 y 座標
    def update(self):
        self.rect.x -= game_speed  # 道具向左移動的速度
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image_list[self.type], (self.rect.x, self.rect.y))  # 繪製道具

#  標題目錄
def menu():
    global game_difficulty

    text_position = (600, window_height // 2) # 螢幕中心
    run = True
    while run :
        window.fill(WHITE)
        window.blit(BACKGROUND_LIST[0], (0, 0))
        start_text = Text("Choose the Game Difficulty", 40, BLACK, text_position)
        start_text.draw(window)

        # 繪製難度選擇按鈕及框框
        easy_button_rect = pygame.Rect(100, 200, 200, 50)
        medium_button_rect = pygame.Rect(100, 300, 200, 50)
        hard_button_rect = pygame.Rect(100, 400, 200, 50)

        pygame.draw.rect(window, BLACK, easy_button_rect, 2)
        pygame.draw.rect(window, BLACK, medium_button_rect, 2)
        pygame.draw.rect(window, BLACK, hard_button_rect, 2)

        # 繪製難度選擇按鈕的文本
        easy_text = Text("EASY", 30, BLACK, (200, 225))
        medium_text = Text("MEDIUM", 30, BLACK, (200, 325))
        hard_text = Text("HARD", 30, BLACK, (200, 425))

        easy_text.draw(window)
        medium_text.draw(window)
        hard_text.draw(window)

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == (pygame.QUIT or pygame.K_ESCAPE):
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左鍵點擊
                    mouse_pos = pygame.mouse.get_pos()
                    if easy_button_rect.collidepoint(mouse_pos):
                        game_difficulty = EASY
                        main()
                    elif medium_button_rect.collidepoint(mouse_pos):
                        game_difficulty = MEDIUM
                        main()
                    elif hard_button_rect.collidepoint(mouse_pos):
                        game_difficulty = HARD
                        main()
 
    pygame.quit()
    sys.exit()


# 主程式
def main():
    global game_speed
    global jump_val
    global points
    global bg
    global invincible_timer
    clock = pygame.time.Clock()
    points = 0
    oripoint = 0
    bg = 0
    player = Charactor()
    obstacles = []
    run = True
    x_bg_pos, y_bg_pos = 0, 0
    x_heart, y_heart = 80, 50
    items = []
    countdown = 3

    while countdown > 0:
        window.blit(BACKGROUND_LIST[bg], (x_bg_pos, y_bg_pos))
        player.draw(window)
        count_text = Text(f"{countdown}", 300, BLACK, (485, 300))
        count_text.draw(window)
        pygame.display.update()
        time.sleep(1)
        countdown -= 1

#  難度調整
    if game_difficulty == EASY:
        game_speed = 7
        life =5
    elif game_difficulty == MEDIUM:
        game_speed = 14
        life = 3
    elif game_difficulty == HARD:
        game_speed = 20
        life = 1

 #  開始迴圈
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
#  背景移動
        x_bg_pos -= game_speed 
        if oripoint % 3200 == 0 and points != 0: 
            bg = (bg + 1) % len(BACKGROUND_LIST)
        window.blit(BACKGROUND_LIST[bg], (x_bg_pos, y_bg_pos))
        window.blit(BACKGROUND_LIST[bg], (x_bg_pos + window_width, y_bg_pos))
        if x_bg_pos <= -window_width:
            window.blit(BACKGROUND_LIST[bg], (x_bg_pos + window_width, y_bg_pos))
            x_bg_pos = 0
        
#  生命值  心的大小是30*30
        window.blit(ITEM[0], (x_heart, y_heart))
        heart = Text(str(life), 30, BLACK, (95, 65))
        heart.draw(window)
        if life <= 0:
            run = False
#  分數計算
        oripoint +=1
        if oripoint % 4 == 0:
            points += 1
        score_position = (80, 20)
        score = Text("Points: " + str(points), 30, BLACK, score_position)
        score.draw(window)
        if points % 300 == 0 and game_speed <= 40:
            game_speed += 1
#  角色操作
        user_input = pygame.key.get_pressed()  # 接收玩家指令
        player.update(user_input)  # 依據玩家指令更新恐龍的動作
        player.draw(window)  
#  障礙物
        if len(obstacles) == 0:  # 生成障礙物
            rand = random.randint(0, 2)
            if rand == 0:
                obstacles.append(smallobs(SMALLOBSTACLE))
            elif rand == 1:
                obstacles.append(largeobs(LARGEOBSTACLE))
            elif rand == 2:
                obstacles.append(flyobs(FLYOBSTACLE))

        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(window)
            if player.ch_rect.colliderect(obstacle.rect) and player.is_invincible() == False :
                life -= 1
                player.take_damage()

            if obstacle.rect.x < -obstacle.rect.width:
                obstacles.remove(obstacle)
#  回血道具
    # 在遊戲迴圈中生成道具
        if len(items) == 0 and random.randint(0, 100) < 2:  # 機率2%
            items.append(Heart(ITEM))  # 加入新的道具到道具列表中

    # 在遊戲迴圈中更新和繪製道具
        for item in items:
            item.update()
            if item.rect.colliderect(obstacle.rect) == False:
                item.draw(window)
            else:
                items.remove(item)

    # 檢測角色和道具的碰撞
            if player.ch_rect.colliderect(item.rect):
                life += 1  # 增加生命值
                items.remove(item)  # 移除已經碰撞的道具
            if item.rect.x < -item.rect.width:
                items.remove(item)
#  無敵星星
        if len(items) == 0 and random.randint(0, 100) < 1:  # 機率1%
            items.append(star(ITEM))  # 加入新的道具到道具列表中

    # 在遊戲迴圈中更新和繪製道具
        for item in items:
            item.update()
            if item.rect.colliderect(obstacle.rect) == False:
                item.draw(window)
            else:
                items.remove(item)

    # 檢測角色和道具的碰撞
            if player.ch_rect.colliderect(item.rect):
                invincible_timer = 300   #無敵
                items.remove(item)  # 移除已經碰撞的道具
            if item.rect.x < -item.rect.width:
                items.remove(item)

        pygame.display.update()
        clock.tick(60)

    gameover()


def gameover():
    window.fill(WHITE)  # 用白色填充整個視窗
    game_over_text = Text("Game Over", 80, BLACK, (window_width // 2, window_height // 2 - 100))  # 顯示 "Game Over" 文字
    score_text = Text("Your Score: " + str(points), 40, BLACK, (window_width // 2, window_height // 2))  # 顯示分數
    continue_text = Text("Press Enter to Continue", 30, BLACK, (window_width // 2, window_height // 2 + 100))  # 提示玩家按 Enter 鍵繼續
    game_over_text.draw(window)
    score_text.draw(window)
    continue_text.draw(window)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # 如果玩家按下 Enter 鍵
                    menu()


# 執行程式碼
if __name__ == "__main__":
    initialize_game()
    menu()