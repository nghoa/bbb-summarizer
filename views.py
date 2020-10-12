from flask import Flask, render_template, request

def hello():
    return render_template('hello.html')

def album():
	return render_template('album.html')

## Getting Query String
def get_query_string():
    # request.query_string           ## Whole Request String
    metadata = {
        "conference_number": request.args.get('confnum'),
        "conference_name": request.args.get('confname')
    }

    return render_template('meta-data.html', metadata=metadata)

## Getting direct value from url
def get_param(param):
    return render_template('meta-data.html', metadata=param)

def table():
    return render_template('table.html')