import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def ax_text(x, y, s,
            color=None,
            highlight_colors=['C1'],
            highlight_weights=['regular'],
            highlight_styles=['normal'],
            fontweight='regular',
            fontstyle='normal',
            ax=None,
            delim=['<', '>'],
            va='bottom',
            ha='left',
            hpadding=0,
            linespacing=0.25,
            **kwargs):
    '''
    NOTE: do not use plt.tight_layout() after using this
    method as it adjusts the margins and spacing. Better to
    use constrained_layout=True as an arg when you create figure.
    Takes a string with substrings delimiters = ['<', '>']
    to be highlighted according to highlight colors:
    'The weather is <sunny> today. Yesterday it <rained>.',
    color = 'k', highlight_colors = ['yellow', 'grey']
    prints the text with 'sunny' as yellow and 'rained' as grey.

    Make sure to set data limits before using this function.
    Otherwise the data transformation will not show properly.

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
    ax: axes to draw the text onto
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

            for i in range(len(split_text)):
                if i % 2 == 1:
                    colors.append(highlight_colors[highlight_count])
                    weights.append(highlight_weights[highlight_count])
                    styles.append(highlight_styles[highlight_count])
                    highlight_count += 1
                else:
                    colors.append(color)
                    weights.append(fontweight)
                    styles.append(fontstyle)

            texts = []

            for text, color, weight, style in zip(split_text, colors, weights, styles):
                if text != '':
                    texts.append(ax.text(s=text, x=x, y=y, color=color,
                                         fontweight=weight, fontstyle=style,
                                         ha='left', va='top', **kwargs))
            fig.canvas.draw()

            tcboxes = []

            for text in texts:
                # display coordinates
                box = text.get_window_extent()
                # transform back into Data coordinates
                tcboxes.append(ax.transData.inverted().transform(box).ravel())
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


def fig_text(x, y, s,
             color=None,
             highlight_colors=['C1'],
             highlight_weights=['regular'],
             highlight_styles=['normal'],
             fontweight='regular',
             fontstyle='normal',
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
            split_text = sum([substring.split(delim[1]) for substring in text_row.split(delim[0])], [])

            colors = []
            weights = []
            styles = []

            for i in range(len(split_text)):
                if i % 2 == 1:
                    colors.append(highlight_colors[highlight_count])
                    weights.append(highlight_weights[highlight_count])
                    styles.append(highlight_styles[highlight_count])
                    highlight_count += 1
                else:
                    colors.append(color)
                    weights.append(fontweight)
                    styles.append(fontstyle)

            texts = []

            for text, color, weight, style in zip(split_text, colors, weights, styles):
                if text != '':
                    texts.append(fig.text(s=text, x=x, y=y, color=color,
                                 fontweight=weight, fontstyle=style,
                                 ha='left', va='top', **kwargs))
            fig.canvas.draw()

            tcboxes = []

            for text in texts:
                # display coordinates
                box = text.get_window_extent()
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
