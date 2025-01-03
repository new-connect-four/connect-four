# connect-four
Implementation of the Connect 4 game

!!! Tresc tego pliku sie zmieni pewnie, narazie daje info jak ogarnac sie z tym repo

Struktura katalogów: \
connect-four\
├── src \
│   ├── core \
│   │   ├── __init__.py \
│   │   ├── const.py \
│   │   └── game.py \
│   ├── gui \
│   │   ├── assets \
│   │   └── main.py \
│   ├── terminal \
│   │   └── main.py \
│   └── utils \
├── tests \
│   ├── core \
│   ├── gui \
│   ├── terminal \
│   └── utils \
├── README.md \
└── requirements.txt

```src\core\game.py``` zawiera po prostu logike gry i stan gry. Kod powinien byc niezalezny do tego czy jest to wersja gui czy terminal

```src\terminal\main.py``` zawiera gre w wersji terminalowej. Kod tam odpowiada za wyswietlanie planszy i to co user wpisuje i zamienia to na
wywołania na obiekcie typy Game

```src\gui\main.py``` zawiera gre w wersji gui. Odpowiada za wyswietlanie planszy i ruchy uzytkownika

```src\gui\assets``` tu beda grafiki itp, wszystko co potrzebne do GUI wersji gry

```tests\core``` tu mozna dac proste testy jednostkowe dla obiektu Game

Aby uruchomic gre w wersji terminal wystarczy wywołać:
```python3 -m src.terminal.main```
