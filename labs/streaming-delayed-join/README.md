
# Lab: Streaming Delayed Join

## 🎯 Objective

Your goal is to fix a slow streaming pipeline. A Python consumer service is reading from two Kafka topics, performing a join, and writing to a log. This join operation is incredibly inefficient, causing the consumer to lag by over an hour on a typical day's worth of data.

**Your task:** Refactor the consumer code to process the stream of 1,000 click events in **under 15 seconds** while producing the correct, enriched output.

---

## 🔧 The Environment

This lab consists of a Docker Compose environment with four services:
*   `zookeeper`: A dependency for Kafka.
*   `kafka`: The message broker.
*   `producer`: A Python service that generates mock data for two topics:
    *   `user_profiles`: A small set of user metadata (ID, name, city). Sent once at the start.
    *   `click_events`: A stream of 1,000 click events (timestamp, user_id, url).
*   `consumer`: **This is the service you need to fix.** It reads from both topics, joins the data to enrich click events with user names, and prints the result.

### The Bottleneck

The problem lies in `app/consumer.py`. Currently, for every single click event, the consumer re-reads the *entire* `user_profiles` topic from the beginning to find the matching user. This is a classic N+1 problem in a streaming context and is extremely inefficient.

---

## ▶️ How to Run the Lab

1.  **Start the pipeline:**
    From this directory (`labs/streaming-delayed-join`), run the start script. This will build the Docker image and start all services. The producer will automatically generate the data.

    ```bash
    ./scripts/run.sh
    ```

2.  **Observe the (slow) output:**
    You will see the consumer's output in your terminal. Notice the significant delay between each processed message. You can stop the process at any time with `Ctrl+C`.

    ```
    # Expected (slow) output
    Enriched Event: {'user_id': 103, 'url': '/products/widget-a', 'user_name': 'Charlie'}
    Enriched Event: {'user_id': 101, 'url': '/home', 'user_name': 'Alice'}
    ... (very slowly) ...
    ```

---

## 📝 Your Task

1.  **Locate the Problem:** Open `app/consumer.py` and analyze the `for message in consumer:` loop. Identify why it's so slow.

2.  **Refactor the Code:** Modify `app/consumer.py` to perform the join efficiently.
    *   **Hint:** Since the user profile data is small and rarely changes, can you load it into the consumer's memory once at the start?

3.  **Validate Your Solution:** Once you have modified the code, you can test it using the local solution validator. This script will run the pipeline, time the consumer's execution, and verify the output is correct.

    ```bash
    # Run this from the labs/streaming-delayed-join/ directory
    ./scripts/solution-validator.sh
    ```

    A successful run will look like this:
    ```
    --- Running Solution Validator ---
    ... (docker-compose output) ...
    --- Consumer finished processing in 3.80 seconds ---
    ✅ SUCCESS: Consumer finished under the 15-second target.
    ✅ SUCCESS: Correct number of records processed (1000/1000).
    --- 🎉 VALIDATION PASSED! ---
    ```

---

## 🏆 Submitting Your Solution

Once you have a working solution and have verified it with `solution-validator.sh`, you can add it to the community solutions list. Our CI process is automated, so please follow these steps carefully:

1.  **Create a public write-up** of your solution. This can be a blog post, a GitHub Gist, or a link to your forked repository.

2.  **Add your solution to the central JSON file.** Edit the `solutions/solutions.json` file at the root of the repository and add a new JSON object to the list.

3.  **Use the correct format.** Your entry must match this structure exactly:

    ```json
    {
      "github_username": "your-github-username",
      "lab_slug": "streaming-delayed-join",
      "solution_link": "https://link-to-your-writeup"
    }
    ```
    *(Remember to add a comma to the preceding entry if you are not the first one!)*

4.  **Open a Pull Request** that modifies **only** the `solutions.json` file. The CI will validate your entry, regenerate the documentation, and update the solver count.

For more detailed instructions, please see the main [**CONTRIBUTING.md**](../../CONTRIBUTING.md) guide.