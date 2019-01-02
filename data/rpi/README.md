subscribers.py registra la cantidad de subscriptores cada 30 minutos con ayuda de `crontab`:

    */30 * * * * cd /home/pi/path/to/directory/; /usr/local/bin/python3.7 subscribers.py

Nótese que el archivo generado, subscriber_count, es comprimido.