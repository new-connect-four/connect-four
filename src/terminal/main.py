from src.core.game import Game

_default_settings = {
    'PLAYER1_DISC' : 'X',
    'PLAYER2_DISC' : 'O'
}
def initialize_settings():
    settings = {}
    with open("settings.txt", "r+") as file:
        for line in file:
            if "=" in line:
                x, y = line.split("=", 1)
                x = x.strip()
                y = y.strip()
                if x in _default_settings:
                    settings[x] = y
        for key, default_value in _default_settings.items():
            if key not in settings:
                settings[key] = default_value
        file.seek(0)
        file.truncate()
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
                    ("[ Play ]", "start_game", "game"),
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
                print("\n\n")
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
        self.draw()

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
                x = ''
                while True:
                    x = input('\nSelect option: ')
                    try:
                        x = int(x)
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
            case "start_game":
                game.new_game()
                screen.type = "game"
                screen.draw(game)
                while screen.type == "game":
                    if game.winner is not None:
                        while True:
                            x = input(f'\nPLAYER {game.winner} WON! Would you like to play again? (y/n): ')
                            if x == 'y':
                                game.new_game()
                                screen.draw(game)
                                break
                            elif x == 'n':
                                screen.switch("main_menu","menu")
                                break
                            else:
                                screen.draw(game)
                                print("\nInvalid input!")
                    else:
                        x = input(f"\nCurrent turn: Player {game.current_player}\n\nSelect move (or 'e' to return to menu): ")
                        if x == 'e':
                            screen.switch("main_menu", "menu")
                        else:
                            try:
                                x = int(x)
                                game.make_move(x)
                                screen.draw(game)
                            except:
                                screen.draw(game)
                                print("\nInvalid input!")
            case "exit":
                return
if __name__ == "__main__":
    main()
