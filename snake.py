from engine import Engine
import keyboard, random, time

class Snake:
    def __init__(self):
        self.body = [(1,1)]
        self.direction = 1 # 0: up, 1: right, 2: down, 3: left
    
    def len(self):
        return len(self.body)
    
    def set_direction(self, direction):
        if self.direction % 2 != direction % 2:
            self.direction = direction
    
    def move(self):
        # move tail
        for i in range(self.len()-1, 0, -1):
            self.body[i] = self.body[i-1]
        # move head
        match self.direction:
            case 0:
                self.body[0] = (self.body[0][0]-1, self.body[0][1])
            case 1:
                self.body[0] = (self.body[0][0], self.body[0][1]+1)
            case 2:
                self.body[0] = (self.body[0][0]+1, self.body[0][1])
            case 3:
                self.body[0] = (self.body[0][0], self.body[0][1]-1)

    def grow(self):
        self.body.append(self.body[-1])

class Game(Engine):
    def __init__(self):
        super().__init__()
        self.snake = Snake()
        self.fruits = []
        self.set_inputs()
        self.symbols.update({2: 'O'})

    def set_inputs(self):
        keyboard.add_hotkey('w', lambda : self.snake.set_direction(0))
        keyboard.add_hotkey('d', lambda : self.snake.set_direction(1))
        keyboard.add_hotkey('s', lambda : self.snake.set_direction(2))
        keyboard.add_hotkey('a', lambda : self.snake.set_direction(3))
        keyboard.add_hotkey('up arrow', lambda : self.snake.set_direction(0))
        keyboard.add_hotkey('right arrow', lambda : self.snake.set_direction(1))
        keyboard.add_hotkey('down arrow', lambda : self.snake.set_direction(2))
        keyboard.add_hotkey('left arrow', lambda : self.snake.set_direction(3))

    def check_collision(self):

        # snake collide with itself
        if self.snake.body[0] in self.snake.body[1:]:
            return True
        
        # snake collide with border
        if self.snake.body[0][0] == 0 or self.snake.body[0][0] == self.display.shape[0]-1:
            return True
        if self.snake.body[0][1] == 0 or self.snake.body[0][1] == self.display.shape[1]-1:
            return True

        return False
  
    def draw_snake(self):
        for i, j in self.snake.body:
            self.display[i, j] = 1

    def generate_fruit(self):
        if random.randint(0, 100**len(self.fruits)) < 10:
            x, y = random.randint(1, self.display.shape[0]-2), random.randint(1, self.display.shape[1]-2)
            if (x, y) not in self.snake.body:
                self.fruits.append((x, y))
        return

    def draw_fruit(self):
        for i, j in self.fruits:
            self.display[i, j] = 2

    def eat_fruit(self):
        if self.snake.body[0] in self.fruits:
            self.fruits.remove(self.snake.body[0])
            self.snake.grow()

    def get_score(self):
        return (self.snake.len()-1) * 10

    def game_over(self):
        stats = """     
             _______  _______  __   __  _______    _______  __   __  _______  ______   
            |       ||   _   ||  |_|  ||       |  |       ||  | |  ||       ||    _ |  
            |    ___||  |_|  ||       ||    ___|  |   _   ||  |_|  ||    ___||   | ||  
            |   | __ |       ||       ||   |___   |  | |  ||       ||   |___ |   |_||_ 
            |   ||  ||       ||       ||    ___|  |  |_|  ||       ||    ___||    __  |
            |   |_| ||   _   || ||_|| ||   |___   |       | |     | |   |___ |   |  | |
            |_______||__| |__||_|   |_||_______|  |_______|  |___|  |_______||___|  |_|
        """
        stats += f'\n\nScore: {self.get_score()}\n'
        stats += f'Eaten fruits: {self.snake.len()-1}\n'
        print(stats)

    def update(self):
        self.snake.move()
        self.generate_fruit()
        self.draw_fruit()
        self.draw_snake()
        if self.check_collision():
            self.draw()
            time.sleep(1)
            self.clear()
            self.game_over()
            return True
        self.eat_fruit()
        print('Score:',self.get_score())
        return False
    
    def main_screen(self):
        frame = 0
        selected = 0
        enter = False

        def change_selection(a: int):
            nonlocal selected
            selected = a % 3

        def confirm_selection():
            nonlocal enter
            enter = True

        keyboard.add_hotkey('up arrow', lambda : change_selection(selected-1))
        keyboard.add_hotkey('down arrow', lambda : change_selection(selected+1))
        keyboard.add_hotkey('enter', lambda : confirm_selection())

        while True:
            self.clear()
            print("""
                 _______  __    _  _______  ___   _  _______ 
                |       ||  |  | ||   _   ||   | | ||       |
                |  _____||   |_| ||  |_|  ||   |_| ||    ___|
                | |_____ |       ||       ||      _||   |___ 
                |_____  ||  _    ||       ||     |_ |    ___|
                 _____| || |  |  ||   _   ||    _  ||   |___ 
                |_______||_|  |__||__| |__||___| |_||_______|\n
                """)
            
            print(f"\t\t\t       {'>' if selected == 0 and frame % 8 != 0 else ' '} Start Game")
            print(f"\t\t\t       {'>' if selected == 1 and frame % 8 != 0 else ' '} Commands")
            print(f"\t\t\t       {'>' if selected == 2 and frame % 8 != 0 else ' '} Quit")
            print("\n\n\n")
            print("Version 0.1")
            print("made by: cocco.exe")
            print("Copyright (c) 2024, All rights reserved.")
            frame += 1
            time.sleep(1/10)
            if enter:
                break
        
        match selected:
            case 0:
                self.loop() 
            case 1:
                self.commands_screen()
            case 2:
                return True
            
        return False

    def commands_screen(self):
        frame = 0
        enter = False

        def confirm_selection():
            nonlocal enter
            enter = True

        keyboard.add_hotkey('enter', lambda : confirm_selection())

        while True:
            self.clear()
            print("""
                Commands:
                - Use the arrow keys or WASD to move the snake
                - Eat the fruits to grow
                - Don't collide with the borders or yourself
                \n""")
            print(f"\t\t\t       {'>' if frame % 8 != 0 else ' '} Main Menu")
            frame += 1
            time.sleep(1/10)
            if enter:
                break
            
        self.main_screen()

def main():
    while True:
        game = Game()
        if game.main_screen(): break
        print("Press enter to return to the main menu.")
        keyboard.wait('enter')


if __name__ == "__main__":
    main()
