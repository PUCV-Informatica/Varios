## Comandos para docker en prod

```
sudo docker build -t rootcl/py38:1.0 .

sudo docker run -it -d  --name mh1 rootcl/py38:1.0

sudo docker exec -it mh1 bin/bash

```
