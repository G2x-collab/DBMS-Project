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

def add_or_update_os(name, version, architecture, vulnerability_score):
    conn = get_connection()
    cur = conn.cursor()
    
    # Fetch the latest os_id
    cur.execute("SELECT COALESCE(MAX(os_id), 0) + 1 FROM operating_system")
    new_id = cur.fetchone()[0]  # Get the next available ID
    
    try:
        # Try inserting a new OS entry
        cur.execute("""
            INSERT INTO operating_system (os_id, name, version, architecture, vulnerability_score) 
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (os_id) DO UPDATE SET
                name = EXCLUDED.name,
                version = EXCLUDED.version,
                architecture = EXCLUDED.architecture,
                vulnerability_score = EXCLUDED.vulnerability_score
        """, (new_id, name, version, architecture, vulnerability_score))
    
        conn.commit()
    except psycopg2.Error as e:
        print("Database Error:", e)
        conn.rollback()
    finally:
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

def get_os_by_id(os_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM operating_system WHERE os_id = %s", (os_id,))
    os_entry = cur.fetchone()

    cur.close()
    conn.close()
    
    return os_entry


def update_os(os_id, name, version, architecture, vulnerability_score):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE operating_system 
            SET name = %s, version = %s, architecture = %s, vulnerability_score = %s 
            WHERE os_id = %s
        """, (name, version, architecture, vulnerability_score, os_id))

        conn.commit()
    except psycopg2.Error as e:
        print("Database Error:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def add_os(name, version, architecture, vulnerability_score):
    conn = get_connection()
    cur = conn.cursor()
    
    # Fetch the latest os_id
    cur.execute("SELECT COALESCE(MAX(os_id), 0) + 1 FROM operating_system")
    new_id = cur.fetchone()[0]  # Get the next available ID
    
    try:
        # Insert new OS entry
        cur.execute("""
            INSERT INTO operating_system (os_id, name, version, architecture, vulnerability_score) 
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (os_id) DO UPDATE SET
                name = EXCLUDED.name,
                version = EXCLUDED.version,
                architecture = EXCLUDED.architecture,
                vulnerability_score = EXCLUDED.vulnerability_score
        """, (new_id, name, version, architecture, vulnerability_score))
    
        conn.commit()
    except:
        print("Database Error:")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


