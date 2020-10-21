#################
#### imports ####
#################
from flask import render_template
 
from . import summarization_blueprint

@summarization_blueprint.route('/summarization')
def index():
    return render_template('summarization.html')