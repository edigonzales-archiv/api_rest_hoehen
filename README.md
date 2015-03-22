## virtualenv

```
sudo apt-get install python-pip
sudo pip install virtualenv virtualenvwrapper
```

In .bashrc einfügen:

```
if [ -f /usr/local/bin/virtualenvwrapper.sh ]; then
    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh
fi
```

## Projekt clonen

```
git clone https://edigonzales@bitbucket.org/edigonzales/api_rest_hoehen.git
```

## virtualenv einrichten

```
virtualenv venv
source venv/bin/activate
pip install flask
pip install geojson
```

## apache conf

```
WSGIScriptAlias /api/v1.0/rest/services /home/stefan/Projekte/api_rest_hoehen/wsgi/flask.wsgi
WSGIScriptReloading On

<Directory /home/stefan/Projekte/api_rest_hoehen/wsgi>
    Order deny,allow
    Allow from all
</Directory>
```

Das geht noch nicht ganz auf: Jetzt müssten sämtliche REST-Services mit diesem einen Projekt abgehandelt werden. Da muss man bei Bedarf nochmals über die Bücher. Und ohne Parameter wird ein "/" hinzugefügt und Apache meint dann "Not found". 

## Links

https://www.youtube.com/watch?v=x6SvecADw2M
http://fosshelp.blogspot.in/2014/03/how-to-deploy-flask-application-with.html


http://usrnotes.blogspot.ch/2014/06/python-development-environment-setup-in.html
https://nextdime.wordpress.com/2014/07/03/how-to-set-up-python-development-environment-ubuntu-14-04/
