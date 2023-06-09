import json
import sys
import os
import numpy as np
import matplotlib
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import pik_lib

def rectify(times_in, price_in):
    times_out = [times_in[0]]
    price_out = [price_in[0]]
    for i in range(1, len(price_in)):
        if price_in[i] != price_out[-1]:
            price_out.append(price_in[i-1])
            times_out.append(times_in[i])
        price_out.append(price_in[i])
        times_out.append(times_in[i])
    return times_out, price_out
    
db = pik_lib.Database()

with open('favourites.json', 'r') as f:
    favourites = json.load(f)

fig = plt.figure(figsize=(16, 4.8))

for flat in favourites:
    timestamps, price = db.get_price_timeline(flat['id'])
    timestamps, price = rectify(timestamps, price)
    plt.plot(timestamps, [p/1000 for p in price], '.-')

# replace timestamps with month-day labels
xmin, xmax, _, _ = plt.axis()
timestamp_ticks = np.arange(xmin - xmin % (24*60*60), xmax, 7*(24*60*60))
timestamp_labels = [datetime.fromtimestamp(t).strftime('%d %b')
                    for t in timestamp_ticks]
plt.xticks(timestamp_ticks, rotation=45)
plt.gca().set_xticklabels(timestamp_labels)

plt.grid(True)
plt.title(datetime.now().strftime('%Y-%m-%d  %H:%M:%S'))
plt.legend([flat['comment'] + ' (' + str(flat['id']) + ')'
            for flat in favourites], loc='upper left', ncol=1)
plt.show()

if not os.path.isdir('../output'):
    os.mkdir('../output')
fig.savefig('../output/favourites.png', dpi=300)

# cmap = matplotlib.cm.get_cmap('tab10')
# color=cmap(i)
