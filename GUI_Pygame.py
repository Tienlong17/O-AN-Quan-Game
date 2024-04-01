import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Màu sắc
white = (255, 255, 255)
Black = (0, 0, 0)
color_background = (38, 116, 250)
# Kích thước cửa sổ
window_size = (1400,700)
# thông số vẽ bảng
cell_size = 150
board_position = (225,200)
# thông số stone
Color_Large_Stone = (43, 43, 8)
Color_Small_Stone = (230, 230, 45)
Size_Large_Stone = 25
Size_Small_Stone = 5
# Khởi tạo cửa sổ
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Trò chơi Ô Ăn Quan")

def Create_Text_Word(a : str, color, size: int):
    '''Ham de tao ghi chu~'''
    font = pygame.font.SysFont("sans",size)
    return  font.render(a,True, color)
# Hàm tạo button
def draw_button(surface, color, x, y, w, h, text, font):
    pygame.draw.rect(surface, color, pygame.Rect(x, y, w, h))
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(center=pygame.Rect(x, y, w, h).center)
    surface.blit(text_surface, text_rect)
# Hàm vẽ bảng game
def draw_board():
    
    for row in range(2):
        for col in range(5):
            pygame.draw.rect(screen, white, (col * cell_size + board_position[0], row * cell_size + board_position[1], cell_size, cell_size), 1)

    # Vẽ hình bán nguyệt ở hai bên
    pygame.draw.arc(screen, white, (board_position[0] - cell_size, board_position[1], cell_size * 2, cell_size * 2), 1.57, -1.57, 1)
    pygame.draw.arc(screen, white, (board_position[0] + 4*cell_size, board_position[1], cell_size * 2, cell_size * 2), -1.57, +1.57, 1)

# Class Stone
class Stone():
    def __init__(self, name, color, size, position):
        self.name = name
        self.color = color
        self.size = size
        self.position = position 
    def draw(self, screen): 
        pygame.draw.circle(screen, self.color, self.position, self.size)
# class Pit hố chứa đá 
class Pit:
    def __init__(self,position):
        self.position = position
        self.stones = []  # Danh sách các viên đá trong hố
        self.selected = False
    def add_stone(self, stone):
        self.stones.append(stone)  # Thêm một viên đá vào hố

    def remove_stone(self, stone):
        self.stones.remove(stone)

    def clear_stones(self):
        self.stones = []    

    def select(self):
            self.selected = True
            print("toi day")

    def unselect(self):
            self.selected = False

    def draw_selection_indicator(self, screen):
        if self.selected:
            # Vẽ tam giác chỉ chỉ bên trái và phải
            pygame.draw.polygon(screen, white, [(self.position[0] - 40, self.position[1] + cell_size // 2), 
                                                 (self.position[0] - 10, self.position[1] + cell_size // 4),
                                                 (self.position[0] - 10, self.position[1] + 3 * cell_size // 4)])

            pygame.draw.polygon(screen, white, [(self.position[0] + cell_size + 40, self.position[1] + cell_size // 2), 
                                                 (self.position[0] + cell_size + 10, self.position[1] + cell_size // 4),
                                                 (self.position[0] + cell_size + 10, self.position[1] + 3 * cell_size // 4)])

# Khởi tạo đối tượng big stone
large_stone_1 = Stone("large_stone", Color_Large_Stone, Size_Large_Stone, (board_position[0] - cell_size/2, board_position[1] + cell_size))
large_stone_2 = Stone("large_stone", Color_Large_Stone, Size_Large_Stone, (board_position[0] + 5.5*cell_size, board_position[1] + cell_size))
# Khởi tạo viên đá nhỏ va hó
pits = []
stones = []
global  inital, choosing_pit 
inital = 1 
choosing_pit = 1 
def Inital():
    # các trạng thái
    global  inital, choosing_pit
    inital = 1  
    choosing_pit = 1
    for row in range(2):
        for col in range(5):
            pit_position = (col * cell_size + board_position[0], row * cell_size + board_position[1])
            pit = Pit(pit_position)
            for i in range(5):
                x = (col * cell_size) + board_position[0] + 50 + (i % 3) * 20 # Điều chỉnh vị trí x dựa trên chỉ số i
                y = (row * cell_size) + board_position[1] + 50 + (i // 3) * 20 # Điều chỉnh vị trí y dựa trên chỉ số i
                stone = Stone(Color_Small_Stone,Color_Small_Stone, Size_Small_Stone, (x,y))
                pit.add_stone(stone)
                stones.append(stone)
            pits.append(pit)
    screen.blit(Create_Text_Word('O An Quan',white,50),(600,20))
    screen.blit(Create_Text_Word('Computer player',white,30),(400,100))
    screen.blit(Create_Text_Word('Player',white,30),(400,570))
    # cac chuc nang ve 
    draw_board()
    large_stone_1.draw(screen)
    large_stone_2.draw(screen)
    for stone in stones:
        stone.draw(screen)
    for pit in pits[5:10]:
        pit.draw_selection_indicator(screen)
        #print("toi day3")
    # tao nut button 
    draw_button(screen, (122, 116, 250),1200, 70, 120, 100, "R: Reset", pygame.font.SysFont(None, 30))
def Reset(): 
    Inital()
    for pit in pits:
        pit.unselect()

# Vòng lặp chính
running = 1 
while running:
    # Xóa màn hình và vẽ lại bảng
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: # thoat game bang phim q 
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_r:
                Reset()      
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Xử lý khi người chơi nhấp chuột
            mouse_pos = pygame.mouse.get_pos()
            # Xác định ô mà người chơi đã nhấp vào
            if choosing_pit == 1: 
                for pit in pits[5:10]:
                    if pit.position[0] < mouse_pos[0] < pit.position[0] + cell_size and pit.position[1] < mouse_pos[1] < pit.position[1] + cell_size:
                        # Đây là ô được chọn bởi người chơi
                        print("Selected Pit:", pit.position)
                        for other_pit in pits[5:10]:
                            if other_pit != pit and other_pit.selected:
                                other_pit.unselect()
                        pit.select()
                        choosing_pit = 0        

            else:
                pygame.time.delay(1000)
                print("thuc hien ham tam giac")
                for pit in pits:
                    pit.unselect()
                choosing_pit = 1        


    
    # thong tin xuat ra man hinh 
    screen.fill(color_background)                 
    if inital == 1:
        Inital()
        initial = 0 


    # Cập nhật màn hình
    pygame.display.flip()

# Kết thúc Pygame
pygame.quit()
sys.exit()
