from flask import Flask, render_template, request
from youtubesearchpython import VideosSearch

app = Flask(__name__)

def extract_keywords(channel_name):
    return [channel_name.lower(), channel_name.lower() + " review", channel_name.lower() + " tutorial"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        my_channel = request.form['my_channel']
        competitor_channel = request.form['competitor_channel']
        keywords = extract_keywords(competitor_channel)
        results = []

        for keyword in keywords:
            search = VideosSearch(keyword, limit=20)
            videos = search.result()['result']
            position = next((i + 1 for i, v in enumerate(videos) if my_channel.lower() in v['channel']['name'].lower()), None)
            results.append({'keyword': keyword, 'position': position or 'Not in top 20'})

        return render_template('result.html', results=results, my_channel=my_channel)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
