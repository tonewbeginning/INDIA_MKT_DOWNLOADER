import quandl
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline
apple = quandl.get("WIKI/AAPL")
plt.plot(apple.index,apple)
# plt.title('Apple Closing Price')
# plt.ylabel('Price')
# plt.show()
# var=1

# trace = go.Heatmap(z=[[1,20,30],[20,1,60],[30,60,1]])
corr = apple[['Close','High','Low','Open']].corr()
# data = [trace]
# plotly.offline.plot(data,filename='basic-heatmap')
# plotly.offline.plot(corr,filename='basic-heatmap')
a = go.Heatmap(z=corr)
plotly.offline.plot([a],filename='basic-heatmap2')
print(1)