from backend.database import get_connection


connection = get_connection()
cursor = connection.cursor()

query = """
SELECT
    p1.name AS product_a,
    p2.name AS product_b,
    COUNT(DISTINCT o1.customer_id) AS customers
FROM orders o1
JOIN orders o2
    ON o1.customer_id = o2.customer_id
    AND o1.product_id < o2.product_id
JOIN products p1
    ON p1.id = o1.product_id
JOIN products p2
    ON p2.id = o2.product_id
WHERE
    o1.status = 'paid'
    AND o2.status = 'paid'
GROUP BY
    o1.product_id,
    o2.product_id
ORDER BY
    customers DESC
LIMIT 10
"""

rows = cursor.execute(query).fetchall()

print("\n🔎 Top Product Combinations\n")

for row in rows:
    print(dict(row))

connection.close()