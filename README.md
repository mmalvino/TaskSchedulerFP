# TaskSchedulerFP
## Micky Malvino Kusandiwinata(2602174522) & Shaan Kishore Gunwani(2602176982)

This project is a Distributed Task Scheduler designed to distribute computational tasks across nodes. It demonstrates fault tolerance, scalability, and resource optimization. The application uses Celery to process the tasks, RabbitMQ as the message broker, Redis for persistent data storage, and Flask as the web server. The program is deployed in a distributed system environment using AWS EC2.

## Key Features


**Task Submission and Management 📋:**

* Tasks can be submitted with unique IDs, priorities, and task_data.

* Tasks are processed asynchronously with acknowledgment to prevent message loss. ```acks_late=True```

* The system supports priority-based task scheduling. Tasks with higher priority values are processed before lower-priority ones when queued in the same Celery worker.

* Submitted tasks are tracked in Redis, where the task_ids are stored.




**Fault Tolerance 💪🏼:**

Tested scenarios include:

* Celery Worker Down: When a Celery worker is down, tasks wait until the worker is reactivated, then processing resumes. In a multi-worker setup, if one worker fails, the task is rerouted to another worker for completion.

* Flask Server Killed: After requests are submitted, killing the Flask server does not disturb the ongoing task processing.

* RabbitMQ Down: If RabbitMQ goes down while tasks are being processed, the Celery worker pauses. Once RabbitMQ is back up, processing continues seamlessly.




**Visualization & Monitoring 👀:**

* Task status (PENDING, STARTED, SUCCESS, FAILURE) can displayed via a dashboard using tools like Flower.

* Rabbitmq management UI can be used to have an in-depth look at queues in detail and whether they are running.

* A dynamic dashboard (HTML with Chart.js) can provide a bar chart visualization of task statuses.



**Scalability 📈:**

* Celery allow seamless scaling by adding more worker nodes

* You can also increase concurrency value in Celery to add more child processes to the nodes.

* The system can distribute the tasks across multiple nodes (celery workers) to balance the load.

* Furthermore, AWS EC2 allows for more scaling vertically and horizontally.


## Technology Involved 

* Flask: Web framework for the API server.

* Celery: Task queue to process distributed tasks.

* RabbitMQ: Message broker for task communication.

* Redis: Backend for storing task results and tracking task IDs.

* Postman: Used to send API requests and test the system with predefined JSON files containing tasks.

* Chart.js: Used in the dashboard for task status visualization.

* AWS EC2: Deployment platform for distributed system demonstration.


## System Architecture

<img width="609" alt="Screenshot 2024-12-18 at 02 46 35" src="https://github.com/user-attachments/assets/c588376b-d6a5-4c8f-b78e-6ae0b3b5067f" />


## Deployment on AWS EC2

The application has been deployed on AWS EC2 to demonstrate functionality in a distributed system.

### Steps for Deployment:

Setup AWS EC2:

* Create and configure an EC2 instance (Ubuntu).

* Open necessary ports (e.g., 5000 for Flask, 5672 for RabbitMQ, 6379 for Redis).

Install Dependencies:

* Install requirements.txt.

* Install RabbitMQ and Redis server.

Run RabbitMQ and Redis:

* Start RabbitMQ broker and Redis server on the EC2 instance.

Start Flask Server:

``` python3 main.py ```

Run Celery Workers:

```celery -A celery_app worker --loglevel=info -Q default --concurrency=1 -n worker1@%h ```

This is to activate one celery worker, for a second one you can do:

```celery -A celery_app worker --loglevel=info -Q default --concurrency=1 -n worker2@%h```

Increase the value of concurrency to add more child processes to the specific worker as you wish.

Send your task request from postman or any alternative.

<img width="852" alt="Screenshot 2024-12-18 at 03 18 59" src="https://github.com/user-attachments/assets/1f14c7c0-0411-48e2-bf02-1aefc0da4814" />

***

Access Dashboard and get the results:

Open ``` http://<EC2-Public-IP>:5000/status/all ``` in your browser. For us, it is "http://52.206.96.121:5000/status/all" as seen in the image below.

<img width="803" alt="Screenshot 2024-12-18 at 05 38 25" src="https://github.com/user-attachments/assets/30efb9bb-f5fd-4878-b132-7c2deff02e96" />

***

Go to "http://52.206.96.121:5000/" for the task status dashboard as seen in the image below.

<img width="1727" alt="Screenshot 2024-12-18 at 05 45 13" src="https://github.com/user-attachments/assets/2b9d19fc-05f2-46ff-bf47-c3c946d779ad" />

***

Go to "http://52.206.96.121:5555/" to access the flower monitoring tool to access worker status, whether they are active, processing, fail, etc.

<img width="1726" alt="Screenshot 2024-12-18 at 05 44 53" src="https://github.com/user-attachments/assets/27cd1ea7-b0b0-48c3-a32b-d35e8be199fb" />

***

Go to "http://52.206.96.121:15672/#/queues" to access rabbitmq's management UI tool where you can see the overview of processes or check individual queues.

<img width="1712" alt="Screenshot 2024-12-18 at 05 44 37" src="https://github.com/user-attachments/assets/c2d7de59-a608-401b-9487-69e5b9ba5be2" />




