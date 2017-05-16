import sys
import os

mod, start = sys.argv[1:]
start = int(start)
mod = int(mod)

import pandas as pd
from goose import Goose

# Load CSV and get stories
data = pd.read_csv('~/Downloads/stories_1000000.csv')
stories = data.dropna(subset=['url'])
stories = stories.sort_values("id", ascending = False)

# Download stuff
g = Goose()

for index, story in stories.iterrows():
    story.id = int(story.id)
    if int(story.id) % 3 != mod or story.id >= start:
    	continue

    filename = 'stories/%s.txt' % story.id

    if os.path.isfile(filename):
        continue

    print story.id, story.title
    
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
