import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    """Фикстура для создания экземпляра BooksCollector перед каждым тестом"""
    return BooksCollector()

# 1. Тесты для add_new_book
@pytest.mark.parametrize('name, expected', [
    ('Война и мир', True),      # нормальное название
    ('A' * 40, True),           # 40 символов (максимум)
    ('', False),                # пустая строка
    ('A' * 41, False),          # 41 символ (слишком длинное)
    ('   ',  True),             # пробелы (теперь False после исправления)
    ('Книга с !@#$%^&*', True)  # спецсимволы
])
def test_add_new_book(collector, name, expected):
    """Тестирует добавление книги с различными вариантами названий"""
    collector.add_new_book(name)
    assert (collector.get_book_genre(name) == '') == expected

def test_add_duplicate_book(collector):
    """Проверяет, что нельзя добавить книгу с одинаковым названием дважды"""
    book_name = 'Преступление и наказание'
    collector.add_new_book(book_name)
    initial_count = len(collector.get_books_genre())
    collector.add_new_book(book_name)
    assert len(collector.get_books_genre()) == initial_count

# 2. Тесты для set_book_genre
def test_set_valid_genre(collector):
    """Проверяет установку корректного жанра"""
    book_name = 'Марсианин'
    collector.add_new_book(book_name)
    collector.set_book_genre(book_name, 'Фантастика')
    assert collector.get_book_genre(book_name) == 'Фантастика'

def test_set_invalid_genre(collector):
    """Проверяет невозможность установки несуществующего жанра"""
    book_name = 'Оно'
    collector.add_new_book(book_name)
    collector.set_book_genre(book_name, 'Несуществующий жанр')
    assert collector.get_book_genre(book_name) == ''

def test_set_genre_for_nonexistent_book(collector):
    """Проверяет обработку попытки установки жанра для несуществующей книги"""
    initial_books = collector.get_books_genre()
    collector.set_book_genre('Несуществующая книга', 'Фантастика')
    assert collector.get_books_genre() == initial_books

# 3. Тесты для get_books_with_specific_genre
def test_get_books_by_genre(collector):
    """Проверяет фильтрацию книг по жанру"""
    books = ['Шерлок Холмс', 'Пуаро', 'Десять негритят']
    genre = 'Детективы'
    
    for book in books:
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
    
    detective_books = collector.get_books_with_specific_genre(genre)
    assert len(detective_books) == len(books)
    for book in books:
        assert book in detective_books
        assert collector.get_book_genre(book) == genre

# 4. Тесты для get_books_for_children
def test_get_children_books(collector):
    """Проверяет получение книг без возрастных ограничений"""
    child_books = ['Король Лев', 'Чип и Дейл']
    adult_books = ['Оно', 'Дракула']
    
    for book in child_books:
        collector.add_new_book(book)
        collector.set_book_genre(book, 'Мультфильмы')
    
    for book in adult_books:
        collector.add_new_book(book)
        collector.set_book_genre(book, 'Ужасы')
    
    result = collector.get_books_for_children()
    assert len(result) == len(child_books)
    for book in child_books:
        assert book in result
    for book in adult_books:
        assert book not in result

# 5. Тесты для работы с избранным
def test_add_to_favorites(collector):
    """Проверяет добавление книги в избранное"""
    book_name = 'Гарри Поттер'
    collector.add_new_book(book_name)
    collector.add_book_in_favorites(book_name)
    assert book_name in collector.get_list_of_favorites_books()

def test_add_to_favorites_twice(collector):
    """Проверяет невозможность дублирования книг в избранном"""
    book_name = 'Властелин колец'
    collector.add_new_book(book_name)
    collector.add_book_in_favorites(book_name)
    initial_count = len(collector.get_list_of_favorites_books())
    collector.add_book_in_favorites(book_name)
    assert len(collector.get_list_of_favorites_books()) == initial_count

def test_remove_from_favorites(collector):
    """Проверяет удаление книги из избранного"""
    book_name = '1984'
    collector.add_new_book(book_name)
    collector.add_book_in_favorites(book_name)
    collector.delete_book_from_favorites(book_name)
    assert book_name not in collector.get_list_of_favorites_books()

def test_add_nonexistent_to_favorites(collector):
    """Проверяет обработку попытки добавления несуществующей книги в избранное"""
    initial_favorites = collector.get_list_of_favorites_books()
    collector.add_book_in_favorites('Несуществующая книга')
    assert collector.get_list_of_favorites_books() == initial_favorites

# 6. Тест для get_books_genre
def test_get_all_books(collector):
    """Проверяет получение полного списка книг"""
    books = ['Книга1', 'Книга2', 'Книга3']
    for book in books:
        collector.add_new_book(book)
    
    all_books = collector.get_books_genre()
    assert len(all_books) == len(books)
    for book in books:
        assert book in all_books
        assert collector.get_book_genre(book) == ''