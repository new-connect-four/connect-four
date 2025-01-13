from src.core.game import Game


def main():
    game = Game()

    # game loop: drawing board -> waiting for player input -> making move on game object -> refresh board

    if game.winner:
        print(f"Player {game.winner} won!")
    else:
        print("It is a draw")


if __name__ == "__main__":
    main()
