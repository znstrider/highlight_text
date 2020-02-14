### highlight_text

This package provides two functions that allow you to plot text with <highlighted substrings> in matplotlib:
 - htext for plotting onto an axes in data coordinates.  
 - fig_htext for plotting onto the figure in figure coordinates.  


They take a string with substring delimiters = ['<', '>'] to be highlighted according to highlight colors:
'The weather is <sunny> today. Yesterday it <rained>.', color = 'w', highlight_colors = ['yellow', 'grey']
prints the text in white with 'sunny' as yellow and 'rained' as grey.

You can further highlight by using  
highlight_styles ie. ['normal', 'italic', 'oblique']  
and highlight_weights ie. ['regular', 'bold'].  

Make sure to set data limits before using this function. Otherwise the data transformation will not work properly.

![png](/examples/h_text.png)

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
