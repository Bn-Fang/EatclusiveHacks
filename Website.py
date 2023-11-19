from flask import Flask, render_template, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import io

app = Flask(__name__)

@app.route('/plot.png')
def plot_png():
    # Assuming your CSV has columns 'x' and 'y' for the plot
    df = pd.read_csv('RandomDataCsv.csv')
    fig = create_figure(df)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure(df):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = df['X']
    ys = df['Y']
    axis.plot(xs, ys)
    return fig

app.run(host="0.0.0.0", port = 80 )