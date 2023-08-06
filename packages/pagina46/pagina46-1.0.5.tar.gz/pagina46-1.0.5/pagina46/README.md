build pacchetto
```
./build.sh
```

build e pubblicazione pacchetto su test
```
./publish_test.sh
```

build e pubblicazione pacchetto su prod
```
./publish_prod.sh
```

installare l'app
```
INSTALLED_APPS = [
    ...
    'pagina46'
    ...
]
```

settings:
aggiungere il context processor
```
TEMPLATES = [{
    # whatever comes before
    'OPTIONS': {
        'context_processors': [
            # whatever comes before
            "pagina46.context_processors.supporto_telefonico",
            "pagina46.context_processors.show_git_info",
        ],
    }
}]
```

nel base aggiungere
```
{% load p46static %}
{% p46_css %}
```

###dev

eseguire il server pypi dopo aver installato il pacchetto per far servire i pacchetti aggiornati
```
pypi-server -p 7002 dist
```
