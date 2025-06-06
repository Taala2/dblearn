# Урок 1: SELECT & FROM

## Введение в SELECT

В основе работы с базами данных лежит возможность извлекать из них данные. В SQL для этого используется оператор `SELECT`. Оператор `SELECT` позволяет получить данные из одной или нескольких таблиц.

Базовый синтаксис оператора `SELECT`:

```sql
SELECT столбец1, столбец2, ...
FROM таблица;
```

## Выбор всех столбцов

Чтобы выбрать все столбцы из таблицы, используйте символ звездочки (*):

```sql
SELECT *
FROM таблица;
```

Например, чтобы выбрать все данные из таблицы `customers`, мы можем написать:

```sql
SELECT *
FROM customers;
```

Этот запрос вернет все строки и все столбцы из таблицы `customers`.

## Выбор конкретных столбцов

Если вам нужны только определенные столбцы, вы можете указать их имена через запятую:

```sql
SELECT имя_столбца1, имя_столбца2
FROM таблица;
```

Например, если мы хотим получить только имена пользователей и их электронные адреса из таблицы `users`:

```sql
SELECT username, email
FROM users;
```

Этот запрос вернет все строки из таблицы `users`, но только столбцы `username` и `email`.

## Порядок столбцов в результате

Порядок столбцов в результате запроса определяется порядком, в котором вы указываете столбцы в операторе `SELECT`. Например:

```sql
SELECT email, username
FROM users;
```

Этот запрос вернет сначала столбец `email`, а затем столбец `username`.

## Псевдонимы столбцов

Вы можете изменить заголовки столбцов в результате запроса, используя псевдонимы (aliases). Для этого используется ключевое слово `AS`:

```sql
SELECT имя_столбца AS псевдоним
FROM таблица;
```

Например:

```sql
SELECT username AS имя_пользователя, email AS электронная_почта
FROM users;
```

Слово `AS` можно опустить, но его использование делает запрос более читаемым:

```sql
SELECT username имя_пользователя, email электронная_почта
FROM users;
```

## Константы и выражения

В операторе `SELECT` можно указывать не только имена столбцов, но и константы и выражения:

```sql
SELECT 'Привет, мир!' AS приветствие, 2 + 2 AS сумма;
```

Этот запрос вернет одну строку с двумя столбцами: `приветствие` со значением "Привет, мир!" и `сумма` со значением 4.

Выражения могут включать столбцы таблицы:

```sql
SELECT product_name, price, price * 0.9 AS sale_price
FROM products;
```

Этот запрос вернет название продукта, его оригинальную цену и цену со скидкой 10%.

## Устранение дубликатов с DISTINCT

Если вы хотите получить только уникальные значения столбца, используйте ключевое слово `DISTINCT`:

```sql
SELECT DISTINCT столбец
FROM таблица;
```

Например, чтобы получить список уникальных категорий продуктов:

```sql
SELECT DISTINCT category
FROM products;
```

`DISTINCT` также работает с несколькими столбцами, в этом случае он удаляет дубликаты комбинаций значений:

```sql
SELECT DISTINCT city, country
FROM customers;
```

## Комментарии в SQL

В SQL есть два типа комментариев:

1. Однострочные комментарии начинаются с `--`:

```sql
-- Это однострочный комментарий
SELECT * FROM users;
```

2. Многострочные комментарии заключаются между `/*` и `*/`:

```sql
/* Это
многострочный
комментарий */
SELECT * FROM users;
```

Комментарии полезны для документирования ваших запросов и временного отключения частей запроса.

## Заключение

В этом уроке мы изучили базовые операции выборки данных с использованием операторов `SELECT` и `FROM`. Мы научились выбирать все или конкретные столбцы, использовать псевдонимы, устранять дубликаты с помощью `DISTINCT`, а также использовать константы и выражения в запросах.

В следующем уроке мы изучим оператор `WHERE`, который позволяет фильтровать данные по определенным условиям.