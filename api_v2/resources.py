from flask_restx import Namespace, Resource, fields
from flask import request
from database import (
    get_all_books, 
    get_book_by_id, 
    create_book, 
    update_book, 
    delete_book, 
    get_statistics,
    search_books
)

api_v2_ns = Namespace('literature', description='Операции с литературными произведениями')

book_model = api_v2_ns.model('Book', {
    'id': fields.Integer(required=True, description='Идентификатор книги'),
    'title': fields.String(required=True, description='Название книги'),
    'author': fields.String(required=True, description='Имя автора'),
    'year': fields.Integer(required=True, description='Год издания'),
    'genre': fields.String(required=True, description='Жанр')
})

new_book_model = api_v2_ns.model('NewBook', {
    'title': fields.String(required=True, description='Название книги'),
    'author': fields.String(required=True, description='Имя автора'),
    'year': fields.Integer(required=True, description='Год издания'),
    'genre': fields.String(required=True, description='Жанр')
})

@api_v2_ns.route('/')
class BookList(Resource):
    def get(self):
        """
        Получить список всех книг с фильтрацией и сортировкой
        ---
        tags:
          - Литература (Расширенный API)
        parameters:
          - name: genre
            in: query
            type: string
            description: Фильтр по жанру
          - name: year_min
            in: query
            type: integer
            description: Минимальный год издания
          - name: sort_by
            in: query
            type: string
            enum: [id, title, author, year, genre]
            description: Поле для сортировки
          - name: order
            in: query
            type: string
            enum: [asc, desc]
            default: asc
            description: Порядок сортировки
        responses:
          200:
            description: Список книг
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        """
        args = request.args
        genre = args.get('genre')
        year_min = args.get('year_min', type=int)
        sort_by = args.get('sort_by', 'id')
        order = args.get('order', 'asc')
        
        books = search_books(genre=genre, year_min=year_min, sort_by=sort_by, order=order)
        return books

    def post(self):
        """
        Добавить новую книгу
        ---
        tags:
          - Литература (Расширенный API)
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/NewBook'
        responses:
          201:
            description: Книга успешно добавлена
            schema:
              $ref: '#/definitions/Book'
        """
        data = request.json
        new_book = create_book(
            title=data['title'],
            author=data['author'],
            year=data['year'],
            genre=data['genre']
        )
        return new_book, 201

@api_v2_ns.route('/<int:book_id>')
@api_v2_ns.param('book_id', 'Идентификатор книги')
@api_v2_ns.response(404, 'Книга не найдена')
class BookItem(Resource):
    def get(self, book_id):
        """
        Получить книгу по ID
        ---
        tags:
          - Литература (Расширенный API)
        responses:
          200:
            description: Данные книги
            schema:
              $ref: '#/definitions/Book'
        """
        book = get_book_by_id(book_id)
        if not book:
            api_v2_ns.abort(404, f"Книга с ID {book_id} не найдена")
        return book

    def put(self, book_id):
        """
        Обновить книгу полностью
        ---
        tags:
          - Литература (Расширенный API)
        parameters:
          - in: body
            name: body
            schema:
              $ref: '#/definitions/NewBook'
        responses:
          200:
            description: Книга обновлена
            schema:
              $ref: '#/definitions/Book'
        """
        existing = get_book_by_id(book_id)
        if not existing:
            api_v2_ns.abort(404, f"Книга с ID {book_id} не найдена")
            
        data = request.json
        updated_book = update_book(
            book_id=book_id,
            title=data['title'],
            author=data['author'],
            year=data['year'],
            genre=data['genre']
        )
        return updated_book

    def delete(self, book_id):
        """
        Удалить книгу
        ---
        tags:
          - Литература (Расширенный API)
        responses:
          204:
            description: Книга удалена
        """
        existing = get_book_by_id(book_id)
        if not existing:
            api_v2_ns.abort(404, f"Книга с ID {book_id} не найдена")
            
        delete_book(book_id)
        return '', 204

@api_v2_ns.route('/stats')
class BookStats(Resource):
    def get(self):
        """
        Получить статистику по году издания
        ---
        tags:
          - Литература (Расширенный API)
        responses:
          200:
            description: Статистические данные
            schema:
              type: object
              properties:
                min_year:
                  type: integer
                  description: Самый ранний год издания
                max_year:
                  type: integer
                  description: Самый поздний год издания
                avg_year:
                  type: number
                  description: Средний год издания
                total_books:
                  type: integer
                  description: Общее количество книг
        """
        return get_statistics()