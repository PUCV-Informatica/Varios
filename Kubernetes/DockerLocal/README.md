## Comandos para docker en debug

```
sudo docker build -t rootcl/py38:debug .

sudo docker run -it -d  --name tesis -v "/Volumes/GoogleDrive/My Drive/Macbook/10 Académico/071_TesisMagisterRepo/:/workspace" rootcl/py38:debug 

sudo docker exec -it tesis bin/bash

```