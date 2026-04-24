from flask import Blueprint, jsonify, request
from database import get_all_books, search_books

api_v1_bp = Blueprint('api_v1', __name__, template_folder='templates', static_folder='static')

@api_v1_bp.route('/info')
def info():
    """
    Общая информация о сервисе
    ---
    tags:
      - General Info
    responses:
      200:
        description: Возвращает версию и автора сервиса
        schema:
          id: InfoResponse
          properties:
            service:
              type: string
            version:
              type: string
            author:
              type: string
    """
    return jsonify({
        "service": "Literature Service (SQLite)",
        "version": "1.0",
        "author": "Student"
    })

@api_v1_bp.route('/books/<genre>')
def get_books_by_genre(genre):
    """
    Получить список книг по жанру
    ---
    tags:
      - Books (Simple)
    parameters:
      - name: genre
        in: path
        type: string
        required: true
        enum: ['classic', 'scifi', 'fantasy', 'dystopia', 'all']
        description: Жанр литературы
    responses:
      200:
        description: Список книг
        schema:
          type: array
          items:
            type: object
    """
    if genre == 'all':
        books = get_all_books()
    else:
        books = search_books(genre=genre)
        
    return jsonify(books)