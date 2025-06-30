# Build all services
build:
	docker-compose build

# Start services
up:
	docker-compose up

# Stop services
down:
	docker-compose down

# Rebuild and restart everything
restart:
	docker-compose down
	docker-compose up --build

# View logs
logs:
	docker-compose logs -f

# Remove containers, volumes, networks
clean:
	docker-compose down -v --remove-orphans
