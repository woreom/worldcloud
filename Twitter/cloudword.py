#

"""
If you want to make a picture using a name
"""

from wordcloud import STOPWORDS as EN_STOPWORDS
from wordcloud import ImageColorGenerator
from stopword_persian import stopword_persian as STOPWORDS
from wordcloud_fa import WordCloudFa
from hazm import Normalizer

##import nltk # Natural Language ToolKit
##nltk.download('stopwords')
from nltk.corpus import stopwords # to get rid of StopWords

from os import path, getcwd
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude

ADD_STOPWORDS=['fuck','fuckhmmmm','hmmmm','نکن','ميساخته','ميخواستم', '!؟','!','؟','=)',"!","?"]

def make_wordcloud(font_path=None,username='woreom',img="southpark2.png", add_stopwords=ADD_STOPWORDS, bg_color='black', include_numbers=True, max_words=500, random_color=False, complex_img=True):
    assert type(add_stopwords)== type(list())
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else getcwd()

    # load text
    text = open(path.join(d, 'tweets/{}_result.txt'.format(username)), encoding='utf-8').read()

    # load image. This has been modified in gimp to be brighter and have more saturation.
    image = np.array(Image.open(path.join(d, "input/bw_{}".format(img))))

    # subsample by factor of 3. Very lossy but for a wordcloud we don't really care.
    mask_color = np.array(Image.open(path.join(d, "input/{}".format(img))))

    # create mask  white is "masked out"
    twitter_mask = image.copy()
    if complex_img:
        twitter_mask[twitter_mask.sum(axis=2) == 0] = 255

    # some finesse: we enforce boundaries between colors so they get less washed out.
    # For that we do some edge detection in the image
        edges = np.mean([gaussian_gradient_magnitude(mask_color[:, :, i] / 255., 2) for i in range(3)], axis=0)
        twitter_mask[edges > .02] = 255

    # Add another stopword
    stop_words = stopwords.words('english')
    ##stop_words_fa = stopwords.words('farsi')
    for word in add_stopwords:
        STOPWORDS.add(Normalizer().normalize(word))
    stop_words.extend(STOPWORDS)
    stop_words.extend(EN_STOPWORDS)
    stop_words = set(stop_words)

    # Getting rid of the stopwords
    text_list = [word for word in text.split() if word not in stop_words]

    # Converting the list to a text
    text = ' '.join([str(elem) for elem in text_list])
    text.replace('\u200c','')

    # Generate a word cloud image

    wordcloud = WordCloudFa(
        font_path=font_path,
        persian_normalize=True,
        include_numbers=include_numbers,
        max_words=max_words,
        stopwords=stop_words,
        margin=0,
        width=3000,
        height=3000,
        min_font_size=1,
        max_font_size=2300,
        random_state=True,
        background_color=bg_color,
        mask=image,
        relative_scaling=0,
        repeat=True
    ).generate(text)

    if not random_color:
        image_colors = ImageColorGenerator(mask_color)
        wordcloud.recolor(color_func=image_colors)
    image = wordcloud.to_image()
    image.show()
    image.save('output/twitter_mask.png')

if __name__ == '__main__':
##    make_wordcloud(font_path=None,max_words=10000, complex_img=False,random_color=False, bg_color='black', include_numbers=True, username='Hedyeh_AD', img="gift.jpg")
    make_wordcloud(font_path=None,max_words=10000,
                   complex_img=True,random_color=False,
                   username='a_sheikhahmadi',img="qanun.png",
                   bg_color='white', include_numbers=True, add_stopwords=ADD_STOPWORDS)
