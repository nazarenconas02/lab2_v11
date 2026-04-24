import sqlite3
import os

DATABASE = 'literature.db'

def get_db_connection():
    """Создает подключение к базе данных SQLite."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """
    Инициализирует базу данных: 
    создает таблицу 'books', если она не существует, 
    и заполняет её начальными данными, если таблица пуста.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            genre TEXT NOT NULL
        )
    ''')
    
    cursor.execute('SELECT count(*) FROM books')
    if cursor.fetchone()[0] == 0:
        initial_books = [
            ('Война и мир', 'Лев Толстой', 1869, 'классика'),
            ('Преступление и наказание', 'Федор Достоевский', 1866, 'классика'),
            ('Мастер и Маргарита', 'Михаил Булгаков', 1967, 'мистика'),
            ('Солярис', 'Станислав Лем', 1961, 'фантастика'),
            ('Пикник на обочине', 'Аркадий и Борис Стругацкие', 1972, 'фантастика'),
            ('Трудно быть богом', 'Аркадий и Борис Стругацкие', 1964, 'фантастика'),
            ('Мы', 'Евгений Замятин', 1920, 'антиутопия'),
            ('1984', 'Джордж Оруэлл', 1949, 'антиутопия')
        ]
        
        cursor.executemany(
            'INSERT INTO books (title, author, year, genre) VALUES (?, ?, ?, ?)', 
            initial_books
        )
        conn.commit()
        print("База данных инициализирована русскоязычными тестовыми данными.")
    
    conn.close()

def get_all_books(sort_by='id', order='asc'):
    """Получить список всех книг с возможностью сортировки."""
    conn = get_db_connection()
    
    allowed_sort_fields = ['id', 'title', 'author', 'year', 'genre']
    if sort_by not in allowed_sort_fields:
        sort_by = 'id'
    
    order_cmd = 'DESC' if order.lower() == 'desc' else 'ASC'
    
    query = f'SELECT * FROM books ORDER BY {sort_by} {order_cmd}'
    books = conn.execute(query).fetchall()
    conn.close()
    
    return [dict(book) for book in books]

def get_book_by_id(book_id):
    """Получить одну книгу по её идентификатору."""
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    
    if book is None:
        return None
    return dict(book)

def create_book(title, author, year, genre):
    """Добавить новую запись о книге в базу данных."""
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO books (title, author, year, genre) VALUES (?, ?, ?, ?)',
        (title, author, year, genre)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return get_book_by_id(new_id)

def update_book(book_id, title, author, year, genre):
    """Обновить данные существующей книги."""
    conn = get_db_connection()
    conn.execute(
        'UPDATE books SET title = ?, author = ?, year = ?, genre = ? WHERE id = ?',
        (title, author, year, genre, book_id)
    )
    conn.commit()
    conn.close()
    
    return get_book_by_id(book_id)

def delete_book(book_id):
    """Удалить книгу из базы данных по ID."""
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

def get_statistics():
    """Получить статистические данные по году издания книг."""
    conn = get_db_connection()
    stats = conn.execute(
        'SELECT MIN(year) as min_year, MAX(year) as max_year, AVG(year) as avg_year, COUNT(*) as total_books FROM books'
    ).fetchone()
    conn.close()
    
    if stats:
        return dict(stats)
    return {'min_year': 0, 'max_year': 0, 'avg_year': 0, 'total_books': 0}

def search_books(genre=None, year_min=None, sort_by='id', order='asc'):
    """
    Поиск книг с фильтрацией по жанру и году, а также сортировкой.
    """
    conn = get_db_connection()
    query = 'SELECT * FROM books WHERE 1=1'
    params = []
    
    if genre:
        query += ' AND genre = ?'
        params.append(genre)
    
    if year_min:
        query += ' AND year >= ?'
        params.append(year_min)
        
    allowed_sort_fields = ['id', 'title', 'author', 'year', 'genre']
    if sort_by not in allowed_sort_fields:
        sort_by = 'id'
        
    order_cmd = 'DESC' if order.lower() == 'desc' else 'ASC'
    query += f' ORDER BY {sort_by} {order_cmd}'
    
    books = conn.execute(query, params).fetchall()
    conn.close()
    
    return [dict(book) for book in books]