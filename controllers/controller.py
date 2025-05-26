from flask import jsonify
from db import get_db_connection
import uuid

def create_company(data):
    conn = get_db_connection()
    cur = conn.cursor()
    company_id = str(uuid.uuid4())
    try:
        cur.execute(
            "INSERT INTO Companies (company_id, company_name) VALUES (%s, %s) RETURNING *;",
            (company_id, data['company_name'])
        )
        new_company = cur.fetchone()
        conn.commit()
        return jsonify({"company": new_company}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

def get_all_companies():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Companies;")
    companies = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"companies": companies})

def get_company_by_id(company_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Companies WHERE company_id = %s;", (company_id,))
    company = cur.fetchone()
    cur.close()
    conn.close()
    if company:
        return jsonify({"company": company})
    return jsonify({"error": "Company not found"}), 404

def update_company(company_id, data):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE Companies SET company_name = %s WHERE company_id = %s RETURNING *;",
            (data['company_name'], company_id)
        )
        updated = cur.fetchone()
        conn.commit()
        if updated:
            return jsonify({"company": updated})
        return jsonify({"error": "Company not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

def delete_company(company_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Companies WHERE company_id = %s RETURNING *;", (company_id,))
        deleted = cur.fetchone()
        conn.commit()
        if deleted:
            return jsonify({"deleted": deleted})
        return jsonify({"error": "Company not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()
