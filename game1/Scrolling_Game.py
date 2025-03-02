import pyxel
import random

class Scrolling_Game:
    def __init__(self):
        pyxel.init(128, 128, title='Scrolling Game')
        pyxel.load('assets/scroll_game.pyxres')
        self.char_x = 50  # キャラクターのX座標
        self.char_y = 50  # キャラクターのY座標
        self.char_frame = 0  # 表示する画像のインデックス (0 または 1)
        self.frame_count = 0 # フレームカウンター
        self.scroll_x = 0 # スクロール位置
        self.scroll_speed = 1 # スクロール速度
        self.is_moving = False  # 移動中フラグを追加
        self.last_input = False #直前のフレームでキー入力があったか
        self.item_x = random.randint(0, 120)
        self.item_y = random.randint(0, 120)
        self.spiderweb_x = 128
        self.spiderweb_y = random.randint(0, 120)
        self.spiderweb_speed = 3
        self.sickle_x = 128
        self.sickle_y = random.randint(0, 120)
        self.sickle_speed = 3
        self.score = 0
        self.is_out_of_screen = False  # 画面外フラグ
        self.collision_flag = False
        self.attack_item_x = -10
        self.attack_item_y = -10
        self.attack_item_active = False

        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.char_x = 50
        self.char_y = 50
        self.char_frame = 0
        self.frame_count = 0
        self.scroll_x = 0
        self.scroll_speed = 1
        self.is_moving = False
        self.last_input = False
        self.item_x = random.randint(0, 120)
        self.item_y = random.randint(0, 120)
        self.spiderweb_x = 128
        self.spiderweb_y = random.randint(0, 120)
        self.spiderweb_speed = 3
        self.sickle_x = 128
        self.sickle_y = random.randint(0, 120)
        self.sickle_speed = 3
        self.score = 0
        self.is_out_of_screen = False
        self.collision_flag = False
        self.attack_item_x = -10
        self.attack_item_y = -10
        self.attack_item_active = False

    def update_scroll(self):
        self.scroll_x += self.scroll_speed
        self.char_x -= self.scroll_speed
        if self.scroll_x > 128:
            self.scroll_x = 0

    def update_obstacles(self):
        self.spiderweb_x -= self.spiderweb_speed
        self.sickle_x -= self.sickle_speed
        if self.spiderweb_x < 0:
            self.spiderweb_x = 128
            self.spiderweb_y = random.randint(0, 120)
        elif self.sickle_x < 0:
            self.sickle_x = 128
            self.sickle_y = random.randint(0, 120)

    def check_collision(self):
        if (self.char_x < self.spiderweb_x + 12 and
            self.char_x + 12 > self.spiderweb_x and
            self.char_y < self.spiderweb_y + 12 and
            self.char_y + 12 > self.spiderweb_y):
            self.collision_flag = True

        if (self.char_x < self.sickle_x + 12 and
            self.char_x + 12 > self.sickle_x and
            self.char_y < self.sickle_y + 12 and
            self.char_y + 12 > self.sickle_y):
            self.collision_flag = True

    def handle_input(self):
        self.is_moving = False
        key_pressed = False
        if pyxel.btn(pyxel.KEY_LEFT):
            self.char_x -= 1
            self.is_moving = True
            key_pressed = True
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.char_x += 3
            self.is_moving = True
            key_pressed = True
        if pyxel.btn(pyxel.KEY_UP):
            self.char_y -= 2
            self.is_moving = True
            key_pressed = True
        if pyxel.btn(pyxel.KEY_DOWN):
            self.char_y += 2
            self.is_moving = True
            key_pressed = True

        if self.is_moving and self.last_input:
            self.frame_count += 1
            if self.frame_count % 10 == 0:
                self.char_frame = 1 - self.char_frame
        elif self.is_moving and not self.last_input:
            self.frame_count = 0

        self.last_input = key_pressed

    def update_attack_item(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.attack_item_x = self.char_x
            self.attack_item_y = self.char_y
            self.attack_item_active = True

        if self.attack_item_active:
            self.attack_item_x += 4  # 速度を2倍に
            if self.attack_item_x > 128:
                self.attack_item_active = False
                self.attack_item_x = -10
                self.attack_item_y = -10

            # 攻撃アイテムが障害物と重なった場合
            if (self.attack_item_x < self.spiderweb_x + 16 and
                self.attack_item_x + 8 > self.spiderweb_x and
                self.attack_item_y < self.spiderweb_y + 16 and
                self.attack_item_y + 8 > self.spiderweb_y):
                self.attack_item_active = False
                self.spiderweb_x = 128
                self.spiderweb_y = random.randint(0, 120)

            if (self.attack_item_x < self.sickle_x + 16 and
                self.attack_item_x + 8 > self.sickle_x and
                self.attack_item_y < self.sickle_y + 16 and
                self.attack_item_y + 8 > self.sickle_y):
                self.attack_item_active = False
                self.sickle_x = 128
                self.sickle_y = random.randint(0, 120)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()

        self.update_scroll()
        self.update_obstacles()
        self.check_collision()
        self.handle_input()
        self.update_attack_item()

        if (self.char_x < self.item_x + 8 and 
            self.char_x + 16 > self.item_x and
            self.char_y < self.item_y + 8 and
            self.char_y + 16 > self.item_y):
            self.score += 100
            self.item_x = random.randint(0, 120)
            self.item_y = random.randint(0, 120)

    def draw(self):
        pyxel.cls(0)

        pyxel.bltm(0, 0, 0, self.scroll_x, 0, 128, 128)
        pyxel.blt(self.item_x, self.item_y, 0, 8, 24, 8, 8, 0)

        if self.attack_item_active:
            pyxel.blt(self.attack_item_x, self.attack_item_y, 0, 16, 16, 8, 8, 7)

        pyxel.blt(self.spiderweb_x, self.spiderweb_y, 0, 32, 0, 16, 16, 0)
        pyxel.blt(self.sickle_x, self.sickle_y, 0, 48, 0, 16, 16, 0)
        

        # キャラクターの描画 (アニメーション)
        if self.char_frame == 0:
            pyxel.blt(self.char_x, self.char_y, 0, 0, 0, 16, 16, 7)
        else:
            pyxel.blt(self.char_x, self.char_y, 0, 16, 0, 16, 16, 7)

        pyxel.text(5, 5, f"Score: {self.score}", 1)
        # キャラクターが画面外に出た場合
        if (self.char_x < -16 or self.char_x > 128 or self.char_y < -16 or self.char_y > 128) or (self.collision_flag):
            self.collision_flag = True
            pyxel.bltm(0, 0, 0, 0, 128, 128, 128, 128)  # 指定のタイルを表示

Scrolling_Game()