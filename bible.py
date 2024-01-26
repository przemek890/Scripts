import requests

timeout = 0.5   # maximum time to generate a quote
enabled = 0     # turn on / turn off the quote generator -> 1 / 0

def get_random_bible_quote():
    if enabled:
        try:
            url = "https://bible-api.com/?random=verse"
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            data = response.json()["verses"][0]
            book_name = data["book_name"]
            chapter = data["chapter"]
            verse = data["verse"]
            text = data["text"]
            return (f"{text} ~ {book_name} {chapter}:{verse}")
        except requests.exceptions.Timeout:
            raise Exception(f"% Quote was not downloaded in the requested {timeout} seconds")
    else:
        print("% Quote generation turned off")
        exit(0)


try:
    quote = get_random_bible_quote()
    print(f"% {quote}")
except Exception:
    print(f"Quote was not downloaded in the requested {timeout} seconds")
