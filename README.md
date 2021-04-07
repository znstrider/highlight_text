![png](/examples/highlight_text_logo.png)

---

# HighlightText

The purpose of this package is to make effective annotations easier in matplotlib.

In 2020 data journalism has played a vital role in communicating to the public.
There are now many publications that routinely use various forms of colored text highlights of key information in the title, that until then has often been shown in legends.  

The HighlightText package provides a natural way to specify substrings that should be highlighted and individual font properties that should be used for each of the highlights.  
That means using different colors, shading backgrounds with bboxes, using path_effects or different fontsize, weights, or styles are all possible and you are free to choose what best supports highlighting the key information you want your viewers to know. 

# Installation

```python
pip install highlight-text
```

## Note

The newest version breaks with the prior syntax of individually specifying highlight_colors and other params for eg. bboxes and path_effects.  
You can now provide any matplotlib.text.Text keyword arguments for any of the highlighted substrings into the `highlight_textprops` parameter.  
You can familiarize yourself with the new syntax and the possibilities this provides by having a look at the examples below.  

## Use

This package provides a HighlightText class and two wrapper functions that allow you to plot text with `<highlighted substrings>` in matplotlib:
 - ax_text for plotting onto an axes in data coordinates.  
 - fig_text for plotting onto the figure in figure coordinates.  

They take a string with substring delimiters = ['<', '>'] to be highlighted according to the specified highlight_textprops. You can provide other delimiters if necessary.    
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

![Example1](/examples/Example1.png)

# Further Examples  

[1) Showcase Use: Color Encoded Title - @petermckeever](#ColorEncodingExample)  
[2) Using Path Effects](#PathEffects)  
[3) Using BBox Highlights](#BBoxHighlights)  
[4) Using Different Fontsizes](#Fontsizes)  
[5) Showcase Use: DerSpiegel](#DerSpiegel)  
[6) Custom Linespacing](#Linespacing)  
[7) Showcase Use (Axes Insets): Financial Times](#AxesInsetsShowcase)  
[8) Axes Inset](#AxesInset)  
[9) AnnotationBBox](#AnnotationBbox)  
[10) Arrowprops](#Arrowprops)  


---  
<font style="color:#2171b5; font-size:16px">You can pass all matplotlib.Text keywords to HighlightText for all text,  
and into the highlight_textprops for each of the text highlights.  
The highlight_textprops overwrite all other passed keywords for the highlighted substrings.
</font>  

---  
<a name="ColorEncodingExample"></a>
A showcase use is provided in [this notebook](/notebooks/color_encoded_title-petermckeever.ipynb)  
Source: https://twitter.com/petermckeever/status/1346075580782047233  
![ColorEncodingExample](/examples/color_encoded_title-petermckeever.png)


<a name="PathEffects"></a>
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

<a name="BBoxHighlights"></a>
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

<a name="Fontsizes"></a>
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


<a name="DerSpiegel"></a>
This example taken from german news publication "Der Spiegel" uses bbox highlights and a different fontsize for title and subtitle.

The code is provided in [this notebook](/notebooks/title_bbox_encoding_spiegel-de.ipynb)  
Source of the Graphic: https://www.spiegel.de/wissenschaft/medizin/coronavirus-in-europa-die-zweite-welle-rollt-a-1d5b12a1-162d-48a3-8e1e-40235c996080?sara_ecid=soci_upd_wbMbjhOSvViISjc8RPU89NcCvtlFcJ  

![Title BBox Example](/examples/title_bboxes_example-spiegel.png)

#### Original Graphic:  

![Original Spiegel Graphic](/examples/Das_Infektionsgeschehen_in_Europa-Der_Spiegel.png)

<a name="TextAlignment"></a>
## Text Alignment and seperation between lines

```python
highlight_textprops =\
[{"fontsize": 12, 'color': '0.4'},
 {"fontsize": 24, "weight": "bold"},
 {"fontsize": 14, "color": "0.3"}]
 
fig, ax = plt.subplots(figsize=(12, 2))  
ax.axis('off')

HighlightText(x=0.5, y=0.5,
              ha='center', va='center', # alignment of the annotationbbox
              s='<In 2021>\n'
                '<Manchester City dominates>\n'
                '<With a series of 11 straight wins City launched from trailing 8 points to being 10 points ahead of its competitors.>\n',
              highlight_textprops=highlight_textprops,
              textalign='center', # horizontal alignment of the text
              vsep=12, # vertical seperation between lines; `hsep` controls seperation of subtexts in a line.
              ax=ax)
```

![Example 8](/examples/Example8_textalign.png)


<a name="Linespacing"></a>
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


<a name="AxesInsetsShowcase"></a>
## Axes insets on top of highlighted substrings

This is great for embedding legends into your title or markers into annotations.  
Look at some of John Burn-Murdoch's (@jburnmurdoch) Plots. He has mastered this.

An Example is provided in [this notebook](/notebooks/inset_legend_in_title-financial_times.ipynb)  
Source: https://twitter.com/jburnmurdoch/status/1319277057650556936/photo/1
![Financial-Times Example](/examples/example_financial-times_jburnmurdoch.png)

<a name="AxesInset"></a>
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


<a name="AnnotationBbox"></a>
## AnnotationBbox BBox

We can also place a Bounding Box around the whole AnnotationBbox that holds all of our text by setting 'frameon': True within the annotationbbox_kw dictionary.

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


<a name="Arrowprops"></a>
## Arrowprops

The AnnotationBBox that holds our texts takes a `xybox` keyword argument that you can input to `annotationbbox_kw`.
In combination with `arrowprops` this allows us to draw an arrow from xybox to the annotation point given by (x, y).

```python
fig, ax = plt.subplots(figsize=(4, 3))  

ht = HighlightText(x=0.5, y=0.5,
                   fontsize=12,
                   ha='center', va='center',
                   s='<Annotation Title:>\nPoint 1\nPoint 2',
                   highlight_textprops=[{'size': 20}],
                   annotationbbox_kw={'frameon': True, 'pad': 1,
                                     'arrowprops': dict(arrowstyle="->"),
                                     'xybox': (3, 0.5),
                                      },
              ax=ax)

ax.set_xlim(0, 3)
```

![Example 9](/examples/Example9_arrowprops.png)

```python
"""
Args:
    x (float): x-position
    y (float): y-position
    s (str): textstring with <highlights>
    ha (str, optional): horizontal alignment of the AnnotationBbox. Defaults to 'left'.
    va (str, optional): vertical alignment of the AnnotationBbox. Defaults to 'top'.
    highlight_textprops (List[dict], optional): list of textprops dictionaries. Defaults to None.
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
