
# Тестовое задание

## Описание
Мы предлагаем вам познакомиться с этой прекрасной платежной системой (Stripe), реализовав простой сервер с одной html страничкой, который общается со Stripe и создает платёжные формы для товаров. 


## Установка и запуск (Локально)

```bash
  git clone ...
  cd django_stripe
```
    
```bash
  python3 -m venv *env_name*
  pip install -r requirements.txt
```
```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
```

Сделать один или несколько Item в Django Admin или через `python manage.py shell`. Для этого
```python
  from main.models import Item
```
```python
  Item.objects.create(name="anyname", description="anydescription", price="anyprice")
```
 или другим удобным способ по созданию объектов.
**anyprice** должно быть **число** (**int**).

Далее,

```http
  GET /item/<int:pk>
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `pk` | `int` | **Required**. ID Item в базе данных |

Нажать на кнопку **Buy**, ожидать ответа от Stripe.

# Дополнительные задания
- ✅ Использование environment variables
- ✅ Просмотр Django Моделей в Django Admin панели
- ✅ Запуск приложения на удаленном сервере, доступном для тестирования (Инструкция ниже)
- ✅ Модель Order, в которой можно объединить несколько Item и сделать платеж в Stripe на содержимое Order с общей стоимость всех Items
- ✅ Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe (50%)
- ✅ Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте

# Запуск приложения на удаленном сервере
Перейти по https://urodec777.pythonanywhere.com/ <br>
Начать тестирование согласно локальной установки и запуска