

from flask import jsonify
from db import get_db_connection
import uuid

def create_category(data):
    conn = get_db_connection()
    cur = conn.cursor()
    category_id = str(uuid.uuid4())
    try:
        cur.execute(
            "INSERT INTO Categories (category_id, category_name) VALUES (%s, %s) RETURNING *;",
            (category_id, data['category_name'])
        )
        new_category = cur.fetchone()
        conn.commit()
        return jsonify({"category": new_category}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

def get_all_categories():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Categories;")
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"categories": categories})

def get_category_by_id(category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Categories WHERE category_id = %s;", (category_id,))
    category = cur.fetchone()
    cur.close()
    conn.close()
    if category:
        return jsonify({"category": category})
    return jsonify({"error": "Category not found"}), 404

def update_category(category_id, data):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE Categories SET category_name = %s WHERE category_id = %s RETURNING *;",
            (data['category_name'], category_id)
        )
        updated = cur.fetchone()
        conn.commit()
        if updated:
            return jsonify({"category": updated})
        return jsonify({"error": "Category not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

def delete_category(category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Categories WHERE category_id = %s RETURNING *;", (category_id,))
        deleted = cur.fetchone()
        conn.commit()
        if deleted:
            return jsonify({"deleted": deleted})
        return jsonify({"error": "Category not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()
