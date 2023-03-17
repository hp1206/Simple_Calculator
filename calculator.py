import pygame,sys
pygame.init()


def Button_event():
    global Num_list,x_pos,memory,result,times_bang
    if Button_0_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('0',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='0'
    elif Button_1_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('1',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=4
        memory+='1'
    elif Button_2_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('2',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='2'
    elif Button_3_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('3',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='3'
    elif Button_4_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('4',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='4'
    elif Button_5_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('5',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='5'
    elif Button_6_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('6',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='6'
    elif Button_7_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('7',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='7'
    elif Button_8_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('8',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='8'
    elif Button_9_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('9',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='9'
    elif Button_cong_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('+',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='+'
    elif Button_tru_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('-',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='-'
    elif Button_nhan_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('*',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='*'
    elif Button_chia_rect.collidepoint(pygame.mouse.get_pos()):
        Num = Num_font.render('/',True,(41,28,41))
        Num_list.append((Num,(x_pos,107)))
        x_pos+=11
        memory+='/'
    elif len(memory)>0:
        if Button_DEL_rect.collidepoint(pygame.mouse.get_pos()):
            if memory[-1]=='1': 
                x_pos-=4
            else:
                x_pos-=11
            if x_pos<36:
                x_pos = 36
            Num_list.remove(Num_list[-1])
            memory = memory[:-1]
            print(memory)
            times_bang = 0
        elif Button_AC_rect.collidepoint(pygame.mouse.get_pos()):
            Num_list,memory = [],''
            x_pos = 36
            times_bang = 0
        elif Button_bang_rect.collidepoint(pygame.mouse.get_pos()) and times_bang == 0:
            times_bang = 1
            if memory.count('+') == memory.count('-') == memory.count('*') == memory.count('/') == 0:
                result = memory
            else:
                for count in range(len(memory)-1):
                    if (ord(memory[count])<ord('0')) or (ord(memory[count])>ord('9')):
                        if memory[count] =='+':
                            result = int(memory[:count])+int(memory[count+1:])
                        elif memory[count] =='-':
                            result = int(memory[:count])-int(memory[count+1:])
                        elif memory[count] =='*':
                            result = int(memory[:count])*int(memory[count+1:])
                        else:
                            result = int(memory[:count])//int(memory[count+1:])
            result = str(result)
            x_pos_result = 236 - (result.count('1')*4+(len(result)-result.count('1'))*11-2)
            Num = Num_font.render(result,True,(41,28,41))
            Num_list.append((Num,(x_pos_result,152)))
            memory+='='
            x_pos+=11


screen = pygame.display.set_mode((274,396))
pygame.display.set_caption('Simple Calculator')


Num_font = pygame.font.Font('img/digital-7.ttf',25)
calculator_screen = pygame.image.load('img/screen.png')
calculator_keyboard = pygame.image.load('img/keyboard.png')


Button_0_rect    = pygame.Rect(24,331,41,28)
Button_1_rect    = pygame.Rect(24,291,41,28)
Button_4_rect    = pygame.Rect(24,251,41,28)
Button_7_rect    = pygame.Rect(24,211,41,28)
Button_2_rect    = pygame.Rect(71,291,41,28)
Button_5_rect    = pygame.Rect(71,251,41,28)
Button_8_rect    = pygame.Rect(71,211,41,28)
Button_3_rect    = pygame.Rect(118,291,41,28)
Button_6_rect    = pygame.Rect(118,251,41,28)
Button_9_rect    = pygame.Rect(118,211,41,28)
Button_cong_rect = pygame.Rect(165,291,41,28)
Button_nhan_rect = pygame.Rect(165,251,41,28)
Button_bang_rect = pygame.Rect(212,331,41,28)
Button_tru_rect  = pygame.Rect(212,291,41,28)
Button_chia_rect = pygame.Rect(212,251,41,28)
Button_DEL_rect  = pygame.Rect(165,211,41,28)
Button_AC_rect   = pygame.Rect(212,211,41,28)


Num_list = []
x_pos = 36
memory = ''
result = 0
times_bang = 0


while True:
    screen.blit(calculator_screen,(0,0))
    screen.blit(calculator_keyboard,(0,197))

    for Num,pos in Num_list:
        screen.blit(Num,pos)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Button_event()

    pygame.display.update()