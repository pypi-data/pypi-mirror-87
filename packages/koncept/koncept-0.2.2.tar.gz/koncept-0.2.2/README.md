# Koncept Image Quality Assessment Models

```
from kuti import applications as apps
from kuti import generic as gen
from kuti import image_utils as iu
import pandas as pd, numpy as np, os, urllib

# download and read the meta-data for the KonIQ-10k IQA database
koniq_meta_url = "https://github.com/subpic/koniq/raw/master/metadata/koniq10k_distributions_sets.csv"
urllib.request.urlretrieve(koniq_meta_url, 'koniq10k_distributions_sets.csv')
df = pd.read_csv('koniq10k_distributions_sets.csv')

# download some images from the test set of the database via direct link
url_list = 'http://media.mmsp-kn.de/koniq10k/1024x768/' + df[df.set=='test'].image_name[::50]
gen.make_dirs('tmp/')
for url in url_list:
    file_name = url.split('/')[-1]
    urllib.request.urlretrieve(url, 'tmp/'+file_name)

from koncept.models import Koncept512
k = Koncept512()

# read images and assess their quality
images = [iu.read_image(p) for p in 'tmp/' + df[df.set=='test'].image_name[::50]]
MOS_pred = k.assess(images)

# compare with the ground-truth quality mean opinion scores (MOS)
MOS_ground = df[df.set=='test'].MOS[::50]
apps.rating_metrics(MOS_ground, MOS_pred);
```