


from flask import jsonify
from db import get_db_connection
import uuid

def create_warranty(data):
    conn = get_db_connection()
    cur = conn.cursor()
    warranty_id = str(uuid.uuid4())
    try:
        cur.execute(
            "INSERT INTO Warranties (warranty_id, product_id, warranty_months) VALUES (%s, %s, %s) RETURNING *;",
            (warranty_id, data['product_id'], data['warranty_months'])
        )
        warranty = cur.fetchone()
        conn.commit()
        return jsonify({"warranty": warranty}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

def get_warranty_by_id(warranty_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Warranties WHERE warranty_id = %s;", (warranty_id,))
    warranty = cur.fetchone()
    cur.close()
    conn.close()
    if warranty:
        return jsonify({"warranty": warranty})
    return jsonify({"error": "Warranty not found"}), 404

def update_warranty(warranty_id, data):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE Warranties SET warranty_months = %s WHERE warranty_id = %s RETURNING *;",
            (data['warranty_months'], warranty_id)
        )
        updated = cur.fetchone()
        conn.commit()
        if updated:
            return jsonify({"warranty": updated})
        return jsonify({"error": "Warranty not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

def delete_warranty(warranty_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Warranties WHERE warranty_id = %s RETURNING *;", (warranty_id,))
        deleted = cur.fetchone()
        conn.commit()
        if deleted:
            return jsonify({"deleted": deleted})
        return jsonify({"error": "Warranty not found"}), 404
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()
