import random
import sys
import requests
import cowsay

list_cows = [cowsay.cow, cowsay.cheese]
def bullcows (guess: str, secret: str) -> (int, int):
    bull = sum(i == j for i, j in zip(guess, secret))
    doubles = sum(min(guess.count(i), secret.count(i)) for i in set(guess))
    cows = doubles - bull
    return bull, cows

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    word = random.choice(words)
    cnt = 0
    while 1:
        tr = ask("Введите слово: ", words)
        cnt += 1
        b, c = bullcows(tr, word)
        inform("Быки: {}, Коровы: {}", b, c)
        if b == len(word):
            print('Победа', cnt)
            return cnt

def ask(prompt: str, valid: list[str] = None) -> str:
    while 1:
        word = input(prompt).strip().lower()
        if not valid or word in valid:
            return word
        cowsay.cow("Такого слова нет в словаре")

def inform(format_string: str, bulls: int, cows:int) -> None:
    rand_cow = random.choice(list_cows)
    rand_cow(format_string.format(bulls, cows))

if len(sys.argv) < 2:
    print("Использование: python -m bullscows словарь [длина]")
    sys.exit(1)
dict = sys.argv[1]
if (len(sys.argv) > 2):
    l = int(sys.argv[2])
else:
    l = 5

if dict.startswith("http"):
    responce = requests.get(dict)
    responce.raise_for_status()
    words = [word.strip().lower() for word in responce.text.splitlines() if len(word.strip()) == l]
else:
    with open(dict, encoding="utf-8") as f:
        words = [word.strip().lower() for word in f if len(word.strip()) == l]

if not words:
    print("Словарь пуст или нет слов нужной длины.")
    sys.exit(1)
gameplay(ask, inform, words)