


from flask import Blueprint, request
from controllers.warranties_controller import (
    create_warranty,
    get_warranty_by_id,
    update_warranty,
    delete_warranty
)

warranties_bp = Blueprint('warranties', __name__)

@warranties_bp.route('/warranty', methods=['POST'])
def create():
    return create_warranty(request.json)

@warranties_bp.route('/warranty/<string:warranty_id>', methods=['GET'])
def get_by_id(warranty_id):
    return get_warranty_by_id(warranty_id)

@warranties_bp.route('/warranty/<string:warranty_id>', methods=['PUT'])
def update(warranty_id):
    return update_warranty(warranty_id, request.json)

@warranties_bp.route('/warranty/delete', methods=['DELETE'])
def delete():
    return delete_warranty(request.json.get('warranty_id'))
