# docker-superset-worker    
Dockerfile and config files for superset async query worker service, using following settings.
- mysql as metadata storage
- redis as asyc query message broker
- redis as asyc query result storage

# docker specification
```
# use default worker number.
docker run -d --name=superset-worker malebear311/superset-worker

# config worker number.
docker run -d --name=superset-worker malebear311/superset-worker worker -w 20
```

You can specify following ENVs when execute docker run command. So the container will create with your config.
- SUPERSET_METADATA_CONNECTION: mysql url of superset metadata storage, must like *mysql://root:gt86589089@galera-lb.galera:3306/superset*.
- APPLICATION_PREFIX: key prefix of data cache and async query result.
- BROKER_URL: redis url of async message broker, must like *redis://redis-master.Redis-cluster:6379/1*.
- CELERY_RESULT_BACKEND: redis url of async query result storage, must like *redis://redis-master.Redis-cluster:6379/1*.