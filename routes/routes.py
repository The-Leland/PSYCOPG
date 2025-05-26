


from flask import Blueprint, request
from controllers.companies_controller import (
    create_company,
    get_all_companies,
    get_company_by_id,
    update_company,
    delete_company
)

companies_bp = Blueprint('companies', __name__)

@companies_bp.route('/company', methods=['POST'])
def create():
    return create_company(request.json)

@companies_bp.route('/companies', methods=['GET'])
def get_all():
    return get_all_companies()

@companies_bp.route('/company/<string:company_id>', methods=['GET'])
def get_by_id(company_id):
    return get_company_by_id(company_id)

@companies_bp.route('/company/<string:company_id>', methods=['PUT'])
def update(company_id):
    return update_company(company_id, request.json)

@companies_bp.route('/company/delete', methods=['DELETE'])
def delete():
    return delete_company(request.json.get("company_id"))
