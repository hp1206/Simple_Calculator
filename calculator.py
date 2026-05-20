import os, sys, array, math
import pygame

script_dir = os.path.dirname(os.path.abspath(__file__))
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

screen_width, screen_height = 274, 396

def make_click(freq=700, dur=0.05, vol=0.35):
    rate = 44100
    n = int(rate * dur)
    buf = array.array('h', [
        int(32767 * vol * math.sin(2 * math.pi * freq * i / rate) * (1 - i / n))
        for i in range(n)
    ])
    return pygame.mixer.Sound(buffer=buf)

click_sound = make_click()

def calculate(expr):
    try:
        if not all(c in '0123456789+-*/.' for c in expr):
            return 'Error'
        r = eval(expr)
        if isinstance(r, float):
            return str(int(r)) if r.is_integer() else f'{r:.8g}'
        return str(r)
    except ZeroDivisionError:
        return 'Error'
    except Exception:
        return 'Error'

OPS = set('+-*/')

def can_append(mem, ch):
    if not mem:
        return ch not in OPS
    last = mem[-1]
    if ch in OPS and last in OPS:
        return False
    if ch == '.':
        seg = ''
        for c in reversed(mem):
            if c in OPS: break
            seg = c + seg
        return '.' not in seg
    return True

def get_trailing_number(mem):
    i = len(mem) - 1
    while i >= 0 and (mem[i].isdigit() or mem[i] == '.'):
        i -= 1
    if i >= 0 and mem[i] == '-' and (i == 0 or mem[i - 1] in OPS):
        i -= 1
    return mem[:i + 1], mem[i + 1:]

def rebuild_display():
    global Num_list, x_pos
    Num_list, x_pos = [], 36
    for ch in memory:
        d = 'x' if ch == '*' else ch
        surf = Num_font.render(d, True, (41, 28, 41))
        Num_list.append((surf, (x_pos, 107)))
        x_pos += 4 if ch == '1' else (8 if ch == '.' else 11)

def do_action(action, rect=None):
    global memory, Num_list, x_pos, result, times_bang
    global highlight_rect, highlight_timer

    if times_bang == 1 and action not in ('DEL', 'AC', 'EQ'):
        Num_list, memory, x_pos, times_bang = [], '', 36, 0

    click_sound.play()
    if rect:
        highlight_rect, highlight_timer = rect, 8

    if action in '0123456789':
        if can_append(memory, action):
            w = 4 if action == '1' else 11
            Num_list.append((Num_font.render(action, True, (41, 28, 41)), (x_pos, 107)))
            x_pos += w
            memory += action

    elif action in OPS:
        disp = 'x' if action == '*' else action
        if can_append(memory, action):
            Num_list.append((Num_font.render(disp, True, (41, 28, 41)), (x_pos, 107)))
            x_pos += 11
            memory += action

    elif action == '.':
        if can_append(memory, '.'):
            Num_list.append((Num_font.render('.', True, (41, 28, 41)), (x_pos, 107)))
            x_pos += 8
            memory += '.'

    elif action == '%':
        if memory and memory[-1] not in OPS:
            prefix, num_str = get_trailing_number(memory)
            try:
                val = float(num_str) / 100
                val_str = str(int(val)) if val == int(val) else f'{val:.8g}'
                memory = prefix + val_str
                rebuild_display()
            except Exception:
                pass

    elif action == 'PM':
        if memory and (memory[-1].isdigit() or memory[-1] == '.'):
            prefix, num_str = get_trailing_number(memory)
            if num_str.startswith('-'):
                num_str = num_str[1:]
            else:
                num_str = '-' + num_str
            memory = prefix + num_str
            rebuild_display()

    # ── DEL ──────────────────────────────────────────────────────
    elif action == 'DEL':
        if times_bang == 1:
            Num_list, memory, x_pos, times_bang = [], '', 36, 0
        elif memory:
            ch = memory[-1]
            x_pos -= 4 if ch == '1' else (8 if ch == '.' else 11)
            x_pos = max(x_pos, 36)
            Num_list.pop()
            memory = memory[:-1]

    elif action == 'AC':
        Num_list, memory, x_pos, times_bang = [], '', 36, 0

    elif action == 'EQ' and times_bang == 0 and memory:
        times_bang = 1
        result = calculate(memory)

        if len(result) <= 8:
            res_font = Num_font
        elif len(result) <= 12:
            res_font = Num_font_sm
        else:
            res_font = Num_font_xs

        rw = result.count('1') * 4 + (len(result) - result.count('1')) * 11
        rx = max(36, 236 - rw + 2)
        Num_list.append((res_font.render(result, True, (41, 28, 41)), (rx, 152)))
        memory += '='
        x_pos += 11


def Button_event():
    pos = pygame.mouse.get_pos()
    mapping = [
        (Button_0_rect,'0'), (Button_1_rect,'1'), (Button_2_rect,'2'),
        (Button_3_rect,'3'), (Button_4_rect,'4'), (Button_5_rect,'5'),
        (Button_6_rect,'6'), (Button_7_rect,'7'), (Button_8_rect,'8'),
        (Button_9_rect,'9'),
        (Button_cong_rect,'+'), (Button_tru_rect,'-'),
        (Button_nhan_rect,'*'), (Button_chia_rect,'/'),
        (Button_dot_rect,'.'), (Button_pct_rect,'%'), (Button_pm_rect,'PM'),
        (Button_DEL_rect,'DEL'), (Button_AC_rect,'AC'), (Button_bang_rect,'EQ'),
    ]
    for rect, action in mapping:
        if rect.collidepoint(pos):
            do_action(action, rect)
            break

def Key_event(key):
    key_map = {
        pygame.K_0: '0', pygame.K_1: '1', pygame.K_2: '2',
        pygame.K_3: '3', pygame.K_4: '4', pygame.K_5: '5',
        pygame.K_6: '6', pygame.K_7: '7', pygame.K_8: '8', pygame.K_9: '9',
        pygame.K_KP0: '0', pygame.K_KP1: '1', pygame.K_KP2: '2',
        pygame.K_KP3: '3', pygame.K_KP4: '4', pygame.K_KP5: '5',
        pygame.K_KP6: '6', pygame.K_KP7: '7', pygame.K_KP8: '8', pygame.K_KP9: '9',
        pygame.K_PLUS: '+',      pygame.K_KP_PLUS: '+',
        pygame.K_MINUS: '-',     pygame.K_KP_MINUS: '-',
        pygame.K_ASTERISK: '*',  pygame.K_KP_MULTIPLY: '*',
        pygame.K_SLASH: '/',     pygame.K_KP_DIVIDE: '/',
        pygame.K_PERIOD: '.',    pygame.K_KP_PERIOD: '.',
        pygame.K_RETURN: 'EQ',  pygame.K_KP_ENTER: 'EQ',
        pygame.K_EQUALS: 'EQ',
        pygame.K_BACKSPACE: 'DEL',
        pygame.K_ESCAPE: 'AC',
        pygame.K_PERCENT: '%',
    }
    action = key_map.get(key)
    if action:
        do_action(action, None)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simple Calculator')

icon_image = pygame.image.load(os.path.join(script_dir, 'img', 'Capture.PNG'))
pygame.display.set_icon(icon_image)

font_path  = os.path.join(script_dir, 'img', 'digital-7.ttf')
Num_font    = pygame.font.Font(font_path, 25)
Num_font_sm = pygame.font.Font(font_path, 18)
Num_font_xs = pygame.font.Font(font_path, 13)
btn_font    = pygame.font.SysFont('Arial', 13, bold=True)

calculator_screen   = pygame.image.load(os.path.join(script_dir, 'img', 'screen.png'))
calculator_keyboard = pygame.image.load(os.path.join(script_dir, 'img', 'keyboard.png'))

Button_0_rect    = pygame.Rect(24,  331, 41, 28)
Button_1_rect    = pygame.Rect(24,  291, 41, 28)
Button_4_rect    = pygame.Rect(24,  251, 41, 28)
Button_7_rect    = pygame.Rect(24,  211, 41, 28)
Button_2_rect    = pygame.Rect(71,  291, 41, 28)
Button_5_rect    = pygame.Rect(71,  251, 41, 28)
Button_8_rect    = pygame.Rect(71,  211, 41, 28)
Button_3_rect    = pygame.Rect(118, 291, 41, 28)
Button_6_rect    = pygame.Rect(118, 251, 41, 28)
Button_9_rect    = pygame.Rect(118, 211, 41, 28)
Button_cong_rect = pygame.Rect(165, 291, 41, 28)
Button_nhan_rect = pygame.Rect(165, 251, 41, 28)
Button_bang_rect = pygame.Rect(212, 331, 41, 28)
Button_tru_rect  = pygame.Rect(212, 291, 41, 28)
Button_chia_rect = pygame.Rect(212, 251, 41, 28)
Button_DEL_rect  = pygame.Rect(165, 211, 41, 28)
Button_AC_rect   = pygame.Rect(212, 211, 41, 28)

Button_dot_rect = pygame.Rect(71,  331, 41, 28)   # dấu .
Button_pm_rect  = pygame.Rect(118, 331, 41, 28)   # +/-
Button_pct_rect = pygame.Rect(165, 331, 41, 28)   # %

NEW_BTN_BG     = (78, 65, 78)
NEW_BTN_BORDER = (50, 40, 50)
NEW_BTN_TEXT   = (215, 205, 215)

Num_list      = []
x_pos         = 36
memory        = ''
result        = 0
times_bang    = 0
highlight_rect  = None
highlight_timer = 0


def draw_new_buttons():
    for rect, label in [
        (Button_dot_rect, '.'),
        (Button_pm_rect,  '+/-'),
        (Button_pct_rect, '%'),
    ]:
        pygame.draw.rect(screen, NEW_BTN_BG, rect, border_radius=4)
        pygame.draw.rect(screen, NEW_BTN_BORDER, rect, width=1, border_radius=4)
        txt = btn_font.render(label, True, NEW_BTN_TEXT)
        screen.blit(txt, txt.get_rect(center=rect.center))



while True:
    screen.blit(calculator_screen, (0, 0))
    screen.blit(calculator_keyboard, (0, 197))
    draw_new_buttons()


    for surf, pos in Num_list:
        screen.blit(surf, pos)


    if highlight_timer > 0:
        hl = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
        hl.fill((255, 255, 255, 55))
        screen.blit(hl, highlight_rect.topleft)
        highlight_timer -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Button_event()
        elif event.type == pygame.KEYDOWN:
            Key_event(event.key)  

    pygame.display.update()