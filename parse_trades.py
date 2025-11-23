import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Базовый адрес списка торгов
BASE_LIST_URL = (
    "https://torgi.org/index.php?class=Auction&action=List&mod=Open&AuctionType=All"
)

# Базовый адрес для карточек лотов
BASE_LOT_URL = "https://torgi.org/index.php"

# Имя локального файла с сохранённой страницей
LOCAL_HTML_NAME = "torgi_auction.html"


def load_html():
    """
    Пытается сначала прочитать локальный файл torgi_auction.html.
    Если файла нет, скачивает страницу с сайта.
    """
    local_path = Path(LOCAL_HTML_NAME)
    if local_path.exists():
        with local_path.open("r", encoding="utf-8") as f:
            return f.read()

    response = requests.get(BASE_LIST_URL, timeout=15)
    response.raise_for_status()
    return response.text


def build_lot_url(href):
    """
    Формирует полный URL карточки лота.
    """
    href = href.strip()
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if href.startswith("?"):
        return BASE_LOT_URL + href
    return BASE_LIST_URL + href


def parse_price(text):
    """
    Преобразует строку вида '2 662 880.00 руб.' в число float.
    Возвращает None, если распознать цену не удалось.
    """
    if not text:
        return None

    cleaned = text.replace("\xa0", " ")
    cleaned = cleaned.replace("руб.", "").replace("руб", "")
    cleaned = cleaned.strip()
    cleaned = cleaned.replace(" ", "")
    cleaned = cleaned.replace(",", ".")

    if not cleaned:
        return None

    if not re.search(r"\d", cleaned):
        return None

    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_lots_from_html(html):
    """
    Разбирает HTML и возвращает список словарей
    с ключами name, price, url.
    """
    soup = BeautifulSoup(html, "html.parser")

    rows = soup.select("tr.auction-table-odd, tr.auction-table-even")

    lots = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 6:
            continue

        name_cell = cells[1]
        price_cell = cells[5]

        link_tag = name_cell.find("a")
        if link_tag is None:
            continue

        name = link_tag.text.strip()
        price_text = price_cell.text.strip()
        price = parse_price(price_text)

        if price is None:
            continue

        href = link_tag.get("href", "").strip()
        if not href:
            continue

        full_url = build_lot_url(href)

        lot = {
            "name": name,
            "price": price,
            "url": full_url,
        }
        lots.append(lot)

    return lots


def ask_price(prompt):
    """
    Считывает цену от пользователя.
    Пустой ввод означает отсутствие ограничения.
    """
    while True:
        raw = input(prompt).strip()

        if raw == "":
            return None

        value = parse_price(raw)
        if value is not None:
            return value

        print(
            "Не удалось распознать число. "
            "Введите цену в любом привычном формате "
            "или оставьте строку пустой."
        )


def filter_lots_by_price(lots, min_price, max_price):
    """
    Фильтрует лоты по заданному диапазону цен.
    """
    result = []
    for lot in lots:
        price = lot["price"]

        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue

        result.append(lot)

    return result


def print_lots(lots):
    """
    Печатает список лотов в человекочитаемом виде.
    """
    if not lots:
        print("По заданному диапазону лоты не найдены.")
        return

    for lot in lots:
        print("-" * 60)
        print(f"Название: {lot['name']}")
        print(f"Цена: {lot['price']:.2f} руб.")
        print(f"Ссылка: {lot['url']}")


def main():
    html = load_html()
    lots = parse_lots_from_html(html)

    if not lots:
        print("Не удалось найти ни одного лота. "
              "Проверьте HTML‑страницу или структуру таблицы.")
        return

    lots.sort(key=lambda lot: lot["price"], reverse=True)

    print(f"Всего найдено лотов: {len(lots)}")
    print("Можно задать минимальную и максимальную цену.")
    print("Пустая строка означает отсутствие ограничения.")

    min_price = ask_price("Минимальная цена: ")
    max_price = ask_price("Максимальная цена: ")

    filtered_lots = filter_lots_by_price(lots, min_price, max_price)

    print()
    print_lots(filtered_lots)


if __name__ == "__main__":
    main()
