from flask_restx import fields

book_model = {
    'id': fields.Integer(required=True, description='Unique ID of the book'),
    'title': fields.String(required=True, description='Title of the book'),
    'author': fields.String(required=True, description='Author name'),
    'year': fields.Integer(required=True, description='Year of publication'),
    'genre': fields.String(required=True, description='Genre of the book')
}
