import pyxel

class Scrolling_Game:
    def __init__(self):
        pyxel.init(128, 128, title='Scrolling Game')
        pyxel.load('assets/scroll_game.pyxres')
        self.char_x = 50  # キャラクターのX座標
        self.char_y = 50  # キャラクターのY座標
        self.char_frame = 0  # 表示する画像のインデックス (0 または 1)
        self.frame_count = 0 # フレームカウンター
        self.scroll_x = 0
        self.scroll_speed = 1
        self.is_moving = False  # 移動中フラグを追加
        self.last_input = False #直前のフレームでキー入力があったか
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        # ゲーム中断
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.scroll_x += self.scroll_speed

        # キー入力と移動処理
        self.is_moving = False
        key_pressed = False # 今のフレームでキーが押されているか

        # キー入力処理とキャラクターの移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.char_x -= 1
            self.is_moving = True  # 移動中フラグを立てる
            key_pressed = True
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.char_x += 1
            self.is_moving = True
            key_pressed = True
        if pyxel.btn(pyxel.KEY_UP):
            self.char_y -= 1
            self.is_moving = True
            key_pressed = True
        if pyxel.btn(pyxel.KEY_DOWN):
            self.char_y += 1
            self.is_moving = True
            key_pressed = True

        if self.is_moving and self.last_input:
            self.frame_count += 1
            if self.frame_count % 10 == 0:
                self.char_frame = 1 - self.char_frame
        elif self.is_moving and not self.last_input:
                self.frame_count = 0
        
        self.last_input = key_pressed # 次のフレームのためにキー入力があったかを保存

    def draw(self):
        pyxel.cls(0)

        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
            
        # キャラクターの描画 (アニメーション)
        if self.char_frame == 0:
            pyxel.blt(self.char_x, self.char_y, 0, 0, 0, 16, 16, 7)
        else:
            pyxel.blt(self.char_x, self.char_y, 0, 16, 0, 16, 16, 7)

Scrolling_Game()