Docker command to push the image to docker registry

```
docker buildx build --platform linux/amd64 -t vikrambhat2/sapaicore_exec_wml:latest -f Dockerfile --push --no-cache .
```


Test locally:
```
docker build --platform linux/amd64 -t codetest_vb:latest .
docker run --platform linux/amd64 -d -p  8080:5000 codetest_vb:latest

curl 0.0.0.0:8080
```
