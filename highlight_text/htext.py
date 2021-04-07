import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.offsetbox import AnnotationBbox, TextArea, HPacker, VPacker
from matplotlib.transforms import BboxTransformTo
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
        self._delim = delim
        self._rowtext = s
        self._set_row_substrings()
        self.text_areas = []
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
                _, s2 = _s.split(self._delim[1])
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

                highlight_count += 1
            text = TextArea(s, textprops=textprops)
            self.text_areas.append(text)

    def _set_hpacker(self):
        """creates an HPacker with all row substrings as children"""
        self._hpacker = HPacker(children=self.text_areas, align="left", pad=self._pad, sep=self._sep)


class HighlightText:
    """
    creates an AnnotationBbox that holds HighlightRows for each row within `s`
    that are aligned vertically using VPacker.

    textprop **kwargs for all texts that can be overridden
    with substring specific textprops either:
        by using `::{"size": 12, "color": 'yellow'}` at the end of the <highlighted> substring.
        or by using highlight_textprops = [{"size": 12, "color": 'yellow'}]

    example: HighlightText(x=0.25, y=0.5,
                           s='The weather is <sunny::{"color": "yellow"}>\n'
                             'Yesterday it was <cloudy::{"color": "grey"}>')

             HighlightText(x=0.25, y=0.5,,
                           s='The weather is <sunny>\nYesterday it was <cloudy>',
                           highlight_textprops=[{"color": 'yellow'},
                                                {"color": 'grey'}])

    by default sets annotationbbox_kw:

        'frameon' to False: to not show the bbox surrounding it

        annotation_clip to False: to draw the annotation even if xy is outside the axes (or figure)
            ```
            annotation_clipbool or None, default: None

                Whether to draw the annotation when the annotation point xy is outside the axes area.

                If True, the annotation will only be drawn when xy is within the axes.
                If False, the annotation will always be drawn.
                If None, the annotation will only be drawn when xy is within the axes and xycoords is 'data'
            ```

    building on: https://stackoverflow.com/questions/63659519/plotting-text-using-textarea-and-annotationbbox-in-matplotlib
    """

    def __init__(self, x, y, s, ha='left', va='top',
                 highlight_textprops=None,
                 textalign='left',
                 delim=('<', '>'),
                 annotationbbox_kw={},
                 ax=None,
                 fig=None,
                 add_artist=True,
                 vpad=0, vsep=4, hpad=0, hsep=0,
                 **kwargs):
        """Initialization of the HighlightText Class

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
            vpad (int, optional): external boundary padding of the VPacker (that contains all HPackers) . Defaults to 0.
            vsep (int, optional): vertical seperation between the HighlightRows. Defaults to 4.
            hpad (int, optional): internal boundary padding of the HPackers. Defaults to 0.
            hsep (int, optional): horizontal seperation between a rows TextAreas. Defaults to 0.
        """

        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax

        if fig is None:
            self.fig = plt.gcf()
        else:
            self.fig = fig

        self._add_artist = add_artist

        self._x = x
        self._y = y
        if 'xybox' in annotationbbox_kw:
            self._xybox = annotationbbox_kw.pop('xybox')
        else:
            self._xybox = None

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
        self._n_rows = len(self._textrows)
        self._set_box_alignment(ha, va)
        self._set_highlight_rows()
        self._set_text_areas()
        self._set_is_highlight()
        self._annotationbbox_kw = annotationbbox_kw
        if 'frameon' not in self._annotationbbox_kw:
            self._annotationbbox_kw['frameon'] = False
        if 'annotation_clip' not in self._annotationbbox_kw:
            self._annotationbbox_kw['annotation_clip'] = False
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
            else:
                row_highlight_textprops = None
            highlight_row = HighlightRow(row, pad=self._hpad, sep=self._hsep, delim=self._delim,
                                         highlight_textprops=row_highlight_textprops,
                                         **self._textprops)
            self._highlight_rows.append(highlight_row)
            self._hpackers.append(highlight_row._hpacker)
            self._set_text_areas()

    def _set_text_areas(self):
        self.text_areas = []
        for hrow in self._highlight_rows:
            self.text_areas.append(hrow.text_areas)
        self.text_areas = [item for sublist in self.text_areas for item in sublist]

    def _set_is_highlight(self):
        self.is_highlight = []
        for hrow in self._highlight_rows:
            self.is_highlight.append(hrow._is_highlight)
        self.is_highlight = [item for sublist in self.is_highlight for item in sublist]

    def get_highlight_areas(self):
        """Get the Highlight TextArea Objects

        Returns:
            list: list of TextArea Objects
        """
        return [text_area for text_area, is_highlight in zip(self.text_areas, self.is_highlight) if is_highlight]

    def _set_annotation_box(self):
        """pack the HPackers of each row vertically into a VPacker and create an AnnotationBBox"""
        self._vpacker = VPacker(children=self._hpackers, pad=self._vpad, sep=self._vsep, align=self._text_align)
        self.annotation_bbox = AnnotationBbox(self._vpacker,
                                              (self._x, self._y),
                                              xybox=self._xybox,
                                              box_alignment=self.box_alignment,
                                              **self._annotationbbox_kw)

        if self._add_artist:
            self.ax.add_artist(self.annotation_bbox)
            self.set_renderer()

    def make_highlight_insets(self, make_highlight_insets, **kwargs):
        """creates axes insets for each text_highlight that is passed True
        Returns a list with length n_highlights of Axes objects or None

        Args:
            make_highlight_insets (list(bool)): list of booleans with len(get_highlight_areas())

        Returns:
            highlight_axes (list(matplotlib.axes.Axes or None))
        """

        self.set_renderer()

        highlight_areas = self.get_highlight_areas()

        assert len(make_highlight_insets) == len(highlight_areas), f'Number of highlights ({len(highlight_areas)}) should be equal to number of make_inset ({len(make_highlight_insets)})'

        self.highlight_axes = []

        for make_inset, text_area in zip(make_highlight_insets, highlight_areas):
            if make_inset:
                # create the inset and store it in self.highlight_insets
                inset = self.make_bbox_axes_inset(text_area, **kwargs)
                self.highlight_axes.append(inset)
            else:
                # set the _highlight_inset to None
                self.highlight_axes.append(None)
        return self.highlight_axes

    def set_renderer(self):
        self.fig.canvas.draw()
        self.renderer = self.fig.canvas.get_renderer()

    def make_bbox_axes_inset(self, obj, axis='off', **kwargs):
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
        if 'facecolor' not in kwargs.keys():
            kwargs.update({'facecolor': 'None'})

        if 'zorder' not in kwargs.keys():
            kwargs.update({'zorder': 99})

        if isinstance(obj, TextArea) or isinstance(obj, AnnotationBbox):
            if 'inline' not in mpl.get_backend():
                plt.show(block=False)

        # bounding box of the object | Axes Coordinates
        win_ext = obj.get_window_extent(self.renderer)

        # transform to Figure Coordinates
        bbox_bounds = get_bbox_bounds(self.fig.transFigure.inverted().transform(win_ext))
        ax_inset = self.fig.add_axes(bbox_bounds, **kwargs)

        # bbox_bounds = get_bbox_bounds(self.ax.transData.inverted().transform(win_ext))
        # ax_inset = self.ax.inset_axes(bbox_bounds, **kwargs)
        ax_inset.axis(axis)

        return ax_inset


def ax_text(x, y, s, ha='left', va='top',
            highlight_textprops=None,
            textalign='left',
            delim=('<', '>'),
            annotationbbox_kw={},
            ax=None,
            fig=None,
            add_artist=True,
            vpad=0, vsep=4, hpad=0, hsep=0,
            **kwargs):

    """wrapper around the HighlightText Class to continue known hightlight_text nomenclature

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
        vpad (int, optional): external boundary padding of the VPacker (that contains all HPackers) . Defaults to 0.
        vsep (int, optional): vertical seperation between the HighlightRows. Defaults to 4.
        hpad (int, optional): internal boundary padding of the HPackers. Defaults to 0.
        hsep (int, optional): horizontal seperation between a rows TextAreas. Defaults to 0.

    Returns:
        HighlightText
    """

    return HighlightText(x, y, s, ha=ha, va=va,
                         highlight_textprops=highlight_textprops,
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
             textalign='left',
             delim=('<', '>'),
             annotationbbox_kw={},
             ax=None,
             fig=None,
             add_artist=True,
             vpad=0, vsep=4, hpad=0, hsep=0,
             **kwargs):

    """wrapper around the HighlightText Class to continue known hightlight_text nomenclature

    sets the Annotation boxcoords to fig.transFigure

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
        vpad (int, optional): external boundary padding of the VPacker (that contains all HPackers) . Defaults to 0.
        vsep (int, optional): vertical seperation between the HighlightRows. Defaults to 4.
        hpad (int, optional): internal boundary padding of the HPackers. Defaults to 0.
        hsep (int, optional): horizontal seperation between a rows TextAreas. Defaults to 0.

    Returns:
        HighlightText
    """

    if fig is None:
        fig = plt.gcf()

    # set the transform
    annotationbbox_kw.update({'boxcoords': fig.transFigure})

    return HighlightText(x, y, s, ha=ha, va=va,
                         highlight_textprops=highlight_textprops,
                         textalign=textalign,
                         delim=delim,
                         annotationbbox_kw=annotationbbox_kw,
                         ax=ax,
                         fig=fig,
                         add_artist=add_artist,
                         vpad=vpad, vsep=vsep, hpad=hpad, hsep=hsep,
                         **kwargs)
