import base64
from flask import Flask, render_template, request
import pandas as pd
import pickle
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for rendering charts
import matplotlib.pyplot as plt
import seaborn as sns

# Load the pickled data
with open('decision_tree_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Convert the loaded object to a pandas DataFrame
X_train = pd.read_csv('NGO Response - Form responses 1.csv')
df = pd.DataFrame(X_train.values, columns=X_train.columns)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    column = request.form['column']
    if column in df.columns:
        chart = generate_chart(df[column], column)
        return render_template('analyze.html', chart=chart)
    else:
        return 'Invalid column name'

def generate_chart(data, column):
    # Determine the appropriate chart based on the column type
    if data.dtype.kind == 'O':
        # Categorical column
        chart = render_bar_chart(data.value_counts(), column)
    elif data.dtype.kind == 'i':
        # Integer column
        chart = render_histogram(data, column)
    else:
        # Continuous column
        chart = render_scatter_plot(data, column)
    
    return chart

def render_bar_chart(data, column):
    fig, ax = plt.subplots(figsize=(8, 6))
    data.plot(kind='bar', ax=ax)
    ax.set_title(f'Distribution of {column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Count')
    return render_chart(fig)

def render_histogram(data, column):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(data, kde=True, ax=ax)
    ax.set_title(f'Distribution of {column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Count')
    return render_chart(fig)

def render_scatter_plot(data, column):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(data.index, data)
    ax.set_title(f'Distribution of {column}')
    ax.set_xlabel('Index')
    ax.set_ylabel(column)
    return render_chart(fig)

def render_chart(fig):
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    chart_url = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return chart_url

if __name__ == '__main__':
    app.run(debug=True)