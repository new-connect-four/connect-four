from src.core.game import Game

_default_settings = {
    'PLAYER1_DISC' : 'X',
    'PLAYER2_DISC' : 'O'
}
settings = {}
with open("settings.txt","w+") as file:
    for line in file:
        x, _, y = line.split()
        if x in _default_settings.keys():
            settings[x] = y

def screens(name):
    match name:
        case "main_menu":
            return [
    ("####################","main_menu"),
    ("#     CONNECT4     #","main_menu"),
    ("####################\n","main_menu"),
    ("Play","start_vsplayer"),
    ("Settings","settings_scr"),
    ("Exit","exit")
            ]
        case "settings_scr":
            return [
    ("####################", "settings_scr"),
    ("#     SETTINGS     #", "settings_scr"),
    ("####################\n", "settings_scr"),
    ("Change Player 1 Disc: '" + str(settings.get("PLAYER1_DISC")) + "'",''),
    ("Change Player 2 Disc: '" + str(settings.get("PLAYER2_DISC")) + "'", ''),
    ("Return to Menu","main_menu")
]


class Screen:
    def __init__(self):
        self.current = "main_menu"

    def draw(self):
        curr = screens(self.current)
        for i in range(len(curr)):
            print(i,curr[i][0])
    def switch(self,n):
        self.current = screens(self.current)[n][1]
        self.draw()
def main():
    game = Game()
    screen = Screen()
    screen.draw()

    while True:
        x = input('')
        print(screen.current)
        screen.switch(int(x))

if __name__ == "__main__":
    main()
