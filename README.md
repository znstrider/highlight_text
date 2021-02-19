![png](/examples/highlight_text_logo.png)

---
## This is a not fully tested full refactoring of the package.

You can download the code of the full_refactor branch or clone the repository and install the package locally
with `pip install -e .` in developer mode from the cloned directory.  
Then change to the full_refactor branch by `git checkout full_refactor` and restart your notebooks / rerun your script.

If you encounter any problems, please let me know.  

---

# highlight_text  

This package provides a HighlightText class and two wrapper functions that allow you to plot text with `<highlighted substrings>` in matplotlib:
 - ax_text for plotting onto an axes in data coordinates.  
 - fig_text for plotting onto the figure in figure coordinates.  

They take a string with substring delimiters = ['<', '>'] to be highlighted according to the specified highlight_textprops.  
You must specify a list with the same number of textprop dictionaries as you use `<highlighted substrings>`.

The example below prints the text <font color='yellow'>sunny</font> as yellow and <font color='grey'>cloudy</font> as grey.

A minimal example would be:  

```python
import matplotlib.pyplot as plt
from highlight_text import HighlightText, ax_text, fig_text
# or
import highlight_text # then use highlight_text.ax_text or highlight_text.fig_text
```

## Plotting text in axes coordinates

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

## Plotting text in figure coordinates:

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

![Example 1](/examples/Example1.png)

---  
<font style="color:#2171b5; font-size:16px">You can pass all matplotlib.Text keywords to HighlightText for all text,  
and into the highlight_textprops for each of the text highlights.  
The highlight_textprops overwrite all other passed keywords for the highlighted substrings.
</font>  

---  

A showcase use is provided in [this notebook](/notebooks/color_encoded_title-petermckeever.ipynb)  
Source: https://twitter.com/petermckeever/status/1346075580782047233  
![Color Encoding Example](/examples/color_encoded_title-petermckeever.png)

## Using Path Effects

```python
import matplotlib.patheffects as path_effects

def path_effect_stroke(**kwargs):
    return [path_effects.Stroke(**kwargs), path_effects.Normal()]
pe = path_effect_stroke(linewidth=3, foreground="orange")

highlight_textprops =\
[{"color": "yellow", "path_effects": pe},
 {"color": "#969696", "fontstyle": "italic", "fontweight": "bold"}]
 
fig, ax = plt.subplots(figsize=(4, 4))  

HighlightText(x=0.5, y=0.5,
              fontsize=16,
              ha='center', va='center',
              s='The weather is <sunny>\nYesterday it was <cloudy>',
              highlight_textprops=highlight_textprops,
              ax=ax)
```

![Example 2](/examples/Example2_path_effects.png)


## BBox highlights

Just like colored substrings or using a path_effect, using a bbox to shade the background of  
relevant text that is color coded in your plot can make a visualization much more accessible.

```python
highlight_textprops =\
[{"bbox": {"edgecolor": "orange", "facecolor": "yellow", "linewidth": 1.5, "pad": 1}},
 {"color": "#969696"}]
 
fig, ax = plt.subplots(figsize=(4, 4))  

HighlightText(x=0.5, y=0.5,
              fontsize=16,
              ha='center', va='center',
              s='The weather is <sunny>\nYesterday it was <cloudy>',
              highlight_textprops=highlight_textprops,
              ax=ax)
```

![Example 3](/examples/Example3_bbox.png)

## Different Fontsizes (ie. for Title + Subtitle)

```python
highlight_textprops =\
[{"fontsize": 24},
 {"color": "#969696"}]
 
fig, ax = plt.subplots(figsize=(4, 4))  

HighlightText(x=0.5, y=0.5,
              fontsize=16,
              ha='center', va='center',
              s='<This is a title.>\n<and a subtitle>',
              highlight_textprops=highlight_textprops,
              fontname='Roboto',
              ax=ax)
```

![Example 5](/examples/Example5_fontsizes.png)

This example taken from german news publication "Der Spiegel" uses bbox highlights and a different fontsize for title and subtitle.

The code is provided in [this notebook](/notebooks/title_bbox_encoding_spiegel-de.ipynb)  
Source of the Graphic: https://www.spiegel.de/wissenschaft/medizin/coronavirus-in-europa-die-zweite-welle-rollt-a-1d5b12a1-162d-48a3-8e1e-40235c996080?sara_ecid=soci_upd_wbMbjhOSvViISjc8RPU89NcCvtlFcJ  

![Title BBox Example](/examples/title_bboxes_example-spiegel.png)

#### Original Graphic:  

![Original Spiegel Graphic](/examples/Das_Infektionsgeschehen_in_Europa-Der_Spiegel.png)


## Custom Linespacing by using invisible text with a fitting fontsize

```python
highlight_textprops =\
[{"fontsize": 24},
 {"alpha": 0, "fontsize": 6},
 {"color": "#969696"}]
 
fig, ax = plt.subplots(figsize=(4, 4))  

HighlightText(x=0.5, y=0.5,
              fontsize=16,
              ha='center', va='center',
              s='<This is a title.>\n<ZERO ALPHA TEXT>\n<and a subtitle>',
              highlight_textprops=highlight_textprops,
              fontname='Roboto',
              ax=ax)
```

![Example 6](/examples/Example6_extra_linespacing.png)

## Axes insets on top of highlighted substrings

This is great for embedding legends into your title or markers into annotations.  
Look at some of John Burn-Murdoch's (@jburnmurdoch) Plots. He has mastered this.

An Example is provided in [this notebook](/notebooks/inset_legend_in_title-financial_times.ipynb)  
Source: https://twitter.com/jburnmurdoch/status/1319277057650556936/photo/1
![Financial-Times Example](/examples/example_financial-times_jburnmurdoch.png)

A more basic example looks like follows:  
Instead of plotting on the inset axes you can also inset images with this.

```python
highlight_textprops =\
[{"alpha": 0},
 {"alpha": 0}]
 
fig, ax = plt.subplots(figsize=(4, 4))  

ht = HighlightText(x=0.5, y=0.5,
              fontsize=16,
              ha='center', va='center',
              s='Today it rained this much <SPACE>\n'
                'Yesterday only this much  <SPACE>',
              highlight_textprops=highlight_textprops,
              ax=ax)

insets = ht.make_highlight_insets([True, True])
for haxes, color, height in zip(ht.highlight_axes, ['b', 'b'], [0.75, 0.25]):
    if haxes:
        haxes.bar(x=[0.25], height=[height], bottom=0.25, color=color, width=0.5)
        haxes.set_ylim(0, 1)
        haxes.set_xlim(0, 1)
```

<font color="red">Important:</font>   
If you make an axes inset using a script, you will have to redraw the canvas!

So at the end of your plotting call:  
```python
fig.canvas.draw()  
plt.show()
```


![Example 4](/examples/Example4_inset.png)

## AnnotationBbox BBox

We can also place a Bounding Box around the whole AnnotationBbox that holds all of our text.

```python
fig, ax = plt.subplots(figsize=(4, 2))

ht = HighlightText(x=0.5, y=0.5,
              fontsize=12,
              ha='center', va='center',
              s='<Grocery List:>\nBananas\nOatmeal',
              highlight_textprops=[{'size': 20}],
              annotationbbox_kw={'frameon': True, 'pad': 2,
                                 'bboxprops': {'facecolor': '#ebfc03', 'edgecolor': '#41b6c4', 'linewidth': 5}},
              ax=ax)
```

![Example 7](/examples/Example7_annotationbbox_bboxprops.png)

# Note:

    pip install highlight-text installs the prior stable version and not this refactor.


```python
"""
Args:
    x (float): x-position
    y (float): y-position
    s (str): textstring with <highlights>
    ha (str, optional): horizontal alignment of the AnnotationBbox. Defaults to 'left'.
    va (str, optional): vertical alignment of the AnnotationBbox. Defaults to 'top'.
    highlight_textprops (dict, optional): list of textprops dictionaries. Defaults to None.
    textalign (str, optional): Text Alignment for the AnnotationBbox. Defaults to 'left'.
    delim (tuple, optional): characters that enclose <highlighted substrings>. Defaults to ('<', '>').
    annotationbbox_kw (dict, optional): AnnotationBbox keywords. Defaults to {}.
    ax (Axes, optional): Defaults to None.
    fig (Figure, optional): Defaults to None.
    add_artist (bool, optional): Whether to add the AnnotationBbox to the axes. Defaults to True.
    vpad (int, optional): vertical padding of the HighlightRows. Defaults to 0.
    vsep (int, optional): vertical seperation between the HighlightRows. Defaults to 4.
    hpad (int, optional): horizontal padding of a rows TextAreas. Defaults to 0.
    hsep (int, optional): horizontal seperation between a rows TextAreas. Defaults to 0.
"""
```
