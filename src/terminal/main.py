from src.core.game import Game
from src.core.bot import Bot
from time import sleep
default_settings = {
    'PLAYER1_DISC' : 'X',
    'PLAYER2_DISC' : 'O'
}


def initialize_settings():
    settings = {}
    try:
        with open("settings.txt", "r") as file:
            for line in file:
                if "=" in line:
                    x, y = line.split("=", 1)
                    x = x.strip()
                    y = y.strip()
                    if x in default_settings:
                        settings[x] = y
    except FileNotFoundError:
        pass
    for key, default_value in default_settings.items():
        if key not in settings:
            settings[key] = default_value
    with open("settings.txt", "w") as file:
        for key, value in settings.items():
            file.write(f"{key} = {value}\n")
    return settings

settings = initialize_settings()



class Screen:
    def __init__(self):
        self.current = "main_menu"
        self.type = "menu"
        self.setting = False

    def screens(self,name):
        match name:
            case "main_menu":
                return [
                    "####################",
                    "#     CONNECT4     #",
                    "####################\n"
                ], [
                    ("[ Play ]", "game", "game_pvp"),
                    ("[ vs Bot ]", "menu", "difficulty_select"),
                    ("[ Settings ]", "menu", "settings_scr"),
                    ("[ Exit ]", "exit", "exit")
                ]
            case "settings_scr":
                return [
                    "####################",
                    "#     SETTINGS     #",
                    "####################\n"
                ], [
                    (f"[ Player 1 Disc ] = '{settings["PLAYER1_DISC"]}'", "setting", "PLAYER1_DISC"),
                    (f"[ Player 2 Disc ] = '{settings["PLAYER2_DISC"]}'\n", "setting", "PLAYER2_DISC"),
                    ("[ Return to Menu ]", "menu", "main_menu")
                ], "menu"
            case "difficulty_select":
                return [
                    "####################",
                    "#  BOT DIFFICULTY  #",
                    "####################\n"
                ], [
                    ("[ Easy ]","game","bot_easy"),
                    ("[ Hard ]\n","game","bot_hard"),
                    ("[ Return to Menu ]", "menu", "main_menu")
                ]

    def draw(self, game=None):
        curr = self.screens(self.current)
        scrtype = self.type
        match scrtype:
            case "menu":
                header = curr[0]
                options = curr[1]
                for i in header:
                    print(i)
                for i in range(len(options)):
                    print(i, options[i][0], sep=' - ')
            case "game":
                d = (" ",settings["PLAYER1_DISC"],settings["PLAYER2_DISC"])
                for i in game.board:
                    for j in i:
                        print(f"[{d[j]}",end=']')
                    print("")
                print("="*21)
                nmbrs = ''.join(f" {x} " for x in range(7))
                print(nmbrs)
    def switch(self,screen,scrtype):
        self.type = scrtype
        if scrtype == "setting":
            self.setting = screen
            self.current = "change_setting"
        else:
            self.current = screen
            self.setting = False
            if scrtype != "game":
                self.draw()
def checkifdraw(game):
    for i in game.board[0]:
        if i == 0: return False
    return True

def update_settingfile():
    with open("settings.txt", "w+") as file:
        file.seek(0)
        file.truncate()
        for key, value in settings.items():
            file.write(f"{key} = {value}\n")

def change_setting(setting,newvalue):
    settings[setting] = newvalue
    update_settingfile()

def main():
    game = Game()
    screen = Screen()
    screen.draw()
    #update_settingfile()
    while True:
        scrtype = screen.type
        curr = screen.screens(screen.current)
        match scrtype:
            case "menu":
                while True:
                    x = input('\nSelect option: ')
                    try:
                        x = int(x)
                        print('')
                        screen.switch(curr[1][x][2],curr[1][x][1])
                        break
                    except:
                        screen.draw()
                        print("\nInvalid input!")
            case "setting":
                setting = screen.setting
                x = input('\nInput new value: ')
                change_setting(setting,x[0])
                screen.switch("settings_scr","menu")
            case "game":
                if screen.current == "bot_hard":
                    bot = Bot(game,"minimax")
                    screen.current = "game_bot"
                elif screen.current == "bot_easy":
                    bot = Bot(game,"rand")
                    screen.current = "game_bot"
                game.new_game()
                screen.draw(game)
                while screen.type != "menu":
                    if game.winner is not None or checkifdraw(game):
                        while True:
                            wintext = "\nIT'S A DRAW!"
                            if screen.current == "game_bot":
                                if game.winner == 1:
                                    wintext = "\nYOU WIN!"
                                elif game.winner == 2:
                                    wintext = "\nBOT WINS!"
                            else:
                                if game.winner is not None:
                                    wintext = f"\nPLAYER {game.winner} WINS!"
                            x = input(wintext + " Would you like to play again? (y/n): ")
                            if x == 'y':
                                game.new_game()
                                print('')
                                screen.draw(game)
                                break
                            elif x == 'n':
                                print('')
                                screen.switch("main_menu","menu")
                                break
                            else:
                                screen.draw(game)
                                print("\nInvalid input!")
                    else:
                        if screen.current == "game_bot":
                            text = "\nYour turn!\n\n"
                        else:
                            text = f"\nCurrent turn: Player {game.current_player}\n\n"
                        x = input(text + "Select move (or 'e' to return to menu): ")
                        if x == 'e':
                            screen.switch("main_menu", "menu")
                        else:
                            try:
                                x = int(x)
                                game.make_move(x)
                                screen.draw(game)
                                if screen.current == "game_bot" and game.winner is None:
                                    print("\nBot's turn.\n")
                                    sleep(0.75)
                                    bot.make_move()
                                    screen.draw(game)
                            except:
                                screen.draw(game)
                                print("\nInvalid input!")
            case "exit":
                return
if __name__ == "__main__":
    main()
