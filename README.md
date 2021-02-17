![png](/examples/highlight_text_logo.png)

# highlight_text

This package provides a HighlightText class and two wrapper functions that allow you to plot text with `<highlighted substrings>` in matplotlib:
 - ax_text for plotting onto an axes in data coordinates.  
 - fig_text for plotting onto the figure in figure coordinates.  

They take a string with substring delimiters = ['<', '>'] to be highlighted according to the specified highlight colors.

The example below prints the text <font color='yellow'>sunny</font> as yellow and <font color='grey'>cloudy</font> as grey.

A minimal example would be:  

```python
import matplotlib.pyplot as plt
from highlight_text import HighlightText, ax_text, fig_text
# or
import highlight_text # then use highlight_text.ax_text or highlight_text.fig_text
```

## Plotting in axes coordinates

```python
fig, ax = plt.subplots()  

# You can either create a HighlightText object
HighlightText(x=0.25, y=0.5,
              s='The weather is <sunny>\nYesterday it was <cloudy>',
              highlight_textprops=[{"color": 'yellow'},
                                   {"color": 'grey'}],
              ax=ax)

# You can use the wrapper around the class
ax_text(x = 0, y = 0.5,
        s='The weather is <sunny>\nYesterday it was <cloudy>',
        highlight_textprops=[{"color": 'yellow'},
                             {"color": 'grey'}],
        ax=ax)
```

## Plotting in figure coordinates:

```python
fig, ax = plt.subplots()  

# either pass 'boxcoords': fig.transFigure into the annotation_bbox_kw:

HighlightText(x=0.25, y=0.5,
              s='The weather is <sunny>\nYesterday it was <cloudy>',
              highlight_textprops=[{"color": 'yellow'},
                                   {"color": 'grey'}],
              annotationbbox_kw={'boxcoords': fig.transFigure})

# or use the wrapper around the class
fig_text(x=0.25, y=0.5,
         s='The weather is <sunny>\nYesterday it was <cloudy>',
         highlight_textprops=[{"color": 'yellow'},
                              {"color": 'grey'}])

```

You can pass all matplotlib.Text keywords to HighlightText for all text,  
and into the highlight_textprops for each of the text highlights.


## Using Path Effects

```python
```

## Using BBox

```python
```

## Creating axes insets on top of highlighted subtrings

```python
```




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
