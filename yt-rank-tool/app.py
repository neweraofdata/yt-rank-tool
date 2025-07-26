from flask import Flask, render_template, request
from youtubesearchpython import VideosSearch

app = Flask(__name__)

COMMON_KEYWORDS = [
    "data analysis", "excel tutorial", "power bi", "dashboard",
    "pivot table", "python data analysis"
]

def get_video_rank(keyword, channel_name):
    try:
        search = VideosSearch(keyword, limit=20)
        results = search.result()['result']
        for index, video in enumerate(results):
            if channel_name.lower() in video['channel']['name'].lower():
                return index + 1
        return None
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    your_channel = request.form['your_channel'].strip()
    competitor_channel = request.form['competitor_channel'].strip()

    ranks = []
    for keyword in COMMON_KEYWORDS:
        your_rank = get_video_rank(keyword, your_channel)
        competitor_rank = get_video_rank(keyword, competitor_channel)
        ranks.append({
            'keyword': keyword,
            'your_rank': your_rank if your_rank else "Not Ranked",
            'competitor_rank': competitor_rank if competitor_rank else "Not Ranked"
        })

    return render_template('result.html', ranks=ranks, your_channel=your_channel, competitor_channel=competitor_channel)
