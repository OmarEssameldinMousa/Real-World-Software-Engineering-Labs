import time
import json
from kafka import KafkaConsumer

# --- Configuration ---
KAFKA_BROKER = "kafka:9092"
USER_PROFILES_TOPIC = "user_profiles"
CLICK_EVENTS_TOPIC = "click_events"
CONSUMER_GROUP_ID = "join-enrichment-group"

# --- Helper Functions ---
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
                consumer_timeout_ms=10000,  # 10 second timeout
            )
            print(f"✅ Kafka consumer connected and subscribed to topic '{topic}'.")
            return consumer
        except Exception as e:
            print(f"🔥 Failed to connect consumer to Kafka: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def get_user_profile(user_id):
    """
    !!!!!!!!!!!!!! THE BOTTLENECK IS HERE !!!!!!!!!!!!!!
    For every click event, this function creates a NEW consumer
    to read the ENTIRE user_profiles topic from the beginning
    just to find one user. This is extremely inefficient.
    """
    print(f"🔍 Looking up profile for user_id {user_id} (this is inefficient on purpose)...")
    
    try:
        profile_consumer = KafkaConsumer(
            USER_PROFILES_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            auto_offset_reset="earliest",
            group_id=f"profile-lookup-{user_id}-{time.time()}",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            consumer_timeout_ms=5000,  # 5 second timeout
        )

        # Artificial delay to make the problem more obvious
        time.sleep(0.1)

        for message in profile_consumer:
            profile = message.value
            if profile.get("user_id") == user_id:
                profile_consumer.close()
                print(f"✅ Found profile for user_id {user_id}")
                return profile

        profile_consumer.close()
        print(f"❌ Profile not found for user_id {user_id}")
        return None
        
    except Exception as e:
        print(f"❌ Error looking up profile for user_id {user_id}: {e}")
        return None

# --- Main Logic ---
if __name__ == "__main__":
    print("🚀 Starting consumer with intentional bottleneck...")
    
    click_consumer = get_kafka_consumer(CLICK_EVENTS_TOPIC)

    print("\n--- Waiting for click events... ---")

    try:
        for message in click_consumer:
            click_event = message.value
            user_id = click_event.get("user_id")
            print(f"📨 Received click event for user_id {user_id}")

            if not user_id:
                print("⚠️  Click event missing user_id, skipping...")
                continue

            # Inefficiently fetch the user profile for each click
            user_profile = get_user_profile(user_id)

            if user_profile:
                enriched_event = {
                    "user_id": click_event["user_id"],
                    "url": click_event["url"],
                    "user_name": user_profile.get("name"),
                }
                print(f"🎉 Enriched Event: {enriched_event}")
            else:
                print(f"⚠️  Warning: Could not find profile for user_id {user_id}")
                
    except Exception as e:
        print(f"💥 Consumer crashed with error: {e}")
        print("Restarting in 5 seconds...")
        time.sleep(5)

