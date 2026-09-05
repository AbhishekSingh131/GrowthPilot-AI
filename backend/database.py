import sqlite3

DATABASE_NAME = "growthpilot.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Customers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    # Products
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # Orders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # Agent Actions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT NOT NULL,
            product_a TEXT,
            product_b TEXT,
            reason TEXT NOT NULL,
            confidence REAL,
            estimated_revenue REAL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # AI Growth Campaigns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_type TEXT NOT NULL,
            name TEXT NOT NULL,
            product_a TEXT,
            product_b TEXT,
            offer TEXT,
            target_customers INTEGER NOT NULL,
            status TEXT NOT NULL,
            expected_revenue REAL,
            created_at TEXT NOT NULL
        )
    """)

    # Campaign Measurement Results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaign_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL,
            targeted_customers INTEGER NOT NULL,
            exposed_customers INTEGER NOT NULL,
            conversions INTEGER NOT NULL,
            campaign_revenue REAL NOT NULL,
            baseline_conversion_rate REAL NOT NULL,
            campaign_conversion_rate REAL NOT NULL,
            incremental_conversions REAL NOT NULL,
            incremental_revenue REAL NOT NULL,
            campaign_cost REAL NOT NULL DEFAULT 0,
            roi REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )
    """)

    connection.commit()
    connection.close()