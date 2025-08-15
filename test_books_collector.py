import pytest
from main import BooksCollector

# Фикстура для создания экземпляра BooksCollector перед каждым тестом
@pytest.fixture
def collector():
    return BooksCollector()

# 1. Тесты для add_new_book
@pytest.mark.parametrize('name, expected', [
    ('Война и мир', True),      # нормальное название
    ('A' * 40, True),           # 40 символов (максимум)
    ('', False),                # пустая строка
    ('A' * 41, False),          # 41 символ (слишком длинное)
    ('   ', True),              # пробелы
    ('Книга с !@#$%^&*', True)  # спецсимволы
])
def test_add_new_book(collector, name, expected):

    collector.add_new_book(name)
    assert (name in collector.books_genre) == expected

def test_add_duplicate_book(collector):
    collector.add_new_book('Преступление и наказание')
    collector.add_new_book('Преступление и наказание')
    assert len(collector.books_genre) == 1

# 2. Тесты для set_book_genre
def test_set_valid_genre(collector):
    collector.add_new_book('Марсианин')
    collector.set_book_genre('Марсианин', 'Фантастика')
    assert collector.get_book_genre('Марсианин') == 'Фантастика'

def test_set_invalid_genre(collector):
    collector.add_new_book('Оно')
    collector.set_book_genre('Оно', 'Несуществующий жанр')
    assert collector.get_book_genre('Оно') == ''

def test_set_genre_for_nonexistent_book(collector):
    collector.set_book_genre('Несуществующая книга', 'Фантастика')
    assert 'Несуществующая книга' not in collector.books_genre

# 3. Тесты для get_books_with_specific_genre
def test_get_books_by_genre(collector):
    books = ['Шерлок Холмс', 'Пуаро', 'Десять негритят']
    for book in books:
        collector.add_new_book(book)
        collector.set_book_genre(book, 'Детективы')
    
    detective_books = collector.get_books_with_specific_genre('Детективы')
    assert len(detective_books) == 3
    assert set(detective_books) == set(books)

# 4. Тесты для get_books_for_children
def test_get_children_books(collector):
    child_books = ['Король Лев', 'Чип и Дейл']
    adult_books = ['Оно', 'Дракула']
    
    for book in child_books:
        collector.add_new_book(book)
        collector.set_book_genre(book, 'Мультфильмы')
    
    for book in adult_books:
        collector.add_new_book(book)
        collector.set_book_genre(book, 'Ужасы')
    
    result = collector.get_books_for_children()
    assert len(result) == 2
    assert set(result) == set(child_books)

# 5. Тесты для работы с избранным
def test_add_to_favorites(collector):
    collector.add_new_book('Гарри Поттер')
    collector.add_book_in_favorites('Гарри Поттер')
    assert 'Гарри Поттер' in collector.get_list_of_favorites_books()

def test_add_to_favorites_twice(collector):
    collector.add_new_book('Властелин колец')
    collector.add_book_in_favorites('Властелин колец')
    collector.add_book_in_favorites('Властелин колец')
    assert len(collector.get_list_of_favorites_books()) == 1

def test_remove_from_favorites(collector):
    collector.add_new_book('1984')
    collector.add_book_in_favorites('1984')
    collector.delete_book_from_favorites('1984')
    assert '1984' not in collector.get_list_of_favorites_books()

def test_add_nonexistent_to_favorites(collector):
    collector.add_book_in_favorites('Несуществующая книга')
    assert len(collector.get_list_of_favorites_books()) == 0

# 6. Тест для get_books_genre
def test_get_all_books(collector):
    books = ['Книга1', 'Книга2', 'Книга3']
    for book in books:
        collector.add_new_book(book)
    assert set(collector.get_books_genre().keys()) == set(books)