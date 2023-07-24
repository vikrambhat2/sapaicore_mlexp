Docker command to push the image to docker registry

```
docker buildx build --platform linux/amd64 -t vikrambhat2/deploy_autoai_model:latest -f Dockerfile --push --no-cache .
```
