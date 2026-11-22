"""Animal shelter adoption register module.

This module provides functions to register pets in an SQLite database,
record adoptions, issue secure adoption codes, find the oldest available
pet, and clear unadopted pet records.
"""

import secrets
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    """CREATE TABLE pets (
        id INTEGER PRIMARY KEY,
        name TEXT,
        species TEXT,
        age INTEGER,
        adopted INTEGER
    )"""
)

shelter_stats = {"adoption_count": 0}


def register_pet(name, species, age, tags=None):
    """Register a new pet in the shelter database.

    Args:
        name: Pet's name.
        species: Pet's species.
        age: Pet's age in years.
        tags: Optional list of tags. Initialized to empty list if None.

    Returns:
        Updated list of tags.
    """
    if tags is None:
        tags = []
    conn.execute(
        "INSERT INTO pets (name, species, age, adopted) VALUES (?, ?, ?, 0)",
        (name, species, age),
    )
    tags.append(species)
    return tags


def adopt(pet_id):
    """Mark a pet as adopted by ID.

    Args:
        pet_id: Primary key ID of the pet.
    """
    conn.execute("UPDATE pets SET adopted = 1 WHERE id = ?", (pet_id,))
    shelter_stats["adoption_count"] += 1


def adoption_code():
    """Generate a secure adoption confirmation code.

    Returns:
        Formatted unique adoption code string.
    """
    code = secrets.randbelow(9000) + 1000
    return f"PET-{code}"


def oldest_available():
    """Find the name of the oldest pet currently available for adoption.

    Returns:
        Name of the oldest unadopted pet, or None if none found.
    """
    try:
        cursor = conn.execute(
            "SELECT name, age FROM pets WHERE adopted = 0 ORDER BY age DESC"
        )
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return None
    except sqlite3.Error as err:
        print(f"Database error querying oldest pet: {err}")
        return None


def clear_unadopted():
    """Remove all unadopted pet records from the database."""
    try:
        conn.execute("DELETE FROM pets WHERE adopted = 0")
    except sqlite3.Error as err:
        print(f"Database error clearing unadopted pets: {err}")


def shelter_status():
    """Return the activity status of the shelter.

    Returns:
        'active' if at least one pet has been adopted, otherwise 'quiet'.
    """
    if shelter_stats["adoption_count"] > 0:
        return "active"
    return "quiet"


def main():
    """Demonstrate shelter operations."""
    register_pet("Bruno", "dog", 7)
    register_pet("Mitzi", "cat", 3)
    register_pet("Kiwi", "parrot", 12)
    adopt(1)
    print(oldest_available(), adoption_code(), shelter_status())
    clear_unadopted()


if __name__ == "__main__":
    main()
