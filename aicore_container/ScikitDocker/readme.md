

Docker command to push the image to docker registry

```
docker buildx build --platform linux/amd64 -t vikrambhat2/vb_ml_model:latest:latest -f Dockerfile --push --no-cache .
```
