# Урок 2: WHERE - Фильтрация данных

## Введение в WHERE

После того как мы научились извлекать данные из таблиц с помощью `SELECT`, следующий важный шаг - научиться фильтровать эти данные, чтобы получать только нужные записи. Для этого в SQL используется оператор `WHERE`.

Базовый синтаксис оператора `WHERE`:

```sql
SELECT столбец1, столбец2, ...
FROM таблица
WHERE условие;
```

Условие в операторе `WHERE` представляет собой выражение, которое может быть либо истинным (TRUE), либо ложным (FALSE) для каждой строки таблицы. В результат запроса попадают только те строки, для которых условие истинно.

## Операторы сравнения

В условиях `WHERE` можно использовать следующие операторы сравнения:

- `=` - равно
- `<>` или `!=` - не равно
- `<` - меньше
- `>` - больше
- `<=` - меньше или равно
- `>=` - больше или равно

Примеры:

```sql
-- Найти все товары с ценой больше 10000
SELECT *
FROM products
WHERE price > 10000;

-- Найти клиента с идентификатором 3
SELECT *
FROM customers
WHERE id = 3;

-- Найти товары, не относящиеся к категории "Электроника"
SELECT *
FROM products
WHERE category <> 'Электроника';
```

## Логические операторы

Для создания сложных условий используются логические операторы:

- `AND` - логическое И (оба условия должны быть истинными)
- `OR` - логическое ИЛИ (хотя бы одно из условий должно быть истинным)
- `NOT` - логическое отрицание (инвертирует значение условия)

Примеры:

```sql
-- Найти дорогие товары в категории "Электроника"
SELECT *
FROM products
WHERE category = 'Электроника' AND price > 30000;

-- Найти товары из категорий "Одежда" или "Обувь"
SELECT *
FROM products
WHERE category = 'Одежда' OR category = 'Обувь';

-- Найти товары, не относящиеся к категории "Электроника"
SELECT *
FROM products
WHERE NOT category = 'Электроника';
```

## BETWEEN

Оператор `BETWEEN` используется для выбора значений в указанном диапазоне (включительно):

```sql
SELECT *
FROM products
WHERE price BETWEEN 5000 AND 20000;
```

Этот запрос вернет товары с ценой от 5000 до 20000 включительно.

## IN

Оператор `IN` позволяет проверить, совпадает ли значение с любым значением в списке:

```sql
SELECT *
FROM customers
WHERE country IN ('Россия', 'Беларусь');
```

Этот запрос вернет клиентов из России или Беларуси.

## LIKE

Оператор `LIKE` используется для поиска по шаблону в текстовых полях:

- `%` - заменяет любую последовательность символов (включая пустую)
- `_` - заменяет ровно один символ

```sql
-- Найти все товары, название которых начинается с "Нот"
SELECT *
FROM products
WHERE name LIKE 'Нот%';

-- Найти клиентов с именем из 4 букв
SELECT *
FROM customers
WHERE first_name LIKE '____';

-- Найти товары, содержащие слово "спорт" в любом месте названия
SELECT *
FROM products
WHERE name LIKE '%спорт%';
```

## IS NULL и IS NOT NULL

Для проверки, содержит ли столбец значение NULL (пустое значение), используются операторы `IS NULL` и `IS NOT NULL`:

```sql
-- Найти заказы без комментария
SELECT *
FROM orders
WHERE comment IS NULL;

-- Найти заказы с комментарием
SELECT *
FROM orders
WHERE comment IS NOT NULL;
```

## Порядок выполнения операторов

При использовании нескольких логических операторов важно учитывать их приоритет:
1. Сначала выполняются операции в скобках
2. Затем операции `NOT`
3. Затем операции `AND`
4. И в последнюю очередь операции `OR`

Рекомендуется использовать скобки для явного указания порядка выполнения операций:

```sql
SELECT *
FROM products
WHERE (category = 'Электроника' OR category = 'Книги') AND price < 10000;
```

## Пример использования WHERE с другими операторами

```sql
-- Выбрать названия и цены дорогих товаров из категории "Электроника"
SELECT name, price
FROM products
WHERE category = 'Электроника' AND price > 20000;

-- Выбрать уникальные страны, в которых живут клиенты с именем на "А"
SELECT DISTINCT country
FROM customers
WHERE first_name LIKE 'А%';
```

## Заключение

В этом уроке мы изучили оператор `WHERE`, который позволяет фильтровать данные в запросах SQL. Мы рассмотрели различные операторы сравнения, логические операторы, а также специальные операторы `BETWEEN`, `IN`, `LIKE`, `IS NULL` и `IS NOT NULL`. Умение правильно составлять условия фильтрации является важным навыком при работе с базами данных.

В следующем уроке мы познакомимся с операторами `ORDER BY` и `LIMIT`, которые позволяют сортировать результаты запросов и ограничивать количество возвращаемых строк.