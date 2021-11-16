import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as pylab
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import base64
from io import BytesIO
import uuid
from django.conf import settings



class plots():

    #global Config for plots
    #load the font
    mpl.font_manager.fontManager.addfont('{}/TwitterNLP/MiddleWare/fonts/Roboto-Regular.ttf'.format(settings.BASE_DIR))
    mpl.rc('font', family='Roboto')

    #update plt sizes
    params = {'axes.labelsize': 14,
            'axes.titlesize':20,
            'xtick.labelsize':16,
            'ytick.labelsize':14}
    pylab.rcParams.update(params)

    def generate_plt():
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight',transparent=True)
        buf.seek(0)
        img_png = buf.getvalue()
        graph = base64.b64encode(img_png)
        graph = graph.decode('utf-8')
        buf.close
        return graph

    def plot_maker(postive_count, negative_count, total_count, searchTerm):
        #generate random name
        filename = str(uuid.uuid4())

        my_colors = ['#52B8F1', '#F15265']
        sen = ['Positive', 'Negative']
        data = [postive_count, negative_count]

        #Bar chart
        fig = plt.figure(figsize = (8, 5))
        ax = fig.add_axes([0,0,1,1])
        ax.bar(sen, data, color=my_colors, width = 0.5)
        ax.set_yticks(np.arange(0, total_count+1, (total_count+1)/10))
        #make the ticks whole number
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        #remove the border form the plot
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # ax.spines['bottom'].set_visible(False)
        # ax.spines['left'].set_visible(False)

        #save the image to memoery as base64 string 
        graph = plots.generate_plt()
        # fig.savefig(f'bar-{filename}.png',bbox_inches='tight', transparent=True) #, dpi=150

        #Pie Chart
        explode = (0, 0.1)  # only "explode" the first slice 
        _, ax1 = plt.subplots(figsize = (8, 8))
        ax1.pie(data, explode=explode, labels=sen, colors=my_colors, autopct='%1.1f%%',
                shadow=True, startangle=90, textprops={'fontsize': 14})
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # fig1.savefig(f'pie{filename}.png', bbox_inches='tight',transparent=True)
        graph1 = plots.generate_plt()
        return [graph, graph1]