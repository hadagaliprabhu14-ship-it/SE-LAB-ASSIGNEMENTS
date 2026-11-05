"""Track purchase orders and warehouse receipts."""

import sqlite3


def initialize_database(connection):
    """Create the purchase order table if it does not already exist."""
    connection.execute(
        """CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            supplier TEXT NOT NULL,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            received INTEGER NOT NULL DEFAULT 0 CHECK (received IN (0, 1))
        )"""
    )


def place_order(connection, supplier, item, quantity):
    """Add an order and return the total quantity across all orders."""
    if not supplier.strip() or not item.strip():
        raise ValueError("Supplier and item must not be empty.")
    valid_integer = isinstance(quantity, int) and not isinstance(
        quantity, bool
    )
    if not valid_integer or quantity <= 0:
        raise ValueError("Quantity must be a positive integer.")

    connection.execute(
        "INSERT INTO orders (supplier, item, quantity) VALUES (?, ?, ?)",
        (supplier.strip(), item.strip(), quantity),
    )
    total = connection.execute("SELECT COALESCE(SUM(quantity), 0) FROM orders")
    return total.fetchone()[0]


def mark_received(connection, order_id):
    """Mark an existing order as received; return whether it was found."""
    cursor = connection.execute(
        "UPDATE orders SET received = 1 WHERE id = ?", (order_id,)
    )
    return cursor.rowcount == 1


def notify_warehouse(supplier):
    """Display a warehouse notification for a supplier."""
    print(f"Notifying warehouse about {supplier}.")


def cleanup(connection):
    """Delete orders that have been received."""
    cursor = connection.execute("DELETE FROM orders WHERE received = 1")
    return cursor.rowcount


def pending_count(connection):
    """Return the number of orders that have not been received."""
    result = connection.execute(
        "SELECT COUNT(*) FROM orders WHERE received = 0"
    )
    return result.fetchone()[0]


def main():
    """Run a short purchase order demonstration."""
    with sqlite3.connect(":memory:") as connection:
        initialize_database(connection)
        total_quantity = place_order(connection, "Acme Steel", "rods", 40)
        total_quantity = place_order(connection, "Bolt Co", "bolts", 500)
        mark_received(connection, 1)
        notify_warehouse("Acme Steel")
        print(f"Pending orders: {pending_count(connection)}")
        print(f"Total quantity ordered: {total_quantity}")
        cleanup(connection)


if __name__ == "__main__":
    main()
