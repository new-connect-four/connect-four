<div align="center">
<h3 align="center">Connect 4</h3>
  <p align="center">Implementacja gry Connect 4 w języku Python.</p>
</div>

## Funkcjonalności
- Implementacja gry Connect 4 w Pythonie
- Interfejs graficzny z użyciem biblioteki pygame
- Interfejs tekstowy
- Tryby:
  - Gra dla dwóch graczy (Player vs Player)
  - Gra z botem na dwóch różnych poziomach trudności (Player vs Bot)
- Implementacja podstawowego bota do gry oraz zaawansowanego bota używającego algorytmu minimax 
 
## Wymagania
Aby uruchomić grę potrzebujesz:

- Python 3.10 lub nowszy
- Biblioteka pygame 2.6.1
- Git
- make (opcjonalnie)

<details> 
  <summary>Instalacja Pythona oraz Gita</summary>
  
  ### Linux:
  ```bash
  sudo apt update
  sudo apt upgrade
  sudo apt install python3 python3-venv git
  ```

  ### Windows 11:
  ```bash
  winget install --id=Python.Python.3.12  -e
  winget install --id=Git.Git  -e
  ```
</details>

## Instalacja

1. Sklonuj repozytorium
```bash
git clone https://github.com/new-connect-four/connect-four.git
```

2. Przejdź do głównego katalogu projektu
```bash
cd connect-four
```

3. Zainstaluj wymagane zależności
```bash
pip install -r requirements.txt
```

## Uruchomienie gry

Aby uruchomić grę w trybie graficznym, użyj komendy
```bash
python3 -m src.gui.main
```

Aby uruchomić grę w trybie tekstowym, użyj komendy
```bash
python3 -m src.terminal.main
```

## Instalacja z `make`
```bash
make setup # Tworzy wirtualne środowisko i instaluje wymagane biblioteki
make gui # Uruchamia grę w trybie graficznym
make terminal # Uruchamia grę w trybie tekstowym
make help # Strona z pomocą
```
## Skład zespołu
- Mirosław Janiszewski [@mirkoooslaw](https://github.com/mirkoooslaw)
- Damian Sobczak [@FullerBread2032](https://github.com/FullerBread2032)
- Hubert Machocki [@lambdade-lta](https://github.com/lambdade-lta)
- Julian Walczak [@mndlno](https://github.com/mndlno)
- Artur Dzido [@353548](https://github.com/353548)
- Michał Leśniak
- Jakub Chyliński