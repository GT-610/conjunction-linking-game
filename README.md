# Conjuctions Linking game (联结词连连看)
Small conjuction linking game fully written in Python.

## Run from code
The game is developed in Python 3.12. Make sure you have at least Python 3.10 or above.

1. Install the requirements:

    ```bash
    pip install -r requirements.txt
    ```

2. Run `main.py`:

    ```bash
    python main.py
    ```

## Compile
1. Install `pyinstaller`:

    ```bash
    pip install pyinstaller
    ```

2. Run:

    ```bash
    pyinstaller --onefile --noconsole main.py
    ```

3. Copy `assets/`, `saves/` folder to the build location.

4. Run `main.exe`.

## License
All code is under [MIT License](LICENSE).

Assets used in this project are licensed under their respective licenses.