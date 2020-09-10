![png](/examples/highlight_text_logo.png)

### highlight_text

This package provides two functions that allow you to plot text with <highlighted substrings> in matplotlib:
 - ax_text for plotting onto an axes in data coordinates.  
 - fig_text for plotting onto the figure in figure coordinates.  

They take a string with substring delimiters = ['<', '>'] to be highlighted according to highlight colors:
'The weather is (sunny) today. Yesterday it (rained).', color = 'k', highlight_colors = ['C1', 'grey']
prints the text with 'sunny' as orange and 'rained' as grey.

A minimal example would be (Replace () with delimiters <> - markdown won't show them):  

    import matplotlib.pyplot as plt
    from highlight_text import ax_text, fig_text
    # or
    import highlight_text # then use highlight_text.ax_text or highlight_text.fig_text
<pre><code>fig, ax = plt.subplots()  
ax_text(x = 0, y = 0.5,
        s = 'The weather is (sunny) today. Yesterday it (rained).'
        color = 'k', highlight_colors = ['C1', 'grey'])</code></pre>

or for the fig_text:

<pre><code>fig, ax = plt.subplots()  
fig_text(x = 0, y = 0.5,
         s = 'The weather is (sunny) today. Yesterday it (rained).',
         color = 'k', highlight_colors = ['C1', 'grey'])</code></pre>

You can further highlight by using  
highlight_styles ie. ['normal', 'italic', 'oblique']  
and highlight_weights ie. ['regular', 'bold'].  

This does work with linebreaks \n, fstrings and ha in ['left', 'right', 'center'] as well as va in ['botton', 'top', 'center'].

<b>Make sure to set data limits and if used call plt.tight_layout() before using the ax_text function. Otherwise the data transformation will not show properly.</b>


### Installation

    pip install highlight-text



![png](/examples/htext.png)

Parameters:  
##########
  
x: x position with left alignment  
y: y position  
s: text including highlighted substrings
color: textcolor of unhighlighted text  
highlight_colors: list of highlight colors  
highlight_weights = ['regular']: the fontweight used for highlighted text  
highlight_styles = ['normal']: the fontstyle used for highlighted text  
fontweight = 'regular': the fontweight used for normal text  
fontstyle = 'normal': the fontstyle used for normal text  
delim = ['<', '>']: delimiters to enclose the highlight substrings  
va = 'bottom', textalignment has to be in ['bottom', 'top', 'center']  
ha = 'left', textalignment has to be in ['left', 'right', 'center']  
hpadding = 0: extra padding between highlight and normal text  
linespacing = 0.25: linespacing in factor of font height between rows  
**kwargs: figure.text | plt.text kwargs  
[ax: axes to draw the text onto (in case of ax_text)]  
[fig: figure(in case of fig_text)]  

Returns:  
##########

a list of texts

![Alt Text](/examples/htext.gif)
