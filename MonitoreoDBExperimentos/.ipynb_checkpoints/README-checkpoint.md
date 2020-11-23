## Desde docker

```
docker pull jupyter/datascience-notebook:latest


docker run --rm -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/home/jovyan/work jupyter/datascience-notebook:latest

```