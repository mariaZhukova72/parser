# Парсер лотов с сайта Торги.орг

Программа читает HTML‑страницу со списком торгов с площадки Торги.орг, извлекает лоты из таблицы и выводит их, отсортировав от самой высокой цены к самой низкой. Пользователь задаёт минимальную и максимальную цену, и отображаются только лоты, попадающие в указанный диапазон (диапазон можно оставить пустым).

## Откуда берутся данные

Данные берутся из HTML‑страницы списка открытых торгов по всем видам на сайте Торги.орг:  
`https://torgi.org/index.php?class=Auction&action=List&mod=Open&AuctionType=All`.  
Рекомендуется открыть эту страницу в браузере, сохранить её как `torgi_auction.html` и положить файл в корень проекта рядом с `parse_trades.py`. Такая схема с заранее сохранённой страницей часто используется в учебных проектах по парсингу веб‑страниц [web:13].

## Как установить зависимости

1. Клонировать репозиторий:
   ```
   git clone https://github.com/USERNAME/torgi_parser.git
   cd torgi_parser
   ```

2. Создать и активировать виртуальное окружение:
   ```
   python -m venv venv
   # Linux / macOS
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```

3. Установить зависимости:
   ```
   pip install -r requirements.txt
   ```

## Как запустить с примером

1. Убедиться, что в корне проекта есть файл `torgi_auction.html` с сохранённой страницей списка торгов.
2. Запустить программу:
   ```
   python parse_trades.py
   ```
3. В консоли ввести минимальную и максимальную цену (можно оставить поле пустым и просто нажать Enter, чтобы не задавать ограничение).

Пример работы:

```
Всего найдено лотов: 20
Можно задать минимальную и максимальную цену.
Пустая строка означает отсутствие ограничения.
Минимальная цена: 500000
Максимальная цена: 3000000

------------------------------------------------------------
Название: Автомобиль АУДИ Q7, 2019 г.в., г/н Н565РН198 vin WAUZZZ4M3KD028964
Цена: 2025833.33 руб.
Ссылка: https://torgi.org/index.php?class=ArrestAuction&action=View&OID=169154
------------------------------------------------------------
Название: легковой автомобиль HYUNDAI SOLARIS, 2017 г.в., г/н Р003ХР98, VIN Z94K241CBJR038265, цвет: серый, номер кузова ...
Цена: 672000.00 руб.
Ссылка: https://torgi.org/index.php?class=ArrestAuction&action=View&OID=169198
...
```

Лоты выводятся в порядке убывания цены, каждый с названием, числовой ценой и полной ссылкой на страницу лота.
```

[1](https://realpython.com/readme-python-project/)
[2](https://www.makeareadme.com)
[3](https://www.freecodecamp.org/news/how-to-structure-your-readme-file/)
[4](https://packaging.python.org/guides/making-a-pypi-friendly-readme/)
[5](https://docs.python-guide.org/writing/structure/)
[6](https://www.youtube.com/watch?v=12trn2NKw5I)
[7](https://github.com/othneildrew/Best-README-Template)
[8](https://git.ifas.rwth-aachen.de/templates/ifas-python-template/-/blob/master/README.md)