import numpy as np
from scipy.stats import uniform, erlang
from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot, layout, row, column, widgetbox
from bokeh.models.widgets import Button, Slider, RangeSlider, TextInput
from bokeh.plotting import figure
from bokeh.models import HoverTool


###-----------------------------------------------------------------------###
###------------------------PARAMETER DEFAULTS-----------------------------###
### This section contains defaults and ranges for the Bokeh controls and  ###
### may be modified without concern, if required. ("View" Part 1)         ###
###-----------------------------------------------------------------------###
# The format for this section is: default, range[Lower, Upper, Step Size]

# number of points
d_N = 10000
# data will be generated for [xmin, xmax]
d_xmin, d_xmax, r_xminmax = -10, 10, [-100, 100, 0.1]

# uniform distribution parameters
# a, b
d_uni_a, d_uni_b, r_uni_ab = 0, 1, [-20, 20, 0.1]

# erlang distribution parameters
# k
d_cust_k, r_cust_k = 1, [1, 20, 1]
# teta
d_cust_teta, r_cust_teta = 1, [0.1, 20, 0.1]



###-----------------------------------------------------------------------###
###----------------------GRAPHICAL USER INTERFACE-------------------------###
### This code defines the Bokeh controls that are used for the user       ###
### interface. All the defaults for the controls are above. This code     ###
### should not need to be modified. ("View" Part 2)                       ###
###-----------------------------------------------------------------------###
def create_plot_distribution(title, source):
    # tools for plot manipulations
    tools = "pan,wheel_zoom,box_zoom,reset,save"

    # create plot figure
    plot_figure = figure(title=title, plot_height=300, plot_width=450,
        toolbar_location="below", tools=tools, x_range=(-1,2))

    # plot properties
    #plot_figure.background_fill_color = "SeaShell"
    #plot_figure.background_fill_alpha = 0.1
    plot_figure.border_fill_color = "whitesmoke"
    plot_figure.border_fill_alpha = 0.5
    plot_figure.min_border_left = 40
    plot_figure.min_border_right = 40
    plot_figure.xaxis.axis_label = "x"
    plot_figure.yaxis.axis_label = "f(x)"

    # create pdf and cdf lines for distribution
    pdf_line_color = 'DarkBlue'
    cdf_line_color = 'YellowGreen'
    line_pdf = plot_figure.line(x='x', y='y_pdf', source=source,
        color=pdf_line_color, line_width=3, legend='pdf',
        muted_color=pdf_line_color, muted_alpha=0.2)
    line_cdf = plot_figure.line(x='x', y='y_cdf', source=source,
        color=cdf_line_color, line_width=3, legend='cdf',
        muted_color=cdf_line_color, muted_alpha=0.2,
        line_dash='dashed')

    # create custom HoverTools separately for pdf and cdf
    hover_pdf = HoverTool(
        renderers=[line_pdf],
        tooltips=[('(x, y_pdf)', '($x, @y_pdf)')],
        mode='vline'
    )
    hover_cdf = HoverTool(
        renderers=[line_cdf],
        tooltips=[('(x, y_cdf)', '($x, @y_cdf)')],
        mode='vline'
    )
    plot_figure.add_tools(hover_pdf)
    plot_figure.add_tools(hover_cdf)

    # make possible to turn off charts by clicking on its legend
    plot_figure.legend.click_policy='mute'
    return plot_figure

button_reset = Button(label="Reset charts")



###-----------------------------------------------------------------------###
###------------------DATA SOURCES AND INITIALIZATION----------------------###
### This section defines the data sources which will be used in the Bokeh ###
### plots. To update a Bokeh plot in the server, each of the sources will ###
### be modified in the CALLBACKS section. ("Model")                       ###
###-----------------------------------------------------------------------###
# x data
d_x = np.linspace(d_xmin, d_xmax, d_N)

# uniform distribution
d_y_uni_pdf = uniform.pdf(d_x, loc=d_uni_a, scale=(d_uni_b - d_uni_a))
d_y_uni_cdf = uniform.cdf(d_x, loc=d_uni_a, scale=(d_uni_b - d_uni_a))

# custom distribution
d_y_cust_pdf = erlang.pdf(d_x, a=d_cust_k, scale=d_cust_teta)
d_y_cust_cdf = erlang.cdf(d_x, a=d_cust_k, scale=d_cust_teta)

d_data_uniform = {
    'x': d_x,
    'y_плотность': d_y_uni_pdf,
    'y_функция': d_y_uni_cdf
}
source_uniform = ColumnDataSource(data=d_data_uniform)

d_data_custom = {
    'x': d_x,
    'y_плотность': d_y_cust_pdf,
    'y_функция': d_y_cust_cdf
}
source_custom = ColumnDataSource(data=d_data_custom)

plot_uniform = create_plot_distribution(title='Равномерное распределение',
                                        source=source_uniform)
# uniform distribution widgets
slider_uni_xminmax = RangeSlider(start=r_xminmax[0], end=r_xminmax[1],
    value=(d_xmin, d_xmax), step=r_xminmax[2], title='[x_мин, x_макс]', width=450)
slider_uni_ab = RangeSlider(start=r_uni_ab[0], end=r_uni_ab[1],
    value=(d_uni_a, d_uni_b), step=r_uni_ab[2], title='[a, b]', width=450)

plot_custom = create_plot_distribution(title='Распределение Эрланга',
                                       source=source_custom)
# custom distribution widgets
slider_cust_xminmax = RangeSlider(start=r_xminmax[0], end=r_xminmax[1],
    value=(d_xmin, d_xmax), step=r_xminmax[2], title='[x_мин, x_макс]', width=450)
slider_cust_k = Slider(start=r_cust_k[0], end=r_cust_k[1], value=d_cust_k,
    step=r_cust_k[2], title='k', width=450)
slider_cust_teta = Slider(start=r_cust_teta[0], end=r_cust_teta[1],
    value=d_cust_teta, step=r_cust_teta[2], title='teta', width=450)



###-----------------------------------------------------------------------###
###----------------------------CALLBACKS----------------------------------###
### This section defines the behavior of the GUI as the user interacts    ###
### with the controls. ("Controller")                                     ###
###-----------------------------------------------------------------------###
def update_uniform_data(attrname, old, new):
    xmin, xmax = slider_uni_xminmax.value
    a, b = slider_uni_ab.value
    scale = b - a

    x = np.linspace(xmin, xmax, d_N)
    y_uni_pdf = uniform.pdf(x, loc=a, scale=scale)
    y_uni_cdf = uniform.cdf(x, loc=a, scale=scale)

    data_uniform = {
        'x': x,
        'y_pdf': y_uni_pdf,
        'y_cdf': y_uni_cdf
    }
    source_uniform.data = data_uniform

def update_custom_data(attrname, old, new):
    xmin, xmax = slider_cust_xminmax.value
    k = slider_cust_k.value
    teta = slider_cust_teta.value

    x = np.linspace(xmin, xmax, d_N)
    y_cust_pdf = erlang.pdf(x, a=k, scale=teta)
    y_cust_cdf = erlang.cdf(x, a=k, scale=teta)

    data_custom = {
        'x': x,
        'y_pdf': y_cust_pdf,
        'y_cdf': y_cust_cdf
    }
    source_custom.data = data_custom

def reset_plot():
    source_uniform.data = d_data_uniform
    source_custom.data = d_data_custom

    slider_uni_xminmax.value = d_xmin, d_xmax
    slider_uni_ab.value = d_uni_a, d_uni_b

    slider_cust_xminmax.value = d_xmin, d_xmax
    slider_cust_k.value = d_cust_k
    slider_cust_teta.value = d_cust_teta


# attach update to uniform distribution
for w in [slider_uni_xminmax, slider_uni_ab]:
    w.on_change('value', update_uniform_data)

# attach update to custom distribution
for w in [slider_cust_xminmax, slider_cust_k, slider_cust_teta]:
    w.on_change('value', update_custom_data)

button_reset.on_click(reset_plot)

###-----------------------------------------------------------------------###
###----------------------------PAGE LAYOUT--------------------------------###
### This section defines the basic layout of the GUI. ("View" Part 3)     ###
###-----------------------------------------------------------------------###
curdoc().add_root(
    layout([
        [
            plot_uniform,
            plot_custom
        ],
        [
            widgetbox([slider_uni_xminmax, slider_uni_ab]),
            widgetbox([slider_cust_xminmax, slider_cust_k, slider_cust_teta])
        ],
        [
            button_reset
        ]
    ], sizing_mode='scale_width')
)
curdoc().title = "Распределения"
