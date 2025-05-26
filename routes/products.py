


from flask import Blueprint, request
from controllers.products_controller import (
    create_product,
    get_all_products,
    get_active_products,
    get_product_by_id,
    update_product,
    delete_product,
    get_products_by_company_id,
    create_product_category
)

products_bp = Blueprint('products', __name__)

@products_bp.route('/product', methods=['POST'])
def create():
    return create_product(request.json)

@products_bp.route('/products', methods=['GET'])
def get_all():
    return get_all_products()

@products_bp.route('/products/active', methods=['GET'])
def get_active():
    return get_active_products()

@products_bp.route('/product/<string:product_id>', methods=['GET'])
def get_by_id(product_id):
    return get_product_by_id(product_id)

@products_bp.route('/product/<string:product_id>', methods=['PUT'])
def update(product_id):
    return update_product(product_id, request.json)

@products_bp.route('/product/delete', methods=['DELETE'])
def delete():
    return delete_product(request.json.get("product_id"))

@products_bp.route('/product/company/<string:company_id>', methods=['GET'])
def get_by_company(company_id):
    return get_products_by_company_id(company_id)

@products_bp.route('/product/category', methods=['POST'])
def add_product_category():
    return create_product_category(request.json)
