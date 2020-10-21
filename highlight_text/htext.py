import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import warnings


def ax_text(x, y, s,
            color=None,
            highlight_colors=['C1'],
            highlight_weights=['regular'],
            highlight_styles=['normal'],
            fontweight='regular',
            fontstyle='normal',
            path_effect_kws=None,
            bbox_kws=None,
            ax=None,
            delim=['<', '>'],
            va='bottom',
            ha='left',
            hpadding=0,
            linespacing=0.25,
            **kwargs):
    '''
    NOTE: Make sure to do all plotting and setting of axes limits
    BEFORE using ax_text.
    Specifically do not use plt.tight_layout() after using this
    method as it adjusts the margins and spacing.
    Better to use constrained_layout=True as an arg when you create figure.

    Takes a string with substrings delimiters = ['<', '>']
    to be highlighted according to highlight colors:
    'The weather is <sunny> today. Yesterday it <rained>.',
    color = 'k', highlight_colors = ['yellow', 'grey']
    prints the text with 'sunny' as yellow and 'rained' as grey.

    Parameters:
    ##########

    s: text including <highlighted substrings>
    x: x position with left alignment
    y: y position
    color: textcolor of unhighlighted text
    highlight_colors: list of highlight colors
    highlight_weights = ['regular']: the fontweight used for highlighted text
    highlight_styles = ['normal']: the fontstyle used for highlighted text
    fontweight = 'regular': the fontweight used for normal text
    fontstyle = 'normal': the fontstyle used for normal text
    path_effect_kws = None: list of dicts of 'linewidth' and 'foreground' or None for a path_effects.Stroke()
                            for each highlighted subtext, or one dict applied to all highlighted subtexts
    bbox_kws = None: list of dicts of 'alpha', 'boxstyle', 'edgecolor', 'facecolor', 'linewidth' and 'pad'
                     or None for plt.text bbox props for each highlighted subtext,
                     or one dict applied to all highlighted subtexts
    ax: axes to draw the text onto
    delim = ['<', '>']: delimiters to enclose the highlight substrings
    va = 'bottom', textalignment has to be in ['bottom', 'top', 'center']
    ha = 'left', textalignment has to be in ['left', 'right', 'center']
    hpadding = 0: extra padding between highlight and normal text
    linespacing = 0.25: linespacing in factor of font height between rows
    **kwargs: ax.text kwargs for all text

    Returns:
    ##########

    a list of texts
    '''

    if color is None:
        color = mpl.rcParams['text.color']

    def is_empty_string(string):
        return string.strip() == ''

    if ax is None:
        ax = plt.gca()
    fig = plt.gcf()

    if type(highlight_colors) == str:
        highlight_colors = [highlight_colors]
    if type(highlight_weights) == str:
        highlight_weights = [highlight_weights]
    if type(highlight_styles) == str:
        highlight_styles = [highlight_styles]

    n_highlights = s.count(delim[0])

    assert n_highlights == s.count(delim[1]), f"You didn't specify the same number of delim[0] '{delim[0]}': {(n_highlights)} as delim[1] '{delim[1]}': {s.count(delim[1])}."

    if len(highlight_colors) == 1:
        highlight_colors = np.repeat(highlight_colors, n_highlights)
    else:
        assert n_highlights == len(highlight_colors), f'You should specify either one highlight color or the same number as text highlights.\nYou input {n_highlights} highlights and {len(highlight_colors)} colors.'

    if len(highlight_weights) == 1:
        highlight_weights = np.repeat(highlight_weights, n_highlights)
    else:
        assert n_highlights == len(highlight_weights), f'You should specify either one highlight weight or the same number as text highlights.\nYou input {n_highlights} highlights and {len(highlight_weights)} weights.'

    if len(highlight_styles) == 1:
        highlight_styles = np.repeat(highlight_styles, n_highlights)
    else:
        assert n_highlights == len(highlight_styles), f'You should specify either one highlight style or the same number as text highlights.\nYou input {n_highlights} highlights and {len(highlight_styles)} styles.'

    if type(path_effect_kws) == list:
        if len(path_effect_kws) == 1:
            path_effect_kws = path_effect_kws[0]

    if (path_effect_kws is None) | (type(path_effect_kws) == dict):
        path_effect_kws = np.repeat([path_effect_kws], n_highlights)
    else:
        assert n_highlights == len(path_effect_kws), f'You should specify either one path_effect_kws dict or the same number as text highlights.\nYou input {n_highlights} highlights and {len(path_effect_kws)} styles.'            

    if type(bbox_kws) == list:
        if len(bbox_kws) == 1:
            bbox_kws = bbox_kws[0]

    if (bbox_kws is None) | (type(bbox_kws) == dict):
        bbox_kws = np.repeat([bbox_kws], n_highlights)
    else:
        assert n_highlights == len(bbox_kws), f'You should specify either one bbox_kws dict or the same number as text highlights.\nYou input {n_highlights} highlights and {len(bbox_kws)} styles.'            

    assert va in ['top', 'bottom', 'center'], "Specify either 'top', 'bottom' or 'center' for va"
    assert ha in ['left', 'right', 'center'], "Specify either 'left', 'right' or 'center' for ha"

    text_rows = s.split('\n')

    while is_empty_string(text_rows[0]):
        text_rows = text_rows[1:]

    textline_height = 0
    textline_widths = []
    textline_xs = []
    row_texts = []
    highlight_count = 0
    text_in_axes_bounds = True

    for text_row in text_rows:
        if is_empty_string(text_row):
            # set next lines y
            y = y - textline_height * (1 + linespacing)
        else:
            split_text = sum([substring.split(delim[1])
                              for substring in text_row.split(delim[0])], [])

            colors = []
            weights = []
            styles = []
            pe_linewidths = []
            pe_foregrounds = []
            bbox_edgecolors = []
            bbox_facecolors = []
            bbox_alphas = []
            bbox_boxstyles = []
            bbox_linewidths = []
            bbox_pads = []

            for i in range(len(split_text)):
                if i % 2 == 1:
                    colors.append(highlight_colors[highlight_count])
                    weights.append(highlight_weights[highlight_count])
                    styles.append(highlight_styles[highlight_count])

                    if path_effect_kws[highlight_count] is not None:
                        pe_linewidths.append(path_effect_kws[highlight_count].pop('linewidth', 1))
                        pe_foregrounds.append(path_effect_kws[highlight_count].pop('foreground', ax.get_facecolor()))
                    else:
                        pe_linewidths.append(None)
                        pe_foregrounds.append(None)

                    if bbox_kws[highlight_count] is not None:
                        if 'edgecolor' in bbox_kws[highlight_count].keys():
                            bbox_edgecolors.append(bbox_kws[highlight_count]['edgecolor'])
                        else:
                            bbox_edgecolors.append('None')
                        if 'facecolor' in bbox_kws[highlight_count].keys():
                            bbox_facecolors.append(bbox_kws[highlight_count]['facecolor'])
                        else:
                            bbox_facecolors.append('None')
                        if 'alpha' in bbox_kws[highlight_count].keys():
                            bbox_alphas.append(bbox_kws[highlight_count]['alpha'])
                        else:
                            bbox_alphas.append(None)
                        if 'boxstyle' in bbox_kws[highlight_count].keys():
                            bbox_boxstyles.append(bbox_kws[highlight_count]['boxstyle'])
                        else:
                            bbox_boxstyles.append(None)
                        if 'linewidth' in bbox_kws[highlight_count].keys():
                            bbox_linewidths.append(bbox_kws[highlight_count]['linewidth'])
                        else:
                            bbox_linewidths.append(1)
                        if 'pad' in bbox_kws[highlight_count].keys():
                            bbox_pads.append(bbox_kws[highlight_count]['pad'])
                        else:
                            bbox_pads.append(0.3)
                    else:
                        bbox_edgecolors.append('None')
                        bbox_facecolors.append('None')
                        bbox_alphas.append(None)
                        bbox_boxstyles.append(None)
                        bbox_linewidths.append(None)
                        bbox_pads.append(None)
                    highlight_count += 1
                else:
                    colors.append(color)
                    weights.append(fontweight)
                    styles.append(fontstyle)
                    pe_linewidths.append(None)
                    pe_foregrounds.append(None)
                    bbox_edgecolors.append('None')
                    bbox_facecolors.append('None')
                    bbox_alphas.append(None)
                    bbox_boxstyles.append(None)
                    bbox_linewidths.append(None)
                    bbox_pads.append(None)

            texts = []

            for text, color, weight, style, pe_linewidth, pe_foreground, bbox_edgecolor, bbox_facecolor, bbox_alpha, bbox_boxstyle, bbox_linewidth, bbox_pad\
                in zip(split_text, colors, weights, styles, pe_linewidths, pe_foregrounds,
                       bbox_edgecolors, bbox_facecolors, bbox_alphas, bbox_boxstyles, bbox_linewidths, bbox_pads):
                if text != '':
                    if not all((item is None) | (item == 'None') for item in [bbox_edgecolor, bbox_facecolor, bbox_alpha, bbox_boxstyle, bbox_linewidth, bbox_pad]):
                        bbox_dict = dict(edgecolor=bbox_edgecolor,
                                         facecolor=bbox_facecolor,
                                         alpha=bbox_alpha,
                                         boxstyle=bbox_boxstyle,
                                         linewidth=bbox_linewidth,
                                         pad=bbox_pad)
                    else:
                        bbox_dict = None

                    text_ = ax.text(s=text, x=x, y=y, color=color,
                                    fontweight=weight,
                                    fontstyle=style,
                                    bbox=bbox_dict,
                                    ha='left', va='top', **kwargs)

                    if (pe_linewidth is not None) | (pe_foreground is not None):

                        if pe_linewidth is None:
                            pe_linewidth = 1
                        if pe_linewidth is None:
                            pe_foreground = plt.gcf().get_facecolor()

                        text_.set_path_effects([path_effects.Stroke(linewidth=pe_linewidth,
                                               foreground=pe_foreground),
                                               path_effects.Normal()])
                    texts.append(text_)

            fig.canvas.draw()

            tcboxes = []

            for text in texts:
                # display coordinates
                box = text.get_window_extent(renderer=fig.canvas.get_renderer())
                # transform back into Data coordinates
                tcboxes.append(ax.transData.inverted().transform(box).ravel())
            tcboxes = np.stack(tcboxes)

            textline_height = tcboxes[0, -1] - tcboxes[0, 1]
            textline_widths.append((tcboxes[:, 2] - tcboxes[:, 0]).sum())
            textbox_height = ((tcboxes[0, -1] - tcboxes[0, 1]) * (len(text_rows)
                              + (len(text_rows) - 1) * linespacing))

            textline_xs.append(np.hstack([tcboxes[0, 0],
                                          tcboxes[0, 0]
                                          + np.cumsum(tcboxes[:-1, 2] - tcboxes[:-1, 0])
                                          + np.cumsum((len(tcboxes)-1)*[hpadding])]))

            if va == 'bottom':
                for text in texts:
                    text.set_y(y + textbox_height)

            elif va == 'center':
                for text in texts:
                    text.set_y(y + 0.5 * textbox_height)

            y = tcboxes[0, 1] - textline_height * linespacing

            row_texts.append(texts)

    for xs, textline_width, texts in zip(textline_xs,
                                         textline_widths,
                                         row_texts):
        if ha == 'center':
            adjust = -0.5 * textline_width
        elif ha == 'right':
            adjust = -textline_width
        else:
            adjust = 0

        xs = xs + adjust

        for x_, text in zip(xs, texts):
            text.set_x(x_)

        # check if texts overflow axes boundary
        if (
            ((texts[0].get_position()[0] + textline_width) > 1) |
            ((texts[0].get_position()[1] + textline_height) > 1) |
            (texts[0].get_position()[0] < 0) |
            (texts[0].get_position()[1] < 0)
           ):
            text_in_axes_bounds = False

    if text_in_axes_bounds is False:
        warnings.warn(f'The text is reaching outside the axes boundary. '
                      'This can result in unwanted behavior for ax_text. '
                      'You can try increasing the figure or axes size, or use fig_text instead. '
                      'If the text does not overspill the figure boundary, you can also set the '
                      'ax.text **kwarg in_layout=False.')

    return row_texts


def fig_text(x, y, s,
             color=None,
             highlight_colors=['C1'],
             highlight_weights=['regular'],
             highlight_styles=['normal'],
             fontweight='regular',
             fontstyle='normal',
             path_effect_kws=None,
             bbox_kws=None,
             fig=None,
             delim=['<', '>'],
             va='bottom',
             ha='left',
             hpadding=0,
             linespacing=0.25,
             **kwargs):
    '''
    Takes a string with substrings in delimiters = ['<', '>']
    to be highlighted according to highlight colors:
    'The weather is <sunny> today. Yesterday it <rained>.',
    color = 'w', highlight_colors = ['yellow', 'grey']
    prints the text in white with 'sunny' as yellow and 'rained' as grey.

    Parameters:
    ##########

    s: text including <highlighted substrings>
    x: x position with left alignment
    y: y position
    color: textcolor of unhighlighted text
    highlight_colors: list of highlight colors
    highlight_weights = ['regular']: the fontweight used for highlighted text
    highlight_styles = ['normal']: the fontstyle used for highlighted text
    fontweight = 'regular': the fontweight used for normal text
    fontstyle = 'normal': the fontstyle used for normal text
    path_effect_kws = None: list of dicts of 'linewidth' and 'foreground' or None for a path_effects.Stroke()
                            for each highlighted subtext, or one dict applied to all highlighted subtexts
    bbox_kws = None: list of dicts of 'alpha', 'boxstyle', 'edgecolor', 'facecolor', 'linewidth' and 'pad'
                     or None for plt.text bbox props for each highlighted subtext,
                     or one dict applied to all highlighted subtexts
    delim = ['<', '>']: delimiters to enclose the highlight substrings
    va = 'bottom', textalignment has to be in ['bottom', 'top', 'center']
    ha = 'left', textalignment has to be in ['left', 'right', 'center']
    hpadding = 0: extra padding between highlight and normal text
    linespacing = 0.25: linespacing in factor of font height between rows
    **kwargs: figure.text kwargs for all text

    Returns:
    ##########

    a list of texts
    '''

    if color is None:
        color = mpl.rcParams['text.color']

    def is_empty_string(string):
        return string.strip() == ''

    if fig is None:
        fig = plt.gcf()

    if type(highlight_colors) == str:
        highlight_colors = [highlight_colors]
    if type(highlight_weights) == str:
        highlight_weights = [highlight_weights]
    if type(highlight_styles) == str:
        highlight_styles = [highlight_styles]

    n_highlights = s.count(delim[0])

    assert n_highlights == s.count(delim[1]), f"You didn't specify the same number of delim[0] '{delim[0]}': {(n_highlights)} as delim[1] '{delim[1]}': {s.count(delim[1])}."

    if len(highlight_colors) == 1:
        highlight_colors = np.repeat(highlight_colors, n_highlights)
    else:
        assert n_highlights == len(highlight_colors), f'You should specify either one highlight color or the same number as text highlights.\nYou input {n_highlights} highlights and {len(highlight_colors)} colors.'

    if len(highlight_weights) == 1:
        highlight_weights = np.repeat(highlight_weights, n_highlights)
    else:
        assert n_highlights == len(highlight_weights), f'You should specify either one highlight weight or the same number as text highlights.\nYou input {n_highlights} highlights and {len(highlight_weights)} weights.'

    if len(highlight_styles) == 1:
        highlight_styles = np.repeat(highlight_styles, n_highlights)
    else:
        assert n_highlights == len(highlight_styles), f'You should specify either one highlight style or the same number as text highlights.\nYou input {n_highlights} highlights and {len(highlight_styles)} styles.'

    if type(path_effect_kws) == list:
        if len(path_effect_kws) == 1:
            path_effect_kws = path_effect_kws[0]

    if (path_effect_kws is None) | (type(path_effect_kws) == dict):
        path_effect_kws = np.repeat([path_effect_kws], n_highlights)
    else:
        assert n_highlights == len(path_effect_kws), f'You should specify either one path_effect_kws dict or the same number as text highlights.\nYou input {n_highlights} highlights and {len(path_effect_kws)} styles.'            

    if type(bbox_kws) == list:
        if len(bbox_kws) == 1:
            bbox_kws = bbox_kws[0]

    if (bbox_kws is None) | (type(bbox_kws) == dict):
        bbox_kws = np.repeat([bbox_kws], n_highlights)
    else:
        assert n_highlights == len(bbox_kws), f'You should specify either one bbox_kws dict or the same number as text highlights.\nYou input {n_highlights} highlights and {len(bbox_kws)} styles.'            

    assert va in ['top', 'bottom', 'center'], "Specify either 'top', 'bottom' or 'center' for va"
    assert ha in ['left', 'right', 'center'], "Specify either 'left', 'right' or 'center' for ha"

    text_rows = s.split('\n')

    while is_empty_string(text_rows[0]):
        text_rows = text_rows[1:]

    textline_hight = 0
    textline_widths = []
    textline_xs = []
    row_texts = []
    highlight_count = 0

    for text_row in text_rows:
        if is_empty_string(text_row):
            # set next lines y
            y = y - textline_hight * (1 + linespacing)
        else:
            split_text = sum([substring.split(delim[1])
                              for substring in text_row.split(delim[0])], [])

            colors = []
            weights = []
            styles = []
            pe_linewidths = []
            pe_foregrounds = []
            bbox_edgecolors = []
            bbox_facecolors = []
            bbox_alphas = []
            bbox_boxstyles = []
            bbox_linewidths = []
            bbox_pads = []

            for i in range(len(split_text)):
                if i % 2 == 1:
                    colors.append(highlight_colors[highlight_count])
                    weights.append(highlight_weights[highlight_count])
                    styles.append(highlight_styles[highlight_count])

                    if path_effect_kws[highlight_count] is not None:
                        pe_linewidths.append(path_effect_kws[highlight_count].pop('linewidth', 1))
                        pe_foregrounds.append(path_effect_kws[highlight_count].pop('foreground', fig.get_facecolor()))
                    else:
                        pe_linewidths.append(None)
                        pe_foregrounds.append(None)

                    if bbox_kws[highlight_count] is not None:
                        if 'edgecolor' in bbox_kws[highlight_count].keys():
                            bbox_edgecolors.append(bbox_kws[highlight_count]['edgecolor'])
                        else:
                            bbox_edgecolors.append('None')
                        if 'facecolor' in bbox_kws[highlight_count].keys():
                            bbox_facecolors.append(bbox_kws[highlight_count]['facecolor'])
                        else:
                            bbox_facecolors.append('None')
                        if 'alpha' in bbox_kws[highlight_count].keys():
                            bbox_alphas.append(bbox_kws[highlight_count]['alpha'])
                        else:
                            bbox_alphas.append(None)
                        if 'boxstyle' in bbox_kws[highlight_count].keys():
                            bbox_boxstyles.append(bbox_kws[highlight_count]['boxstyle'])
                        else:
                            bbox_boxstyles.append(None)
                        if 'linewidth' in bbox_kws[highlight_count].keys():
                            bbox_linewidths.append(bbox_kws[highlight_count]['linewidth'])
                        else:
                            bbox_linewidths.append(1)
                        if 'pad' in bbox_kws[highlight_count].keys():
                            bbox_pads.append(bbox_kws[highlight_count]['pad'])
                        else:
                            bbox_pads.append(0.3)
                    else:
                        bbox_edgecolors.append('None')
                        bbox_facecolors.append('None')
                        bbox_alphas.append(None)
                        bbox_boxstyles.append(None)
                        bbox_linewidths.append(None)
                        bbox_pads.append(None)
                    highlight_count += 1
                else:
                    colors.append(color)
                    weights.append(fontweight)
                    styles.append(fontstyle)
                    pe_linewidths.append(None)
                    pe_foregrounds.append(None)
                    bbox_edgecolors.append('None')
                    bbox_facecolors.append('None')
                    bbox_alphas.append(None)
                    bbox_boxstyles.append(None)
                    bbox_linewidths.append(None)
                    bbox_pads.append(None)

            texts = []

            for text, color, weight, style, pe_linewidth, pe_foreground, bbox_edgecolor, bbox_facecolor, bbox_alpha, bbox_boxstyle, bbox_linewidth, bbox_pad\
                in zip(split_text, colors, weights, styles, pe_linewidths, pe_foregrounds,
                       bbox_edgecolors, bbox_facecolors, bbox_alphas, bbox_boxstyles, bbox_linewidths, bbox_pads):
                if text != '':
                    if not all((item is None) | (item == 'None') for item in [bbox_edgecolor, bbox_facecolor, bbox_alpha, bbox_boxstyle, bbox_linewidth, bbox_pad]):
                        bbox_dict = dict(edgecolor=bbox_edgecolor,
                                         facecolor=bbox_facecolor,
                                         alpha=bbox_alpha,
                                         boxstyle=bbox_boxstyle,
                                         linewidth=bbox_linewidth,
                                         pad=bbox_pad)
                    else:
                        bbox_dict = None

                    text_ = fig.text(s=text, x=x, y=y, color=color,
                                     fontweight=weight,
                                     fontstyle=style,
                                     bbox=bbox_dict,
                                     ha='left', va='top', **kwargs)

                    if (pe_linewidth is not None) | (pe_foreground is not None):

                        if pe_linewidth is None:
                            pe_linewidth = 1
                        if pe_linewidth is None:
                            pe_foreground = plt.gcf().get_facecolor()

                        text_.set_path_effects([path_effects.Stroke(linewidth=pe_linewidth,
                                                foreground=pe_foreground),
                                                path_effects.Normal()])
                    texts.append(text_)

            fig.canvas.draw()

            tcboxes = []

            for text in texts:
                # display coordinates
                box = text.get_window_extent(renderer=fig.canvas.get_renderer())
                # transform back into Data coordinates
                tcboxes.append(fig.transFigure.inverted().transform(box).ravel())
            tcboxes = np.stack(tcboxes)

            textline_hight = tcboxes[0, -1] - tcboxes[0, 1]
            textline_widths.append((tcboxes[:, 2] - tcboxes[:, 0]).sum())
            textbox_hight = ((tcboxes[0, -1] - tcboxes[0, 1]) * (len(text_rows)
                             + (len(text_rows) - 1) * linespacing))

            textline_xs.append(np.hstack([tcboxes[0, 0],
                                          tcboxes[0, 0]
                                          + np.cumsum(tcboxes[:-1, 2] - tcboxes[:-1, 0])
                                          + np.cumsum((len(tcboxes)-1)*[hpadding])]))

            if va == 'bottom':
                for text in texts:
                    text.set_y(y + textbox_hight)

            elif va == 'center':
                for text in texts:
                    text.set_y(y + 0.5 * textbox_hight)

            y = tcboxes[0, 1] - textline_hight * linespacing

            row_texts.append(texts)

    for xs, textline_width, texts in zip(textline_xs,
                                         textline_widths,
                                         row_texts):
        if ha == 'center':
            adjust = -0.5 * textline_width
        elif ha == 'right':
            adjust = -textline_width
        else:
            adjust = 0

        xs = xs + adjust

        for x_, text in zip(xs, texts):
            text.set_x(x_)

    return row_texts
