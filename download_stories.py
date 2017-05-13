import os

import pandas as pd
from goose import Goose

# Load CSV and get stories
data = pd.read_csv('output_0.csv')
data.columns = fields = ["type", "id", "title", "score", "time", "url", "by", "text"]
stories = data[data.type == 'story']
stories = stories.dropna(subset=['url'])

# Download stuff
g = Goose()

for index, story in stories.iterrows():
    print story.id, story.title
    filename = 'stories/%s.txt' % story.id
    if os.path.isfile(filename):
        continue
    
    try:
        article = g.extract(url=story['url'])                
        with open(filename, 'w') as file:
            output = '%s|||\n\n%s' % (
                article.cleaned_text.encode('utf-8'),
                article.meta_description.encode('utf-8'),
            )
            file.write(output)
    except Exception as e:
        print(e)

