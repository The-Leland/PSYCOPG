

from flask import jsonify
from db import get_db_connection
import uuid

def create_product(data):
    conn = get_db_connection()
    cur = conn.cursor()
    product_id = str(uuid.uuid4())
    try:
        cur.execute(
            """
            INSERT INTO Products (product_id, company_id, company_name, price, description, active)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
            """,
            (product_id, data['company_id'], data['company_name'], data['price'], data['description'], data.get('active', True))
        )
        product = cur.fetchone()
        conn.commit()
        return jsonify({"product": product}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

def get_all_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.*, 
            w.warranty_id, 
            w.warranty_months,
            ARRAY(
                SELECT c.category_name
                FROM ProductsCategoriesXref pcx
                JOIN Categories c ON pcx.category_id = c.category_id
                WHERE pcx.product_id = p.product_id
            ) AS categories
        FROM Products p
        LEFT JOIN Warranties w ON p.product_id = w.product_id;
    """)
    products = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"products": products})

def get_active_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Products WHERE active = true;")
    products = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"products": products})

def get_product_by_id(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.*, 
            w.warranty_id, 
            w.warranty_months,
            ARRAY(
                SELECT c.category_name
                FROM ProductsCategoriesXref pcx
                JOIN Categories c ON pcx.category_id = c.category_id
                WHERE pcx.product_id = p.product_id
            ) AS categories
        FROM Products p
        LEFT JOIN Warranties w ON p.product_id = w.product_id
        WHERE p.product_id = %s;
    """, (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if product:
        return jsonify({"product": product})
    return jsonify({"error": "Product not found"}), 404

def update_product(product_id, data):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE Products
            SET price = %s,
                description = %s,
                active = %s
            WHERE product_id = %s
            RETURNING *;
        """, (
            data['price'], 
            data['description'], 
            data['active'], 
            product_id
        ))
        updated = cur.fetchone()
        conn.commit()
        if updated:
            return jsonify({"product": updated})
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Products WHERE product_id = %s RETURNING *;", (product_id,))
        deleted = cur.fetchone()
        conn.commit()
        if deleted:
            return jsonify({"deleted": deleted})
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

def get_products_by_company_id(company_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Products WHERE company_id = %s;", (company_id,))
    products = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"products": products})

def create_product_category(data):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO ProductsCategoriesXref (product_id, category_id) VALUES (%s, %s) RETURNING *;",
            (data['product_id'], data['category_id'])
        )
        xref = cur.fetchone()
        conn.commit()
        return jsonify({"xref": xref}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

