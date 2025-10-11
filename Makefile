include .env
export
TRAVIAN_BOT_SRC:=$(PWD)/travian-bot-server
NETWORK:=cloudflare-network
TRAVIAN_BOT_IMAGE:=travian-bot
PROXY_CONTAINER:=traefik-reverse-proxy
CLOUDFLARE_CONTAINER:=cloudflared
TUNNEL_ID:=4a9c4354-6306-4fde-ab44-89802d3fc24c
DOMAIN:=www.959353d1958446d49b91832e0d8e21fa.online
TUNNEL_NAME:=traefik-tunnel

.PHONY: run run-traefik run-cloudflare run-travian-bot stop start restart kill rebuild

# --- RUN ALL ---
run: run-cloudflare run-traefik run-travian-bot

setup-cloudflare:
	-cloudflared tunnel create $(TUNNEL_NAME)
	-cloudflared tunnel route dns $(TUNNEL_NAME) $(DOMAIN) 

# Traefik reverse proxy
stop-traefik:
	docker kill $(PROXY_CONTAINER)

rm-traefik: stop-traefik
	docker rm $(PROXY_CONTAINER)

restart-traefik: rm-traefik rm-auth-service run-traefik

run-traefik: run-auth-service
	docker run -d \
		--name $(PROXY_CONTAINER) \
		-p 80:80 \
		-p 8080:8080 \
		--network $(NETWORK) \
		-v $(PWD)/traefik-reverse-proxy/traefik.yml:/etc/traefik/traefik.yml:Z \
		-v $(PWD)/traefik-reverse-proxy/dynamic.yml:/etc/traefik/dynamic.yml:Z \
		-v $(PWD)/traefik-reverse-proxy/traefikauth:/plugins-local/src/github.com/mmarci96/traefikauth \
		-v /var/run/docker.sock:/var/run/docker.sock \
		traefik:v3.5 \
		--entrypoints.web.address=:80 \
		--api.dashboard=true \
		--providers.docker=true \
		--providers.docker.exposedbydefault=false

stop-auth-service:
	docker kill auth-service

rm-auth-service: stop-auth-service
	docker rm auth-service

restart-auth-service: rm-auth-service run-auth-service

run-auth-service:
	docker run -d \
	  --name auth-service \
	  --network $(NETWORK) \
	  -p 8081:8000 \
	  -l 'traefik.enable=true' \
	  -l 'traefik.http.routers.authservice.rule=Host(`www.959353d1958446d49b91832e0d8e21fa.online`) && PathPrefix(`/login`) || PathPrefix(`/verify`) || PathPrefix(`/success`)' \
	  -l 'traefik.http.routers.authservice.entrypoints=web' \
	  -l 'traefik.http.services.authservice.loadbalancer.server.port=8000' \
	  -v $(PWD)/traefik-reverse-proxy/auth-service:/app \
	  -w /app \
	  python:3.11-slim \
	  sh -c "pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port 8000"


rm-cloudflare:
	docker rm -f cloudflared

restart-cloudflare: rm-cloudflare run-cloudflare

# Cloudflare Tunnel
run-cloudflare:
	docker run -d \
		--name cloudflared \
		--network cloudflare-network \
		--user root \
		--label traefik.enable=false \
		-v /home/notme/.cloudflared:/etc/cloudflared:Z \
		cloudflare/cloudflared:latest \
		tunnel --no-autoupdate \
		--config /etc/cloudflared/config.yaml \
		--url http://$(PROXY_CONTAINER):80/ \
		--credentials-file /etc/cloudflared/$(TUNNEL_ID).json \
		run $(TUNNEL_NAME)

rm-travian-bot:
	docker rm -f travian-bot

restart-travian-bot: rm-travian-bot run-travian-bot
	
# Travian bot app
run-travian-bot:
	docker run -d \
		--name travian-bot \
		--network $(NETWORK) \
		-p 8000:8000 \
		-l 'traefik.enable=true' \
		-l 'traefik.http.routers.travianbot.rule=PathPrefix(`/api`)' \
		-l 'traefik.http.routers.travianbot.entrypoints=web' \
		-l 'traefik.http.services.travianbot.loadbalancer.server.port=8000' \
		$(TRAVIAN_BOT_IMAGE)

# --- STOP ALL ---
stop:
	docker stop $(PROXY_CONTAINER) $(CLOUDFLARE_CONTAINER) $(APP_CONTAINERS) || true

# --- START ALL ---
start:
	docker start $(PROXY_CONTAINER) $(CLOUDFLARE_CONTAINER) $(APP_CONTAINERS) || true

# --- RESTART ALL ---
restart: stop start

# --- KILL / REMOVE ALL ---
kill:
	docker rm -f $(PROXY_CONTAINER) $(CLOUDFLARE_CONTAINER) $(APP_CONTAINERS) travian-bot auth-service || true

# --- REBUILD APP ---
build-travian-bot:
	docker build -t $(TRAVIAN_BOT_IMAGE) $(TRAVIAN_BOT_SRC)

