import toml
from sqlalchemy import create_engine, text

try:
    secrets = toml.load('.streamlit/secrets.toml')
    config = secrets['database']
    db_url = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    engine = create_engine(db_url)
    
    with engine.connect() as conn:
        # Check if sales_summary table exists and has data
        try:
            result = conn.execute(text("SELECT count(*) FROM sales_summary"))
            count = result.scalar()
            print(f"✅ SUCCESS: sales_summary table has {count} rows.")
        except Exception as e:
            print(f"⚠️ Table check failed (might not exist): {e}")
            
except Exception as e:
    print(f"❌ Connection failed: {e}")
