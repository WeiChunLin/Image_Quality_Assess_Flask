from flask import Flask
from app import views

app = Flask(__name__) # webserver gateway interphase (WSGI)

app.add_url_rule(rule='/', endpoint='home', view_func=views.index)
app.add_url_rule(rule='/app/', endpoint='app', view_func=views.app)
app.add_url_rule(rule='/app/tool/',
                  endpoint='tool', 
                  view_func=views.tool,
                  methods=['GET', 'POST'])
app.add_url_rule('/download/<file_name>', endpoint='download_csv', view_func=views.download_csv)


if __name__ == "__main__":
    app.run(debug=True)