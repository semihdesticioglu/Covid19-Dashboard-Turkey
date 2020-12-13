from covidapp import app
import json, plotly
from flask import render_template
from wrangling_scripts.wrangle_data import return_figures, prepare_df

@app.route('/')
@app.route('/index')
def index():
    data = prepare_df()
    figures = return_figures()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON,data=data)