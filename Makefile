# --- Configuration ---
URL:=game_server_url
USERNAME:=username
PASSWORD:=username
SERVER=http://127.0.0.1:8000

include .env

run:
	uvicorn server:app --host 0.0.0.0 --port 8000

build:
	podman build -t travian-bot .

start:
	podman run -p 8000:8000 travian-bot


start-server:
	sudo podman run -d \
		--name travian-bot \
		--net=host \
		-v $(shell pwd)/data:/app/data \
		travian-bot

# --- Commands ---
login:
	curl -X POST "$(SERVER)/login" \
		-H "Content-Type: application/json" \
		-d '{"url": "$(URL)", "username": "$(USERNAME)", "password": "$(PASSWORD)"}'

update:
	curl -X POST "$(SERVER)/update" \
		-H "Content-Type: application/json"

get_villages:
	curl -X GET "$(SERVER)/villages" \
		-H "Content-Type: application/json"

get_constructions_by_village:
	curl -X GET "${SERVER}/villages/39780/constructions" \
		-H "Content-Type: application/json"

# --- Add resource build tasks ---
wood_task:
	curl -X POST "$(SERVER)/villages/tasks" \
		-H "Content-Type: application/json" \
		-d '{"village_id": "39780", "resource_type": "wood", "target_level": 5}'

clay_task:
	curl -X POST "$(SERVER)/villages/tasks" \
		-H "Content-Type: application/json" \
		-d '{"village_id": "39780", "resource_type": "clay", "target_level": 5}'

iron_task:
	curl -X POST "$(SERVER)/villages/tasks" \
		-H "Content-Type: application/json" \
		-d '{"village_id": "39780", "resource_type": "iron", "target_level": 5}'

crop_task:
	curl -X POST "$(SERVER)/villages/tasks" \
		-H "Content-Type: application/json" \
		-d '{"village_id": "39780", "resource_type": "crop", "target_level": 5}'

# Optional: run all at once
all_tasks: wood_task clay_task iron_task crop_task

send_farmlist:
	# Pass FARM_LIST as a space-separated list of indexes, e.g.
	# make send_farmlist FARM_LIST="0 1 2"
	curl -X POST "$(SERVER)/send_farmlist" \
		-H "Content-Type: application/json" \
		-d '{"list": [$(FARM_LIST)]}'
