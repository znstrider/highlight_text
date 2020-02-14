### highlight_text

This package provides two functions that allow you to plot text with <highlighted substrings> in matplotlib:
 - htext for plotting onto an axes in data coordinates.  
 - fig_htext for plotting onto the figure in figure coordinates.  

They take a string with substring delimiters = ['<', '>'] to be highlighted according to highlight colors:
'The weather is (sunny) today. Yesterday it (rained).', color = 'k', highlight_colors = ['C1', 'grey']
prints the text with 'sunny' as orange and 'rained' as grey.

A minimal example would be (Replace () with delimiters <> - markdown won't show them):  

from highlight_text.htext import htext, fig_htext  

<pre><code>fig, ax = plt.subplots()  
htext(s = 'The weather is (sunny) today. Yesterday it (rained).',
          x = 0, y = 0.5,
          color = 'k', highlight_colors = ['C1', 'grey'])</code></pre>

or for the fig_htext:

<pre><code>fig, ax = plt.subplots()  
fig_htext(s = 'The weather is (sunny) today. Yesterday it (rained).',
              x = 0, y = 0.5,
              color = 'k', highlight_colors = ['C1', 'grey'])</code></pre>

You can further highlight by using  
highlight_styles ie. ['normal', 'italic', 'oblique']  
and highlight_weights ie. ['regular', 'bold'].  

This does work with linebreaks \n, fstrings and ha in ['left', 'right', 'center'] as well as va in ['botton', 'top', 'center'].

Make sure to set data limits before using this function. Otherwise the data transformation will not work properly.


### Installation

    pip install highlight-text



![png](/examples/htext.png)

Parameters:  
##########

s: text including <highlighted substrings>  
x: x position with left alignment  
y: y position  
color: textcolor of unhighlighted text  
highlight_colors: list of highlight colors  
highlight_weights = ['regular']: the fontweight used for highlighted text  
highlight_styles = ['normal']: the fontstyle used for highlighted text  
string_weight = 'regular': the fontweight used for normal text  
string_style = 'normal': the fontstyle used for normal text  
delim = ['<', '>']: delimiters to enclose the highlight substrings  
va = 'bottom', textalignment has to be in ['bottom', 'top', 'center']  
ha = 'left', textalignment has to be in ['left', 'right', 'center']  
hpadding = 0: extra padding between highlight and normal text  
linespacing = 0.25: linespacing in factor of font height between rows  
**kwargs: figure.text | plt.text kwargs  
[ax: axes to draw the text onto (in case of htext)]  
[fig: figure(in case of fig_htext)]  

Returns:  
##########

a list of texts

![Alt Text](/examples/htext.gif)
