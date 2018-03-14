import numpy as np
from scipy.stats import uniform, erlang
from bokeh.io import curdoc, show, output_file, push_notebook, output_notebook
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot, layout, row, column, widgetbox
from bokeh.models.widgets import Slider, RangeSlider, TextInput
from bokeh.plotting import figure
from bokeh.models import HoverTool


###-----------------------------------------------------------------------###
###------------------------PARAMETER DEFAULTS-----------------------------###
### This section contains defaults and ranges for the Bokeh controls and  ###
### may be modified without concern, if required. ("View" Part 1)         ###
###-----------------------------------------------------------------------###
# The format for this section is: default, range[Lower, Upper, Step Size]
d_N = 5000 # number of points
d_xmin, d_xmax, r_xminmax = -10, 10, [-100, 100, 0.1] # data will be generated for [xmin, xmax]
# uniform distribution parameters
d_uni_a, d_uni_b, r_uni_ab = 0, 1, [-20, 20, 0.1] # a, b
# erlang distribution parameters
d_erl_k, r_erl_k = 1, [1, 20, 1] # k
d_erl_teta, r_erl_teta = 1, [0.1, 20, 0.1] # k


x = np.linspace(d_xmin, d_xmax, N)
y_uni_pdf = uniform.pdf(x, loc=d_uni_a, scale=(d_uni_b - d_uni_a))
y_uni_cdf = uniform.cdf(x, loc=d_uni_a, scale=(d_uni_b - d_uni_a))

y_cust_pdf = erlang.pdf(x, a=d_erl_k, scale=d_erl_teta)
y_cust_cdf = erlang.cdf(x, a=d_erl_k, scale=d_erl_teta)

data_uniform = {'x': x,
                'y_pdf': y_uni_pdf,
                'y_cdf': y_uni_cdf}

source_uniform = ColumnDataSource(data=data_uniform)

data_custom = {'x': x,
                'y_pdf': y_cust_pdf,
                'y_cdf': y_cust_cdf}

source_custom = ColumnDataSource(data=data_custom)

# set up plot
pdf_col = 'DarkBlue'
cdf_col = 'YellowGreen'
tools = "pan,wheel_zoom,box_zoom,reset,save"
hover = HoverTool(
    tooltips=[("(x,y)", "($x, $y)")],
    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
)

# uniform distribution
plot_uniform = figure(title='Uniform distribution', plot_height=300, plot_width=450,
                      toolbar_location="below", tools=tools, x_range=(-1,2))
plot_uniform.add_tools(hover)
#plot_uniform.background_fill_color = "SeaShell"
#plot_uniform.background_fill_alpha = 0.1
plot_uniform.border_fill_color = "whitesmoke"
plot_uniform.border_fill_alpha = 0.5
plot_uniform.min_border_left = 40
plot_uniform.min_border_right = 40
plot_uniform.xaxis.axis_label = "x"
plot_uniform.yaxis.axis_label = "f(x)"
uni_func_pdf = plot_uniform.line(x='x', y='y_pdf', source=source_uniform,
                                 color=pdf_col, line_width=3, legend='pdf',
                                 muted_color=pdf_col, muted_alpha=0.35)
uni_func_cdf = plot_uniform.line(x='x', y='y_cdf', source=source_uniform,
                                 color=cdf_col, line_width=3, legend='cdf',
                                 muted_color=cdf_col, muted_alpha=0.35,
                                 line_dash='dashed')
plot_uniform.legend.click_policy='mute'

# uniform widgets
sld_uni_xminmax = RangeSlider(start=r_xminmax[0], end=r_xminmax[1], value=(d_xmin, d_xmax), step=r_xminmax[2], title='[xmin, xmax]', width=450)
sld_uni_ab = RangeSlider(start=r_uni_ab[0], end=r_uni_ab[1], value=(d_uni_a, d_uni_b), step=r_uni_ab[2], title='[a, b]', width=450)

# custom distribution
plot_custom = figure(title='Erlang distribution', plot_height=300, plot_width=450,
                     toolbar_location="below", tools=tools, x_range=(-1,10))
plot_custom.add_tools(hover)
#plot_custom.background_fill_color = "SeaShell"
#plot_custom.background_fill_alpha = 0.1
plot_custom.border_fill_color = "whitesmoke"
plot_custom.border_fill_alpha = 0.5
plot_custom.min_border_left = 40
plot_custom.min_border_right = 40
plot_custom.xaxis.axis_label = "x"
plot_custom.yaxis.axis_label = "f(x)"
cust_func_pdf = plot_custom.line(x='x', y='y_pdf', source=source_custom,
                                 color=pdf_col, line_width=3, legend='pdf',
                                 muted_color=pdf_col, muted_alpha=0.35)
cust_func_cdf = plot_custom.line(x='x', y='y_cdf', source=source_custom,
                                 color=cdf_col, line_width=3, legend='cdf',
                                 muted_color=cdf_col, muted_alpha=0.35,
                                 line_dash='dashed')
plot_custom.legend.click_policy='mute'

# custom widgets
sld_cust_xminmax = RangeSlider(start=r_xminmax[0], end=r_xminmax[1], value=(d_xmin, d_xmax), step=r_xminmax[2], title='[xmin, xmax]', width=450)
sld_cust_k = Slider(start=r_erl_k[0], end=r_erl_k[1], value=d_erl_k, step=r_erl_k[2], title='k', width=450)
sld_cust_teta = Slider(start=r_erl_teta[0], end=r_erl_teta[1], value=d_erl_teta, step=r_erl_teta[2], title='teta', width=450)


def update_uniform_data(attrname, old, new):
	xmin, xmax = sld_uni_xminmax.value
	a, b = sld_uni_ab.value
	scale = b - a
	
	x = np.linspace(xmin, xmax, N)
	y_uni_pdf = uniform.pdf(x, loc=a, scale=scale)
	y_uni_cdf = uniform.cdf(x, loc=a, scale=scale)
	
	data_uniform = {'x': x,
                'y_pdf': y_uni_pdf,
                'y_cdf': y_uni_cdf}

	source_uniform.data = data_uniform
	
def update_custom_data(attrname, old, new):
	xmin, xmax = sld_cust_xminmax.value
	k = sld_cust_k.value
	teta = sld_cust_teta.value
	
	x = np.linspace(xmin, xmax, N)
	y_cust_pdf = erlang.pdf(x, a=k, scale=teta)
	y_cust_cdf = erlang.cdf(x, a=k, scale=teta)
	
	data_custom = {'x': x,
					'y_pdf': y_cust_pdf,
					'y_cdf': y_cust_cdf}

	source_custom.data = data_custom
	
for w in [sld_uni_xminmax, sld_uni_ab]:
    w.on_change('value', update_uniform_data)
	
for w in [sld_cust_xminmax, sld_cust_k, sld_cust_teta]:
    w.on_change('value', update_custom_data)
	
curdoc().add_root(layout([
        [plot_uniform, plot_custom],
        [widgetbox([sld_uni_xminmax, sld_uni_ab]), widgetbox([sld_cust_xminmax, sld_cust_k, sld_cust_teta])]
    ], sizing_mode='scale_width'))
curdoc().title = "Distributions"