import time
import json
from kafka import KafkaProducer

# --- Configuration ---
KAFKA_BROKER = 'kafka:9092'
USER_PROFILES_TOPIC = 'user_profiles'
CLICK_EVENTS_TOPIC = 'click_events'
RETRY_TIMEOUT_MS = 5000  # 5 seconds
TOTAL_CLICKS = 1000

# --- Mock Data ---
USERS = [
    {"user_id": 101, "name": "Alice", "city": "New York"},
    {"user_id": 102, "name": "Bob", "city": "London"},
    {"user_id": 103, "name": "Charlie", "city": "Paris"},
    {"user_id": 104, "name": "David", "city": "Tokyo"},
]

CLICK_URLS = ['/home', '/products/widget-a', '/cart', '/checkout', '/about-us']

# --- Helper Functions ---
def get_kafka_producer():
    """Tries to connect to Kafka and returns a producer instance."""
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BROKER],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("✅ Kafka producer connected successfully.")
            return producer
        except Exception as e:
            print(f"🔥 Failed to connect to Kafka: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# --- Main Logic ---
if __name__ == "__main__":
    print("🚀 Starting producer...")
    producer = get_kafka_producer()

    # 1. Send all user profiles to the 'user_profiles' topic
    print(f"--- Sending {len(USERS)} user profiles to topic '{USER_PROFILES_TOPIC}' ---")
    for user in USERS:
        producer.send(USER_PROFILES_TOPIC, key=str(user["user_id"]).encode('utf-8'), value=user)
        print(f"📤 Sent user profile: {user['name']} (ID: {user['user_id']})")
    
    # Ensure all profile messages are sent before clicks
    producer.flush()
    print("--- User profiles sent. ---")
    
    time.sleep(2) # Brief pause

    # 2. Send a stream of click events
    print(f"--- Sending {TOTAL_CLICKS} click events to topic '{CLICK_EVENTS_TOPIC}' ---")
    for i in range(TOTAL_CLICKS):
        user = USERS[i % len(USERS)] # Cycle through users
        event = {"user_id": user["user_id"], "url": CLICK_URLS[i % len(CLICK_URLS)]}
        producer.send(CLICK_EVENTS_TOPIC, value=event)
        
        if (i + 1) % 100 == 0:
            print(f"  ... {i+1}/{TOTAL_CLICKS} clicks sent")

    # Flush messages to ensure they are all sent
    producer.flush()
    print("--- All click events sent. Producer finished. ---")

    producer.close()