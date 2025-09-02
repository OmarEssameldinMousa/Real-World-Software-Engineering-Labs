
import time
import json
from kafka import KafkaConsumer

# --- Configuration ---
KAFKA_BROKER = "kafka:9092"
USER_PROFILES_TOPIC = "user_profiles"
CLICK_EVENTS_TOPIC = "click_events"
CONSUMER_GROUP_ID = "join-enrichment-group"

# --- Global cache for user profiles ---
user_profiles_cache = {}

def load_user_profiles():
    """Load all user profiles into memory once at startup"""
    print("📖 Loading user profiles into cache...")
    try:
        profile_consumer = KafkaConsumer(
            USER_PROFILES_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            auto_offset_reset="earliest",
            enable_auto_commit=False,
            consumer_timeout_ms=10000,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        
        for message in profile_consumer:
            profile = message.value
            user_id = profile.get("user_id")
            if user_id:
                user_profiles_cache[user_id] = profile
                print(f"  Cached profile for user_id {user_id}")
        
        profile_consumer.close()
        print(f"✅ Loaded {len(user_profiles_cache)} user profiles into cache")
        
    except Exception as e:
        print(f"❌ Failed to load user profiles: {e}")

def get_kafka_consumer(topic):
    """Creates and returns a Kafka consumer subscribed to a specific topic."""
    while True:
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=[KAFKA_BROKER],
                auto_offset_reset="earliest",
                group_id=CONSUMER_GROUP_ID,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            )
            print(f"✅ Kafka consumer connected and subscribed to topic '{topic}'.")
            return consumer
        except Exception as e:
            print(f"🔥 Failed to connect consumer to Kafka: {e}. Retrying in 5 seconds...")
            time.sleep(5)

# --- Main Logic ---
if __name__ == "__main__":
    # Pre-load user profiles into memory (THE FIX)
    load_user_profiles()
    
    click_consumer = get_kafka_consumer(CLICK_EVENTS_TOPIC)

    print("\n--- Waiting for click events... ---")

    processed_count = 0
    start_time = time.time()

    for message in click_consumer:
        click_event = message.value
        user_id = click_event.get("user_id")

        if not user_id:
            continue

        # Efficient lookup from memory cache (THE FIX)
        user_profile = user_profiles_cache.get(user_id)

        if user_profile:
            enriched_event = {
                "user_id": click_event["user_id"],
                "url": click_event["url"],
                "user_name": user_profile.get("name"),
            }
            print(f"Enriched Event: {enriched_event}")
        else:
            print(f"Warning: Could not find profile for user_id {user_id}")
        
        processed_count += 1
        if processed_count >= 1000:
            break

    elapsed = time.time() - start_time
    print(f"\n--- Processed {processed_count} events in {elapsed:.2f} seconds ---")
    click_consumer.close()