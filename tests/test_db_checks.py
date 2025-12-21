import pytest


@pytest.mark.parametrize("username,email", [("ali", "ali@example.com")])
def test_user_exists(db, username, email):
    """Assert that a given user exists in the 'users' table."""
    assert db is not None, "Database not initialized. Check config/config.yaml env->db settings."

    rows = db.execute_query(
        "SELECT 1 FROM users WHERE username = :username AND email = :email LIMIT 1",
        {"username": username, "email": email},
    )
    print(f"[DB] Checking existence -> users(username='{username}', email='{email}'), rows_returned={len(rows)}")

    assert len(rows) == 1, f"Expected user '{username}' with email '{email}' to exist"


@pytest.mark.smoke
def test_users_table_has_rows(db):
    """Basic sanity: ensure 'users' table is not empty."""
    count = db.execute_scalar("SELECT COUNT(*) FROM users")
    print(f"[DB] users table row count -> {count}")
    assert count is not None and count > 0, "Expected at least one row in users table"


