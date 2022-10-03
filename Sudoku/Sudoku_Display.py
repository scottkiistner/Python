from Sudoku_Core import *
import pygame, math
pygame.init()

#Initialize the Pygame Screen
screen_width = 812
screen_height = 812
screen_size = screen_width,screen_height
screen_title = "Python Sudoku App"
screen_icon = pygame.image.load("img\\icon.png")
cell_size = 90

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption(screen_title)
pygame.display.set_icon(screen_icon)
clock = pygame.time.Clock()

game_running = True

game_board = []
game_display = []
note_mode = False
clicking = False
solved_board = []

input_keys = [pygame.K_SPACE,
              pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
              pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_TAB, pygame.K_RETURN]

#Load Images
img_numbers = [pygame.image.load('img\\1.png').convert_alpha(),
               pygame.image.load('img\\2.png').convert_alpha(),
               pygame.image.load('img\\3.png').convert_alpha(),
               pygame.image.load('img\\4.png').convert_alpha(),
               pygame.image.load('img\\5.png').convert_alpha(),
               pygame.image.load('img\\6.png').convert_alpha(),
               pygame.image.load('img\\7.png').convert_alpha(),
               pygame.image.load('img\\8.png').convert_alpha(),
               pygame.image.load('img\\9.png').convert_alpha()]

img_notes = [pygame.image.load('img\\N1.png').convert_alpha(),
               pygame.image.load('img\\N2.png').convert_alpha(),
               pygame.image.load('img\\N3.png').convert_alpha(),
               pygame.image.load('img\\N4.png').convert_alpha(),
               pygame.image.load('img\\N5.png').convert_alpha(),
               pygame.image.load('img\\N6.png').convert_alpha(),
               pygame.image.load('img\\N7.png').convert_alpha(),
               pygame.image.load('img\\N8.png').convert_alpha(),
               pygame.image.load('img\\N9.png').convert_alpha()]

img_board = [pygame.image.load('img\\Cell.png').convert(),
             pygame.image.load('img\\Edit_Cell.png').convert(),
             pygame.image.load('img\\Board.png').convert_alpha(),
             pygame.image.load('img\\Highlight.png').convert_alpha(),
             pygame.image.load('img\\Select.png').convert_alpha(),
             pygame.image.load('img\\Notes.png').convert_alpha(),
             pygame.image.load('img\\Error.png').convert_alpha()]

img_buttons = [pygame.image.load('img\\B_New_1.png').convert(),
               pygame.image.load('img\\B_New_2.png').convert(),
               pygame.image.load('img\\B_Save_1.png').convert(),
               pygame.image.load('img\\B_Save_2.png').convert(),
               pygame.image.load('img\\B_Load_1.png').convert(),
               pygame.image.load('img\\B_Load_2.png').convert(),
               pygame.image.load('img\\B_Solve_1.png').convert(),
               pygame.image.load('img\\B_Solve_2.png').convert()]

def UnselectAll():
    global game_display
    for cell in game_display[0]:
        cell.selected = False

def UnhighlightAll():
    global game_display
    for cell in game_display[0]:
        cell.highlight = False

def SelectAll(data):
    global game_display
    for cell in game_display[0]:
        cell.highlight = False
        if cell.data == data:
            cell.highlight = True

def ClearErrors():
    global game_display
    for cell in game_display[0]:
        cell.error = False

def GetPattern(cell_array):
    resultPattern = ""
    for cell in cell_array:
        resultPattern += str(cell.data)
        print(resultPattern)
    return resultPattern

def GetLinearPos(y, x):
    return x + (y * 9)

def CheckErrors():
    global game_display
    global solved_board
    checkBoard = Board(GetPattern(game_display[0]))
    checkBoard.Print()
    print("Solved: ")
    solved_board.Print()
    ClearErrors()
    UnhighlightAll()

    if checkBoard.rows != solved_board.rows:
        for cRow in checkBoard.rows:
            for cBox in cRow:
                if cBox == 0:
                    continue
                if cBox != solved_board.rows[checkBoard.rows.index(cRow)][cRow.index(cBox)]:
                    game_display[0][GetLinearPos(checkBoard.rows.index(cRow), cRow.index(cBox))].error = True
                    print(GetLinearPos(checkBoard.rows.index(cRow), cRow.index(cBox)))
    #else:
        #print("Puzzle is Solved!")
    

class Cell():
    def __init__(self, data, x, y):
        self.data = data
        self.editable = not bool(self.data)
        self.highlight = False
        self.selected = False
        self.error = False
        self.click = [False, False] #Clicking, Clicked
        
        self.x = x
        self.y = y
        self.cell_img = [img_board[0].copy(), img_board[1].copy(), img_board[3].copy(), img_board[4].copy(), img_board[5].copy(), img_board[6].copy()]
        self.digit_img = [img_numbers[0].copy(),img_numbers[1].copy(),img_numbers[2].copy(),
                          img_numbers[3].copy(),img_numbers[4].copy(),img_numbers[5].copy(),
                          img_numbers[6].copy(),img_numbers[7].copy(),img_numbers[8].copy()]
        self.notes_img = [img_notes[0].copy(),img_notes[1].copy(),img_notes[2].copy(),
                          img_notes[3].copy(),img_notes[4].copy(),img_notes[5].copy(),
                          img_notes[6].copy(),img_notes[7].copy(),img_notes[8].copy()]
        self.notes = [False, False, False,
                      False, False, False,
                      False, False, False]

    def Draw(self):
        global note_mode
        global clicking
        pos = pygame.mouse.get_pos()

        rdata = self.getDimensions()
        rect = pygame.Rect(rdata[0], rdata[1], rdata[2], rdata[2])

        if rect.collidepoint(pos):
            UnselectAll()
            self.selected = True

        if pygame.mouse.get_pressed()[0] == 1:
            if rect.collidepoint(pos):
                if not clicking:
                    ClearErrors()
                    UnhighlightAll()
                    self.highlight = True                    
                    self.click[0] = True
                    clicking = True
                else:
                    self.highlight = True
                    self.click[0] = True
        else:
            self.click[0] = False
            clicking = False

        if pygame.mouse.get_pressed()[2] == 1:            
            if rect.collidepoint(pos):
                if not self.click[1]:
                    SelectAll(self.data)
                    self.click[1] = True
        else:
            self.click[1] = False
                        
        screen.blit(self.cell_img[int(self.editable)], (self.x, self.y))
        if self.data != 0:
            screen.blit(self.digit_img[self.data - 1], (self.x, self.y))
        else:
            counter = 0
            for note in self.notes:
                if note:
                    screen.blit(self.notes_img[counter], (self.x, self.y))
                counter += 1
        if self.highlight:
            if note_mode:
                screen.blit(self.cell_img[4], (self.x, self.y))
            else:
                screen.blit(self.cell_img[2], (self.x, self.y))
        if self.error:
            screen.blit(self.cell_img[5], (self.x, self.y))
        
        if self.selected:
            screen.blit(self.cell_img[3], (self.x, self.y))

    def getDimensions(self):
        return [self.x, self.y, cell_size]

def CreateBoardArray(board, x, y):
    data = [[], ]
    #0 will be the cells list
    #1 will be x
    #2 will be y
    
    pos = [0,0]
    for row in board.rows:
        pos[0] = 0
        for box in row:
            tCell = Cell(box, (pos[0] * cell_size) + x + 1,(pos[1] * cell_size) + y + 1)
            data[0].append(tCell)
            pos[0] += 1
        pos[1] += 1
    data.append(x)
    data.append(y)
    return data

def DrawBoard(board_array):
    gx = board_array[1]
    gy = board_array[2]
    for cell in board_array[0]:
        cell.Draw()
    screen.blit(img_board[2], (gx, gy))


    
def Init():
    global game_board
    global game_display
    global solved_board
    new_board = Board("000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    game_board = new_board.Generate(30)
    game_board.Print()
    Board.solved_counter = []
    solved_board = game_board.Solve(game_board.Copy())
    solved_board.Print()
    game_display = CreateBoardArray(game_board, 0, 0)

def Update():
    global game_running
    global game_state
    global game_display
    global input_keys
    global note_mode
    
    #Main Pygame Event/Input Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == input_keys[12]:
                note_mode = not note_mode
            if event.key == input_keys[0]:
                UnhighlightAll()
            if event.key == input_keys[10] or event.key == input_keys[11]:
                for cell in game_display[0]:
                    if cell.editable and cell.highlight:
                        cell.data = 0
            ik = input_keys
            e = event
            if e.key == ik[1] or e.key == ik[2] or e.key == ik[3] or e.key == ik[4] or e.key == ik[5] or e.key == ik[6] or e.key == ik[7] or e.key == ik[8] or e.key == ik[9]:
                for cell in game_display[0]:
                    if cell.editable and cell.highlight:
                        if note_mode:
                            cell.notes[input_keys.index(event.key) - 1] = not cell.notes[input_keys.index(event.key) - 1]
                        else:
                            cell.data = input_keys.index(event.key)
            if event.key == input_keys[13]:
                CheckErrors()
                
            
            

def Render():
    global game_runnng
    global game_state
    global game_board
    global game_display
    screen.fill((255, 255, 255))
    DrawBoard(game_display)
    pygame.display.flip()            

def main():
    Init()
    while game_running:
        Update()
        Render()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
        
