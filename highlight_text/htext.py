import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.offsetbox import AnnotationBbox, TextArea, HPacker, VPacker
import ast
import warnings


def get_bbox_bounds(bbox_array):
    """
    returns the x, y, width and height of a bounding box object
    
    """
    x = bbox_array[0, 0]
    y = bbox_array[0, 1]
    width, height = np.diff(bbox_array, axis=0)[0]
    return (x, y, width, height)


class HighlightRow:
    """
    Creates TextArea objects for each row substring and aligns them horizontally using HPacker.
    Uses substring specific textprops.
    """
    def __init__(self, s, pad=0, sep=0, highlight_textprops=None, delim=('<', '>'), **kwargs):
        self._pad = pad
        self._sep = sep
        self._textprops = kwargs
        self._n_highlights = s.count(delim[0])
        if highlight_textprops is not None:
            assert len(highlight_textprops) == self._n_highlights, f'Number of highlights ({self._n_highlights}) should be equal to number of highlight_textprops ({len(highlight_textprops)})'
        self._highlight_textprops = highlight_textprops
       # if highlight_insets is not None:
       #     assert len(highlight_insets) == self._n_highlights, f'Number of highlights ({self._n_highlights}) should be equal to number of highlight_textprops ({len(highlight_insets)})'
       # self.highlight_insets = highlight_insets
        self._delim = delim
        self._rowtext = s
        self._set_row_substrings()
        self._text_areas = []
        self._set_text_areas()
        self._set_hpacker()

    def _set_row_substrings(self):
        """splits a rowtext into substrings"""
        split = self._rowtext.split(self._delim[0])
        if '' in split:
            split.remove('')
        substrings = sum([substring.split(self._delim[1])
                            for substring in split], [])

        self._substrings = [_s for _s in substrings if _s != '']
        
        self._set_highlights(split)

        
    def _set_highlights(self, split):
        """
        for each substring sets whether it is a highlighted substring (contained in `< >`)
        """
        is_highlight = []
        for _s in split:
            if not self._delim[1] in _s:
                is_highlight.append(False)
            else:
                s1, s2 = _s.split(self._delim[1])
                if s2 == '':
                    is_highlight.append(True)
                else:
                    is_highlight.extend([True, False])
                    
        self._is_highlight = is_highlight
        
    def _set_text_areas(self):
        """
        creates TextArea objects for each row substring
        uses substring specific textprops following `::` within the delim'ed substring
        """
        highlight_count = 0
        for i, (s, is_highlight) in enumerate(zip(self._substrings, self._is_highlight)):
            textprops = self._textprops.copy()
            # use base textprops for all text areas
            # and update them with given textprops_kw below
            if is_highlight:
                if self._highlight_textprops is not None:
                    textprops.update(self._highlight_textprops[highlight_count])
                else:
                    if '::' in s:
                        s, textprops_kw = s.split('::')
                        textprops.update(**ast.literal_eval(textprops_kw))
                        
                highlight_count+=1
            text = TextArea(s, textprops=textprops)
            self._text_areas.append(text)

    def _set_hpacker(self):
        """creates an HPacker with all row substrings as children"""
        self._hpacker = HPacker(children=self._text_areas, align="left", pad=self._pad, sep=self._sep)

    def create_highlight_insets(self):
        """
        creates axes insets above the bboxes of the TextAreas for which highlight_inset = True
        """
        for i, (make_inset, text_area) in enumerate(zip(self.highlight_insets, self._text_areas)):
            if make_inset:
                # create the inset and store it in self.highlight_insets
                inset = bbox_axes_inset(text_area)
                self.highlight_insets[i] = inset
            else:
                # set the _highlight_inset to None
                self.highlight_insets[i] = None        


class HighlightText:
    """
    creates an AnnotationBbox that holds HighlightRows for each row within `s`
    that are aligned vertically using VPacker.
    
    textprop **kwargs for all texts that can be overridden
    with substring specific textprops either:
        by using `::{"size": 12, "color": 'yellow'}` within the <highlighted> substring.
        or by using highlight_textprops = [{"size": 12, "color": 'yellow'}]
    
    example: HighlightText(s='The weather is <sunny::{"color": "yellow"}>\n'
                             'Yesterday it was <cloudy::{"color": "grey"}>', x=0.25, y=0.5)
              
              HighlightText(s='The weather is <sunny>\nYesterday it was <cloudy>', x=0.25, y=0.5,
                            highlight_textprops=[{"color": 'yellow'},
                                                 {"color": 'grey'}])
             
    building on: https://stackoverflow.com/questions/63659519/plotting-text-using-textarea-and-annotationbbox-in-matplotlib
    """
    def __init__(self, x, y, s, ha='left', va='top',
                 highlight_textprops=None,
                 #highlight_insets=None,
                 textalign='left',
                 delim=('<', '>'),
                 annotationbbox_kw={},
                 ax=None,
                 fig=None,
                 add_artist=True,
                 vpad=0, vsep=4, hpad=0, hsep=0,
                 **kwargs):
        
        if ax is None:
            self._ax = plt.gca()
        else:
            self._ax = ax

        if fig is None:
            self._fig = plt.gcf()
        else:
            self._fig = fig
            
        self._add_artist = add_artist

        self._x = x
        self._y = y
        self._vpad = vpad
        self._vsep = vsep
        self._hpad = hpad
        self._hsep = hsep
        self._text = s
        self._text_align = textalign
        self._textprops = kwargs
        self._delim = delim
        self._textrows = self._text.split('\n')
        self._highlights_per_row = [row.count(delim[0]) for row in self._textrows]
        if highlight_textprops is not None:
            assert len(highlight_textprops) == sum(self._highlights_per_row), f'Number of highlights ({sum(self._highlights_per_row)}) should be equal to number of highlight_textprops ({len(highlight_textprops)})'
        self._highlight_textprops = highlight_textprops
       # if highlight_insets is not None:
       #     assert len(highlight_insets) == sum(self._highlights_per_row), f'Number of highlights ({sum(self._highlights_per_row)}) should be equal to number of highlight_insets ({len(highlight_insets)})'
       # self.highlight_insets = highlight_insets
        self._n_rows = len(self._textrows)
        self._set_box_alignment(ha, va)
        self._set_highlight_rows()
        self._set_text_areas()
        self._set_is_highlight()
        self._annotationbbox_kw = annotationbbox_kw
        if 'frameon' not in self._annotationbbox_kw:
            self._annotationbbox_kw['frameon'] = False
        self._set_annotation_box()
    
    def _set_box_alignment(self, ha, va):
        # AnnotationBox vertical box_alignment
        if va == 'bottom':
            self.va_align = 0
        elif va == 'top':
            self.va_align = 1
        elif va == 'center':
            self.va_align = 0.5
        else:
            raise ValueError('vertical alignment needs to be either left, right or center.')

        # AnnotationBox horizontal box_alignment
        if ha == 'left':
            self.ha_align = 0
        elif ha == 'right':
            self.ha_align = 1
        elif ha == 'center':
            self.ha_align = 0.5
        else:
            raise ValueError('horizontal alignment needs to be either top, bottom or center.')

        self.box_alignment = (self.ha_align, self.va_align)

    def _set_highlight_rows(self):
        """ for each textrow create an HighlightRow"""
        self._hpackers = []
        self._highlight_rows = []
        for i, row in enumerate(self._textrows):
            if self._highlight_textprops is not None:
                row_highlight_textprops = self._highlight_textprops[sum(self._highlights_per_row[:i]):sum(self._highlights_per_row[:i+1])]
               # row_highlight_insets = self.highlight_insets[sum(self._highlights_per_row[:i]):sum(self._highlights_per_row[:i+1])]
            else:
                row_highlight_textprops = None
               # row_highlight_insets = None
            highlight_row = HighlightRow(row, pad=self._hpad, sep=self._hsep, delim=self._delim,
                                         highlight_textprops=row_highlight_textprops, 
                                      #   highlight_insets=row_highlight_insets, 
                                         **self._textprops)
            self._highlight_rows.append(highlight_row)
            self._hpackers.append(highlight_row._hpacker)
            self._set_text_areas()
            
    def _set_text_areas(self):
        self.text_areas = []
        for hrow in self._highlight_rows:
            self.text_areas.append(hrow._text_areas)
        self.text_areas = [item for sublist in self.text_areas for item in sublist]
        
    def _set_is_highlight(self):
        self.is_highlight = []
        for hrow in self._highlight_rows:
            self.is_highlight.append(hrow._is_highlight)
        self.is_highlight = [item for sublist in self.is_highlight for item in sublist]
        
    def get_highlight_areas(self):
        return [text_area for text_area, is_highlight in zip(self.text_areas, self.is_highlight) if is_highlight]
        
    def _set_annotation_box(self):
        """pack the HPackers of each row vertically into a VPacker and create an AnnotationBBox"""
        self._vpacker = VPacker(children=self._hpackers, pad=self._vpad, sep=self._vsep, align=self._text_align)
        self.annotation_bbox = AnnotationBbox(self._vpacker,
                                              (self._x, self._y),
                                              box_alignment=self.box_alignment,
                                              **self._annotationbbox_kw)
        
        #self._fig.canvas.draw()
        if self._add_artist:
            self._ax.add_artist(self.annotation_bbox)
            
        """        if any(self.highlight_insets):
                self.highlight_insets = []
                for hrow in self._highlight_rows:
                    hrow.create_highlight_insets()
                    print(hrow.highlight_insets)
                    self.highlight_insets.append(hrow.highlight_insets)
                self.highlight_insets = [item for sublist in self.highlight_insets for item in sublist]  """ 
            
    def make_highlight_insets(self, make_highlight_insets):
        
        highlight_areas = self.get_highlight_areas()
        
        assert len(make_highlight_insets) == len(highlight_areas), f'Number of highlights ({len(highlight_areas)}) should be equal to number of make_inset ({len(make_highlight_insets)})'
        
        self.highlight_axes = []
        
        for make_inset, text_area in zip(make_highlight_insets, highlight_areas):
            if make_inset:
                # create the inset and store it in self.highlight_insets
                inset = self.make_bbox_axes_inset(text_area)
                self.highlight_axes.append(inset)
            else:
                # set the _highlight_inset to None
                self.highlight_axes.append(None)
                
    def make_bbox_axes_inset(self, obj, fig=None, ax=None, zorder=99, axis='off', facecolor='None'):
        """
        add another axes to the figure in the position and extent of obj
        for a matplotlib object that has the get_window_extent function

        by default sets the axis zorder to 99
        turns the axis 'off'
        and sets the facecolor to None

        Parameters:
        ----------
        obj : a matplotlib object with the get_window_extent function
        fig = None : a plt.figure object
        zorder = -1 : float 
        axis = 'off' : bool or str - see help(plt.axis) for possible values
        facecolor = 'None': str

        """
        fig = self._fig

        if isinstance(obj, TextArea) or isinstance(obj, AnnotationBbox):
            if 'inline' not in mpl.get_backend():
                plt.show(block=False)

        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()

        # bounding box of the object | Axes Coordinates
        win_ext = obj.get_window_extent(renderer)

        # transform to Figure Coordinates
        bbox_bounds = get_bbox_bounds(fig.transFigure.inverted().transform(win_ext))
        
        ax_inset = fig.add_axes(bbox_bounds)
        ax_inset.set_zorder(zorder)
        ax_inset.axis(axis)
        ax_inset.set_facecolor(facecolor)

        return ax_inset
            
            
def ax_text(x, y, s, ha='left', va='top',
            highlight_textprops=None,
        #  highlight_insets=None,
            textalign='left',
            delim=('<', '>'),
            annotationbbox_kw={},
            ax=None,
            fig=None,
            add_artist=True,
            vpad=0, vsep=4, hpad=0, hsep=0,
            **kwargs):
    
    return HighlightText(x, y, s, ha=ha, va=va,
                        highlight_textprops=highlight_textprops,
                    #   highlight_insets=highlight_insets,
                        textalign=textalign,
                        delim=delim,
                        annotationbbox_kw=annotationbbox_kw,
                        ax=ax,
                        fig=fig,
                        add_artist=add_artist,
                        vpad=vpad, vsep=vsep, hpad=hpad, hsep=hsep,
                        **kwargs)
    
    
def fig_text(x, y, s, ha='left', va='top',
            highlight_textprops=None,
        #   highlight_insets=None,
            textalign='left',
            delim=('<', '>'),
            annotationbbox_kw={},
            ax=None,
            fig=None,
            add_artist=True,
            vpad=0, vsep=4, hpad=0, hsep=0,
            **kwargs):
    
    if fig is None:
        fig = plt.gcf()
    
    annotationbbox_kw.update({'boxcoords': fig.transFigure})
    
    return HighlightText(x, y, s, ha=ha, va=va,
                        highlight_textprops=highlight_textprops,
                        # highlight_insets=highlight_insets,
                        textalign=textalign,
                        delim=delim,
                        annotationbbox_kw=annotationbbox_kw,
                        ax=ax,
                        fig=fig,
                        add_artist=add_artist,
                        vpad=vpad, vsep=vsep, hpad=hpad, hsep=hsep,
                        **kwargs)
