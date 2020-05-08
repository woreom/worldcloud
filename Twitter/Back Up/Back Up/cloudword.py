#

"""
"""

from wordcloud import STOPWORDS as EN_STOPWORDS
from stopword_persian import stopword_persian as STOPWORDS
from wordcloud_fa import WordCloudFa
from hazm import Normalizer

from os import path
from PIL import Image
import numpy as np

d = path.dirname(__file__)

text = open(path.join(d, 'tweets/result.txt'), encoding='utf-8').read()

# Add another stopword
twitter_mask = np.array(Image.open(path.join(d, "input/southpark1.png")))

stopwords = set(STOPWORDS)
stopwords |= EN_STOPWORDS


# Generate a word cloud image

wordcloud = WordCloudFa(
    persian_normalize=True,
    include_numbers=False,
    max_words=200,
    stopwords=stopwords,
    margin=0,
    width=3000,
    height=3000,
    min_font_size=10,
    max_font_size=2300,
    random_state=True,
    background_color="black",
    mask=twitter_mask
).generate(text)

image = wordcloud.to_image()
image.show()
image.save('output/twitter_mask.png')

