Docker command to push the image to docker registry

```
docker buildx build --platform linux/amd64 -t vikrambhat2/sapaicore_exec_wml:latest -f Dockerfile --push --no-cache .
```
