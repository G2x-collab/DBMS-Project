from flask import jsonify
from flask.cli import load_dotenv
import psycopg2
import os

load_dotenv()

DB_URL = os.getenv("DB_URL")

def get_connection():
    """Create a new database connection."""
    return psycopg2.connect(DB_URL)

def get_virus_by_id(virus_id):
    """Fetch a virus by its ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Virus WHERE virus_id = %s", (virus_id,))
    virus = cur.fetchone()
    cur.close()
    conn.close()
    return virus

def update_virus(virus_id, name, category, discovery_date, attack_vector, spread_rate, infection_method, damage_potential):
    """Update an existing virus entry."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE Virus 
        SET name = %s, category = %s, discovery_date = %s, attack_vector = %s, 
            spread_rate = %s, infection_method = %s, damage_potential = %s
        WHERE virus_id = %s
    """, (name, category, discovery_date, attack_vector, spread_rate, infection_method, damage_potential, virus_id))
    conn.commit()
    cur.close()
    conn.close()

import psycopg2

def add_virus(name, category, discovery_date, attack_vector, spread_rate, infection_method, damage_potential):
    conn = get_connection()
    cur = conn.cursor()
    
    # Fetch the latest virus_id
    cur.execute("SELECT COALESCE(MAX(virus_id), 0) + 1 FROM virus")
    new_id = cur.fetchone()[0]  # Get the next available ID
    
    try:
        # Try inserting a new virus entry
        cur.execute("""
            INSERT INTO virus (virus_id, name, category, discovery_date, attack_vector, spread_rate, infection_method, damage_potential) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (virus_id) DO UPDATE SET
                name = EXCLUDED.name,
                category = EXCLUDED.category,
                discovery_date = EXCLUDED.discovery_date,
                attack_vector = EXCLUDED.attack_vector,
                spread_rate = EXCLUDED.spread_rate,
                infection_method = EXCLUDED.infection_method,
                damage_potential = EXCLUDED.damage_potential
        """, (new_id, name, category, discovery_date, attack_vector, spread_rate, infection_method, damage_potential))
    
        conn.commit()
    except psycopg2.Error as e:
        print("Database Error:", e)
        conn.rollback()
    
    cur.close()
    conn.close()


def delete_virus(virus_id):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM virus WHERE virus_id = %s", (virus_id,))  # Use %s instead of ?
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": "Virus deleted successfully"})


