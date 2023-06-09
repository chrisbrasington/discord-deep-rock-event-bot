# discord-deep-rock-event-bot

`docker build -t deep-rock-bot .`

```
docker stop deep-rock-bot           # Stop the existing container
docker rm deep-rock-bot             # Remove the existing container
docker run -d -t --name deep-rock-bot deep-rock-bot:latest  # Run the new container
```

`docker logs -f deep-rock-bot`