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

        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        # ゲーム中断
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # Rキーが押されたらリセット
        if pyxel.btnp(pyxel.KEY_R):
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

        self.scroll_x += self.scroll_speed  # スクロール位置を更新
        self.char_x -= self.scroll_speed  # キャラ位置を更新
        # スクロール位置が背景画像の幅を超えたら、0に戻す
        if self.scroll_x > 128:  # 128は背景画像の幅
            self.scroll_x = 0 

        self.spiderweb_x -= self.spiderweb_speed
        self.sickle_x -= self.sickle_speed
        if self.spiderweb_x < 0:
            self.spiderweb_x = 128
            self.spiderweb_y = random.randint(0, 120)
        elif self.sickle_x < 0:
            self.sickle_x = 128
            self.sickle_y = random.randint(0, 120)
        # 当たり判定
        if (self.char_x < self.spiderweb_x + 12 and
            self.char_x + 12 > self.spiderweb_x and
            self.char_y < self.spiderweb_y + 12 and
            self.char_y + 12 > self.spiderweb_y):

            # 当たり時の処理 (例: ゲームオーバー)
            self.collision_flag = True

        # 当たり判定
        if (self.char_x < self.sickle_x + 12 and
            self.char_x + 12 > self.sickle_x and
            self.char_y < self.sickle_y + 12 and
            self.char_y + 12 > self.sickle_y):

            # 当たり時の処理 (例: ゲームオーバー)
            self.collision_flag = True

        # キー入力と移動処理
        self.is_moving = False
        key_pressed = False # 今のフレームでキーが押されているか

        # キー入力処理とキャラクターの移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.char_x -= 1
            self.is_moving = True  # 移動中フラグを立てる
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
        
        self.last_input = key_pressed # 次のフレームのためにキー入力があったかを保存

        # 当たり判定
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
            pyxel.bltm(0, 0, 0, 0, 128, 128, 128)  # 指定のタイルを表示

Scrolling_Game()