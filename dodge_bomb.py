import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),#上
    pg.K_DOWN:(0,5),#下
    pg.K_LEFT:(-5,0),#左
    pg.K_RIGHT:(5,0),#右
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面内か画面外かを判定する関数
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向,縦方向判定結果（True: 画面内,False: 画面外）
    """

    yoko,tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    引数：画面Surface
    """
    black = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(screen,(0, 0, 0), (0, 0, WIDTH, HEIGHT))
    black.set_alpha(128)
    fonto = pg.font.Font(None,80)
    txt = fonto.render("Game Over", True, (255,255,255))
    fonto_rct = txt.get_rect()
    fonto_rct.center = (WIDTH // 2, HEIGHT // 2)
    game_img = pg.image.load("fig/8.png")
    game_img = pg.image.load("fig/8.png")
    game_rct_l = game_img.get_rect()
    game_rct_r = game_img.get_rect()
    game_rct_l.center = WIDTH // 2 - 200, HEIGHT // 2 
    game_rct_r.center = WIDTH // 2 + 200, HEIGHT // 2
    screen.blit(black, [0, 0])
    screen.blit(txt, fonto_rct)
    screen.blit(game_img, game_rct_l)
    screen.blit(game_img, game_rct_r)
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    base_img = pg.image.load("fig/3.png")
    # 左向きが基本なので、左右反転(flip)させたものを右向きの基本にする
    base_img_flip = pg.transform.flip(base_img, True, False)
    
    kk_dict = {
        ( 0,  0): pg.transform.rotozoom(base_img_flip, 0, 1.0),   # 止まっている（右向き）
        (+5,  0): pg.transform.rotozoom(base_img_flip, 0, 1.0),   # 右
        (+5, -5): pg.transform.rotozoom(base_img_flip, 45, 1.0),  # 右上
        ( 0, -5): pg.transform.rotozoom(base_img_flip, 90, 1.0),  # 上
        (-5, -5): pg.transform.rotozoom(base_img, -45, 1.0),      # 左上
        (-5,  0): pg.transform.rotozoom(base_img, 0, 1.0),        # 左
        (-5, +5): pg.transform.rotozoom(base_img, 45, 1.0),       # 左下
        ( 0, +5): pg.transform.rotozoom(base_img, -90, 1.0),      # 下
        (0, +5): pg.transform.rotozoom(base_img_flip, -45, 1.0), # 右下
    }
    return kk_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()
    kk_imgs = get_kk_imgs()

    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (225, 0, 0),(10,10),10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT) 
    vx,vy = 5,-5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            #print("ゲームオーバー")
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        avx = vx * bb_accs[min(tmr // 500, 9)]
        avy = vy * bb_accs[min(tmr // 500, 9)]
        bb_img = bb_imgs[min(tmr // 500, 9)]
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        if tuple(sum_mv) in kk_imgs:
            kk_img = kk_imgs[tuple(sum_mv)]
        kk_rct.move_ip(sum_mv)
        yoko, tate = check_bound(kk_rct)
        if not yoko:
            kk_rct.move_ip(-sum_mv[0], 0)
        if not tate:
            kk_rct.move_ip(0, -sum_mv[1])

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
