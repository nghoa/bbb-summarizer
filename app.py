from flask import Flask
import views

app = Flask(__name__)

app.add_url_rule('/', view_func=views.hello)
app.add_url_rule('/data', view_func=views.get_query_string)
app.add_url_rule('/data/<param>', view_func=views.get_param)
app.add_url_rule('/table', view_func=views.table)

if __name__ == '__main__':
    app.run(host='localhost', port=8132, debug=True)