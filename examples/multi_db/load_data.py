from sqlalchemy import create_engine
from faker import Faker
from sqlalchemy import text
import random
from datetime import datetime, timedelta

fake = Faker()

def gen_mysql():
    engine = create_engine('mysql+pymysql://root:root@localhost/mysql-data-ai-test')

    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS `Order`"))
        conn.execute(text("DROP TABLE IF EXISTS Product"))
        conn.execute(text("DROP TABLE IF EXISTS Store"))
        conn.execute(text("DROP TABLE IF EXISTS User"))

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS User (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                full_name VARCHAR(100),
                address TEXT,
                age INT,
                dob DATE
            )
            """))
        conn.commit()

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS Store (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                address TEXT
            )
            """))
        conn.commit()

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS Product (
                id INT AUTO_INCREMENT PRIMARY KEY,
                store_id INT,
                name VARCHAR(100),
                address TEXT,
                FOREIGN KEY (store_id) REFERENCES Store(id)
            )
            """))
        conn.commit()

    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS `Order` (
                id INT AUTO_INCREMENT PRIMARY KEY,
                store_id INT,
                product_id INT,
                user_id INT,
                name VARCHAR(100),
                address TEXT,
                FOREIGN KEY (store_id) REFERENCES Store(id),
                FOREIGN KEY (product_id) REFERENCES Product(id),
                FOREIGN KEY (user_id) REFERENCES User(id)
            )
            """))
        conn.commit()


    with engine.connect() as conn:
        # Insert sample users
        user_ids = []
        for _ in range(10):
            name = fake.first_name()
            full_name = fake.name()
            address = fake.address()
            age = random.randint(18, 70)
            dob = fake.date_of_birth(minimum_age=age, maximum_age=age)
            result = conn.execute(
                text("INSERT INTO User (name, full_name, address, age, dob) VALUES (:name, :full_name, :address, :age, :dob)"),
                {"name": name, "full_name": full_name, "address": address, "age": age, "dob": dob}
            )
            conn.commit()
            user_ids.append(result.lastrowid)

        # Insert sample stores
        store_ids = []
        for _ in range(5):
            name = fake.company()
            address = fake.address()
            result = conn.execute(
                text("INSERT INTO Store (name, address) VALUES (:name, :address)"),
                {"name": name, "address": address}
            )
            conn.commit()
            store_ids.append(result.lastrowid)

        # Insert sample products
        product_ids = []
        for _ in range(20):
            store_id = random.choice(store_ids)
            name = fake.word()
            address = fake.address()
            result = conn.execute(
                text("INSERT INTO Product (store_id, name, address) VALUES (:store_id, :name, :address)"),
                {"store_id": store_id, "name": name, "address": address}
            )
            conn.commit()
            product_ids.append(result.lastrowid)

        # Insert sample orders
        for _ in range(30):
            store_id = random.choice(store_ids)
            product_id = random.choice(product_ids)
            user_id = random.choice(user_ids)
            name = fake.bs()
            address = fake.address()
            conn.execute(
                text("INSERT INTO `Order` (store_id, product_id, user_id, name, address) VALUES (:store_id, :product_id, :user_id, :name, :address)"),
                {"store_id": store_id, "product_id": product_id, "user_id": user_id, "name": name, "address": address}
            )
            conn.commit()

    print("Data generated and inserted into MySQL successfully.")

def gen_pg():
    engine = create_engine("postgresql://postgres:root@localhost/pg-data-ai-test")
    conn = engine.connect()

    # Create tables
    conn.execute(text("DROP TABLE IF EXISTS Transaction CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS PaymentMethod CASCADE"))

    conn.execute(text("""
    CREATE TABLE PaymentMethod (
        id SERIAL PRIMARY KEY,
        method_name VARCHAR(50) NOT NULL,
        description TEXT
    )
    """))

    conn.execute(text("""
    CREATE TABLE Transaction (
        id SERIAL PRIMARY KEY,
        order_id INT NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        payment_method_id INT REFERENCES PaymentMethod(id),
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """))

    conn.execute(text("COMMENT ON TABLE PaymentMethod IS 'Table storing payment method details'"))
    conn.execute(text("COMMENT ON TABLE Transaction IS 'Table storing transaction records'"))

    # Comment for PaymentMethod
    conn.execute(text("COMMENT ON TABLE PaymentMethod IS 'Table storing payment method details'"))
    conn.execute(text("COMMENT ON COLUMN PaymentMethod.id IS 'Primary key for payment methods'"))
    conn.execute(text("COMMENT ON COLUMN PaymentMethod.method_name IS 'Name of the payment method'"))
    conn.execute(text("COMMENT ON COLUMN PaymentMethod.description IS 'Description of the payment method'"))

    # Comment for Transaction
    conn.execute(text("COMMENT ON TABLE Transaction IS 'Table storing transaction records'"))
    conn.execute(text("COMMENT ON COLUMN Transaction.id IS 'Primary key for transactions'"))
    conn.execute(text("COMMENT ON COLUMN Transaction.order_id IS 'Associated order ID'"))
    conn.execute(text("COMMENT ON COLUMN Transaction.amount IS 'Transaction amount'"))
    conn.execute(text("COMMENT ON COLUMN Transaction.payment_method_id IS 'Foreign key to payment method'"))
    conn.execute(text("COMMENT ON COLUMN Transaction.transaction_date IS 'Date and time of the transaction'"))

    # Seed payment methods
    payment_methods = [
        {'method_name': 'Credit Card', 'description': 'Visa, MasterCard, etc.'},
        {'method_name': 'Bank Transfer', 'description': 'Direct bank to bank transfer'},
        {'method_name': 'E-Wallet', 'description': 'Momo, ZaloPay, etc.'}
    ]

    conn.execute(
        text("INSERT INTO PaymentMethod (method_name, description) VALUES (:method_name, :description)"),
        payment_methods
    )

    # Generate sample transactions using order_ids 1 to 10
    for order_id in range(1, 11):
        amount = round(random.uniform(10, 1000), 2)
        payment_method_id = random.randint(1, 3)
        days_ago = random.randint(0, 30)
        transaction_date = datetime.now() - timedelta(days=days_ago)

        conn.execute(
            text("""
                INSERT INTO Transaction (order_id, amount, payment_method_id, transaction_date)
                VALUES (:order_id, :amount, :payment_method_id, :transaction_date)
            """),
            {'order_id': order_id, 'amount': amount, 'payment_method_id': payment_method_id, 'transaction_date': transaction_date}
        )

    conn.commit()
    conn.close()
    print("PostgreSQL transaction data generated successfully.")

def gen_clickhouse():
    fake = Faker()
    try:
        # Sử dụng cổng mặc định 9000 cho clickhouse-native
        uri = 'clickhouse+native://root:root@localhost:19000/ch-data-ai-test'
        engine = create_engine(url=uri)
        
        with engine.connect() as conn:
            # Tạo database
            conn.execute(text("CREATE DATABASE IF NOT EXISTS `ch-data-ai-test`"))
            
            # Xóa table nếu tồn tại
            conn.execute(text("DROP TABLE IF EXISTS `ch-data-ai-test`.events"))
            
            # Tạo table
            conn.execute(text("""
                CREATE TABLE `ch-data-ai-test`.events (
                    id UInt64,
                    user_id UInt64,
                    event_name String,
                    meta_data String,
                    created_at DateTime
                ) ENGINE = MergeTree()
                ORDER BY id
            """))

            # Tạo dữ liệu giả
            rows = []
            for i in range(1, 101):
                rows.append({
                    "id": i,
                    "user_id": fake.random_int(min=1, max=100),
                    "event_name": fake.word(),
                    "meta_data": fake.json(data_columns={"key": "word"}, num_rows=1),
                    "created_at": fake.date_time_between(start_date='-30d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
                })

            values = ", ".join(
                f"({row['id']}, {row['user_id']}, '{row['event_name']}', '{row['meta_data'].replace('\'', '\\\'')}', '{row['created_at']}')"
                for row in rows
            )
            insert_stmt = text(
                f"INSERT INTO `ch-data-ai-test`.events (id, user_id, event_name, meta_data, created_at) VALUES {values}"
            )
            
            conn.execute(insert_stmt)
            
            # Commit transaction
            conn.commit()
            
        print("ClickHouse event data generated successfully.")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise
    finally:
        engine.dispose()
# gen_mysql()
# gen_pg()
gen_clickhouse()
