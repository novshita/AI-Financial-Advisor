import hashlib
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "finance.db"
PBKDF2_ITERATIONS = 260_000

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"


def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def _now():
    return datetime.now(timezone.utc).isoformat()


def _hash_password(password, salt, iterations=PBKDF2_ITERATIONS):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations).hex()


def init_db():
    with get_connection() as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                iterations INTEGER NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin','user')),
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                income REAL, expenses REAL, savings REAL, debt REAL,
                goal_name TEXT, goal_amount REAL, goal_months INTEGER, risk TEXT,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()

        admin_count = conn.execute(
            "SELECT COUNT(*) FROM users WHERE role='admin'"
        ).fetchone()[0]
        if admin_count == 0:
            create_user(DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD, "admin", conn=conn)


def create_user(username, password, role, conn=None):
    salt = secrets.token_hex(16).encode()
    password_hash = _hash_password(password, salt)
    owns_conn = conn is None
    conn = conn or get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password_hash, salt, iterations, role, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (username, password_hash, salt.hex(), PBKDF2_ITERATIONS, role, _now()),
        )
        conn.commit()
    finally:
        if owns_conn:
            conn.close()


def verify_user(username, password):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash, salt, iterations, role FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if row is None:
        return None
    salt = bytes.fromhex(row["salt"])
    expected = _hash_password(password, salt, row["iterations"])
    if not secrets.compare_digest(expected, row["password_hash"]):
        return None
    return {"id": row["id"], "username": row["username"], "role": row["role"]}


def set_password(user_id, new_password):
    salt = secrets.token_hex(16).encode()
    password_hash = _hash_password(new_password, salt)
    with get_connection() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ?, salt = ?, iterations = ? WHERE id = ?",
            (password_hash, salt.hex(), PBKDF2_ITERATIONS, user_id),
        )
        conn.commit()


def username_exists(username):
    with get_connection() as conn:
        row = conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
    return row is not None


def save_profile_snapshot(user_id, profile):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO profiles (user_id, income, expenses, savings, debt, goal_name, "
            "goal_amount, goal_months, risk, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                user_id, profile["income"], profile["expenses"], profile["savings"], profile["debt"],
                profile["goal_name"], profile["goal_amount"], profile["goal_months"], profile["risk"],
                _now(),
            ),
        )
        conn.commit()


def get_latest_profile(user_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM profiles WHERE user_id = ? AND id = "
            "(SELECT MAX(id) FROM profiles WHERE user_id = ?)",
            (user_id, user_id),
        ).fetchone()
    return dict(row) if row else None


def list_users_with_latest_snapshot():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT u.id, u.username, u.role, u.created_at,
                   p.income, p.expenses, p.savings, p.debt,
                   p.goal_name, p.goal_amount, p.goal_months, p.risk, p.created_at AS snapshot_at
            FROM users u
            LEFT JOIN profiles p ON p.id = (
                SELECT MAX(id) FROM profiles WHERE user_id = u.id
            )
            ORDER BY u.username
        """).fetchall()
    return [dict(row) for row in rows]
