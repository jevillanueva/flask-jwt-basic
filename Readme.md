# Para levantar el servicio utilizar
```
$ docker-compose up --build -d
```
# Para navegar por la base de datos redis
```
$ docker-compose exec redis redis-cli
```
## Para navegar con redis cli ver todos los keys
```
> KEYS *
``` 
## Para ver con redis cli la expiracion de un key
```
> TTL "KEY"
``` 
## Para ver el contenido en redis cli la expiracion de un key
```
> GET "KEY"
``` 