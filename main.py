from flask import Flask, request, jsonify, render_template
from celery.result import AsyncResult
from celery_app import celery_app, process_task
from kombu.exceptions import OperationalError
from datetime import datetime
import time
import redis

app = Flask(__name__)

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=1, decode_responses=True)

# Function to retry task submission with exponential backoff
def retry_submit_task(task_func, *args, retries=5, delay=2, **kwargs):
    for attempt in range(retries):
        try:
            return task_func.apply_async(args=args, **kwargs)
        except OperationalError as e:
            print(f"Attempt {attempt + 1}: Failed to send task to RabbitMQ. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("Failed to submit task after multiple retries.")

@app.route('/')
def dashboard():
    """
    Serve the task visualization dashboard.
    as in the 'dashboard.html' inside templates folder.
    """
    return render_template('dashboard.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    """
    Endpoint to add a new task to the Celery queue.
    Expects JSON data containing 'task_id', 'task_data', and 'priority'.
    Stores the task ID in Redis for tracking.
    """
    data = request.get_json()
    print("Received Data:", data)

    try:
        task_id = data.get("task_id")
        task_data = data.get("task_data", "default task")
        priority = int(data.get("priority", 5))
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Submitting task {task_id} with priority {priority} at {timestamp}")

        # Submit the task with retries in case RabbitMQ is down
        task = retry_submit_task(
            process_task,
            task_id, task_data, priority, timestamp,
            queue='default',
            priority=priority
        )

        # Store task ID in Redis
        redis_client.rpush("task_ids", task.id)
        
        return jsonify({"task_id": task.id, "status": "Task added to Celery queue"})

    except (ValueError, TypeError, KeyError) as e:
        print("Error:", e)
        return jsonify({"error": "Invalid input data. Ensure 'priority' is an integer."}), 400
    except Exception as e:
        print("Error during task submission:", e)
        return jsonify({"error": "Task submission failed. Please try again later."}), 503

@app.route('/status/all', methods=['GET'])
def get_all_task_status():
    """
    Retrieve results and statuses of all tasks in the list.
    """
    task_ids = redis_client.lrange("task_ids", 0, -1)  # Retrieve all task IDs from Redis
    results = []
    for task_id in task_ids:
        result = AsyncResult(task_id, app=celery_app)
        results.append({
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None
        })
    
    return jsonify({"tasks": results})

@app.route('/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """
    Retrieve status and result for a specific task ID.
    """
    result = AsyncResult(task_id, app=celery_app)
    return jsonify({
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False) # Run Flask server on all interfaces, port 5000
