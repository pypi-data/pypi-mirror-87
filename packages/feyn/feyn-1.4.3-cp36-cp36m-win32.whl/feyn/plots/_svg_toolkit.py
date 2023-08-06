import itertools
import svgwrite
import io
import numpy as np
import matplotlib.colors as clr

from feyn import SVGRenderer
from ._themes import Theme


class RenderState():
    def __init__(self):
        self.x_loc = 0
        self.y_loc = 0
        self.heights = [0]
        self.widths = [0]

    def wrap(self):
        self.x_loc = 0
        self.y_loc = self.y_loc + self.current_row_height()
        self.heights = [0]

    def update_xloc(self, x):
        self.x_loc += x
        self.widths.append(self.x_loc)

    def update_height(self, y):
        self.heights.append(y)

    def current_row_height(self):
        return max(self.heights)

    def abs_max_width(self):
        return max(self.widths)


class SVGGraphToolkit():

    def __init__(self, auto_wrap_px=None):
        self.nodew = 90
        self.nodeh = 35
        self.margin = 20
        self.node_margin = 2

        self.auto_wrap_px = auto_wrap_px

        self.drawing = svgwrite.Drawing(
            profile="full"
        )

        self.render_items = []

    def _repr_svg_(self):
        return self.render()

    def _repr_html_(self):
        return self.render()

    def render(self):
        drawing = svgwrite.Drawing(
            profile="full",
            size=(0, 0)
        )

        state = RenderState()

        for item in self.render_items.copy():
            item_width = item.attribs['width']
            item_height = item.attribs['height']

            if item.attribs['class'] == 'h_space':
                state.wrap()
            elif self.auto_wrap_px is not None:
                # If item is not already the first and the total is larger than max, wrap
                if state.x_loc > 0 and state.x_loc + item_width >= self.auto_wrap_px:
                    state.wrap()

            # Reposition the svg element w.r.t. state
            item.attribs['x'] = state.x_loc
            item.attribs['y'] = state.y_loc

            # TODO: Consider adding dynamic spacer objects
            drawing.add(item)
            state.update_xloc(item_width)
            state.update_height(item_height)

            if item.attribs['class'] == 'h_space':
                state.wrap()

        f = io.StringIO()

        colorbar_correction = 5  # Sometimes the colorbar gets a little wonky.

        drawing.attribs['height'] = state.y_loc + state.current_row_height() + colorbar_correction
        drawing.attribs['width'] = state.abs_max_width()
        drawing.write(f)
        return f.getvalue()

    def _add_txt(self, parent, content, insert, color='dark', font_size='medium', anchor='start'):
        txt = self.drawing.text(content,
                                insert=insert,
                                fill=Theme.color(color),
                                text_anchor=anchor,
                                font_size=Theme.font_size(font_size),
                                font_family="monospace")
        parent.add(txt)

    def add_horizontal_spacer(self, title=""):
        font_size = Theme.font_size('large')
        title_spacing = self.margin + font_size + 5
        font_width_ratio = 0.6
        t_width = len(title) * font_size * font_width_ratio + self.margin*4

        spacer = self.drawing.svg(insert=(0, 0), size=(t_width,  title_spacing))
        spacer.attribs['class'] = 'h_space'
        self._add_txt(spacer, title,
                      insert=(self.margin*2, self.margin + font_size),
                      font_size=font_size)

        line = self.drawing.line(start=(0, title_spacing), end=(t_width, title_spacing), stroke=Theme.color('dark'))
        spacer.add(line)

        self.render_items.append(spacer)
        return self

    def add_summary_information(self, metrics, title=""):
        summaryw = 160
        font_size = Theme.font_size('large')
        text_spacing = font_size + 1
        title_spacing = font_size + 5
        summaryh = len(metrics) * text_spacing + title_spacing

        text_margin = 5

        summary = self.drawing.svg(insert=(0, 0), size=(summaryw+self.margin, summaryh))
        summary.attribs['class'] = 'summary'
        self._add_txt(summary, title,
                      insert=(0, font_size),
                      font_size=font_size)
        line = self.drawing.line(start=(0, title_spacing), end=(summaryw, title_spacing), stroke=Theme.color('dark'))
        summary.add(line)

        # Draw summary information in rectangle
        m_ix = 0
        for name, metric in metrics.items():
            m_ix += 1  # 1 indexed for pixel reasons
            self._add_txt(summary, name,
                          insert=(text_margin, title_spacing + text_spacing * (m_ix)),
                          font_size=font_size)
            self._add_txt(summary, "{:.3}".format(metric),
                          insert=(summaryw - text_margin, title_spacing + text_spacing * (m_ix)),
                          font_size=font_size,
                          anchor='end')

        self.render_items.append(summary)
        return self

    @staticmethod
    def _get_node_color(graph, ix, node_signal=None):
        if node_signal is None:
            if graph[ix].spec.startswith("cell:"):
                return Theme.color('light'), Theme.color('accent')
            else:
                return Theme.color('primary'), Theme.color('dark')

        gradient = Theme.gradient()
        cmap = clr.LinearSegmentedColormap.from_list('random',
                                                [(0,   gradient[0][1]),
                                                (0.5, gradient[1][1]),
                                                (1,   gradient[2][1])], N=256)

        norm = clr.Normalize(vmin=min(node_signal),
                             vmax=max(node_signal))
        return clr.rgb2hex(cmap(norm(node_signal[ix]))[:3]), Theme.color('dark')

    def _add_signal_colorbar(self, svg):
        bar_w = 50
        bar_h = 20
        svg.attribs['height'] += bar_h  # Add offset
        w = svg.attribs['width']
        h = svg.attribs['height']
        colorbar_loc = (w/2-bar_w*1.5, h-bar_h)

        gradient = Theme.gradient()
        for i in range(len(gradient)):
            color = gradient[i][1]
            signal_name = gradient[i][0]

            # The node rect
            rect = self.drawing.rect(
                (colorbar_loc[0]+i*bar_w, colorbar_loc[1]),
                (bar_w,bar_h),
                fill=color,
                stroke_width=1
            )
            svg.add(rect)

            # Text on signal
            self._add_txt(svg, signal_name,
                          insert=(colorbar_loc[0]+i*bar_w+bar_w/2, colorbar_loc[1]+bar_h/2+3),
                          anchor='middle')

        self._add_txt(svg, "Signal capture",
                      insert=(colorbar_loc[0]+bar_w*1.5, colorbar_loc[1]-5),
                      anchor='middle')

        return self

    def _add_node_signal_markers(self, locs, node_signal, svg):
        for ix, loc in enumerate(locs):
            # The mutual information markers
            self._add_txt(svg, np.round(node_signal[ix], 2),
                          insert=(loc[0] + self.nodew/2, loc[1] - 5),
                          anchor="middle",
                          font_size='small')

        return self

    def _add_loss_value(self, graph, locs, svg):
        if graph.loss_value is not None:
            loss_label = "Loss: %.2E" % (graph.loss_value)
            loc = locs[-1]
            self._add_txt(svg,
                          loss_label,
                          insert=(loc[0]+self.nodew/2, loc[1]+1.4*self.nodeh),
                          anchor="middle")
        return self

    def _add_label(self, label, height, svg):
        if label:
            label_margin = self.margin - 10
            self._add_txt(svg,
                          label,
                          insert=(0, height - label_margin))
        return self

    def add_graph(self, graph, node_signal=None, label=None):
        locs = SVGRenderer.layout_2d(graph)

        # Move y values so the smallest is 0
        min_y = min([loc[1] for loc in locs])
        locs = [(1+loc[0]*120, (loc[1]-min_y)*60+20) for loc in locs]  # Magic numbers

        max_x = max([loc[0] for loc in locs])
        max_y = max([loc[1] for loc in locs])
        width = max(max_x+self.nodew+self.margin, 450)  # max to accomodate space for label
        height = max_y+self.nodeh+self.margin*2

        graph_svg = self.drawing.svg(insert=(0,0), size=(width, height))
        graph_svg.attribs['class'] = 'graph'

        if np.any(node_signal):
            self._add_signal_colorbar(graph_svg)
            self._add_node_signal_markers(locs, node_signal, graph_svg)
        else:
            self._add_loss_value(graph, locs, graph_svg)
            if label:
                self._add_label(label, height, graph_svg)

        for ix, interaction in enumerate(graph):
            loc = locs[ix]

            fill, stroke = self._get_node_color(graph, ix, node_signal=node_signal)

            # The node rect + tooltip
            rect = self.drawing.rect(
                (loc[0], loc[1]),
                (self.nodew, self.nodeh),
                fill=fill,
                stroke=stroke,
                stroke_width=1
            )
            tooltip = svgwrite.base.Title(repr(interaction._latticeloc)+"\n"+interaction._tooltip)
            rect.add(tooltip)
            graph_svg.add(rect)

            # The node text
            trunc_name = interaction.name
            if not trunc_name:
                trunc_name = interaction.spec.split(":")[1].split("(")[0]

            if len(trunc_name) > 8:
                trunc_name = trunc_name[:8]+".."

            self._add_txt(graph_svg, trunc_name,
                          insert=(loc[0] + self.nodew/2, loc[1] + self.nodeh/2 + 4),
                          anchor='middle')

            # The index markers
            self._add_txt(graph_svg, interaction._index,
                          insert=(loc[0] + self.nodew - self.node_margin, loc[1] + 9),
                          anchor='end',
                          font_size='small')

            # The type text
            interaction_type = interaction.name
            if not interaction_type:
                interaction_type = ""
            if interaction.spec.startswith("in:cat"):
                interaction_type = "cat"
            elif interaction.spec.startswith("in:lin"):
                interaction_type = "num"
            elif interaction.spec.startswith("out"):
                interaction_type = "out"

            self._add_txt(graph_svg, interaction_type,
                          insert=(loc[0] + self.node_margin, loc[1]+9),
                          font_size='small')

            for ord, src_ix in enumerate(interaction.sources):
                if src_ix == -1:
                    continue

                src_loc = locs[src_ix]
                x0 = src_loc[0] + self.nodew
                y0 = src_loc[1] + self.nodeh/2

                x1 = loc[0]
                y1 = loc[1] + self.nodeh/2
                if len(interaction.sources) == 2:
                    y1 += 9-(ord*18)

                # Connecting lines
                line = self.drawing.line(
                    (x0, y0), (x1, y1),
                    stroke=Theme.color('dark')
                )
                graph_svg.add(line)

                if interaction.spec.startswith("out"):
                    continue

                # The ordinal markers
                self._add_txt(graph_svg, f"x{ord}",
                              insert=(x1 + self.node_margin, y1 + 3),
                              font_size='small')

        self.render_items.append(graph_svg)
        return self
