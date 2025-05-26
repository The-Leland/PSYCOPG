
from flask import Blueprint, request
from controllers.categories_controller import (
    create_category,
    get_all_categories,
    get_category_by_id,
    update_category,
    delete_category
)

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/category', methods=['POST'])
def create():
    return create_category(request.json)

@categories_bp.route('/categories', methods=['GET'])
def get_all():
    return get_all_categories()

@categories_bp.route('/category/<string:category_id>', methods=['GET'])
def get_by_id(category_id):
    return get_category_by_id(category_id)

@categories_bp.route('/category/<string:category_id>', methods=['PUT'])
def update(category_id):
    return update_category(category_id, request.json)

@categories_bp.route('/category/delete', methods=['DELETE'])
def delete():
    return delete_category(request.json.get("category_id"))
