"""
Define the report styling for seaborn plots
"""
import seaborn as sns
import matplotlib.font_manager

colors = [ # define report color pallette 
    '#00A878', # green
    '#FAA31B', # orange
    '#E83834', # red
    '#FEDF40', # yellow
    '#2176AF', # blue
    '#BC67A9', # purple
    '#606060' # grey
]

custom_palette = sns.set_palette(sns.color_palette(colors))

#Set up fonts in final style with selected font

matplotlib.font_manager.fontManager.addfont('/Users/seth/Library/Fonts/Mundial Regular.ttf')

sns.set_theme(style='darkgrid',
               palette=custom_palette, 
               font='Mundial', 
               font_scale=1,
               #rc={'text.color':'black','font.weight':'black'}
               )

