
import itertools
import svgwrite
import io

class SVGRenderer:
    """Renders feyn graphs as SVG"""

    def layout_2d(graph):
        # This layout algo moves nodes to the latest layer possible (graphs are wide in the middle)
        lmap = {}
        layers = []
        out = graph[-1]
        layers.insert(0, [out])
        while True:
            layer = []
            for node in layers[0]:
                for ix in reversed(node.sources):
                    if ix!=-1:
                        pred = graph[ix]
                        if pred in lmap:
                            lmap[pred].remove(pred)

                        layer.append(pred)
                        lmap[pred] = layer

            if layer == []:
                break
            layers.insert(0,layer)

        locs = [None]*len(graph)
        for layer, interactions in enumerate(layers):
            sz = len(interactions)
            center = (sz-1) / 2
            for ix, interaction in enumerate(interactions):
                locs[interaction._index] = (layer, ix-center)

        return locs

    def layout_2d_simple(graph):
        # This layout algo moves nodes to the earliest layer possible (graphs are wide towards the beginning)
        layers = [list() for _ in range(graph.depth+2)]

        for node in graph:
            l = node.depth + 1
            layers[l].append(node)

        locs = [None]*len(graph)
        for layer, interactions in enumerate(layers):
            sz = len(interactions)
            center = (sz-1) / 2
            for ix, interaction in enumerate(interactions):
                locs[interaction._index] = (layer, ix-center)

        return locs
    


    @staticmethod
    def rendergraph(graph, label=None):
        from feyn.plots._svg_toolkit import SVGGraphToolkit
        gtk = SVGGraphToolkit()
        gtk.add_graph(graph, label=label)
        return gtk.render()


    @staticmethod
    def old_rendergraph(graph, label=None):
        locs = SVGRenderer.layout_2d(graph)

        # Move y values so the smallest is 0
        min_y = min([loc[1] for loc in locs])
        locs = [(1+loc[0]*120, (loc[1]-min_y)*60+5) for loc in locs]
        
        
        max_x = max([loc[0] for loc in locs])
        max_y = max([loc[1] for loc in locs])

        nodew = 80
        nodeh = 30
        
        h = max_y+nodeh+40
        w = max(max_x+nodew+10, 450)
        drawing = svgwrite.Drawing(
            profile="tiny", 
            size=(w, h)
        )

        for ix, interaction in enumerate(graph):
            loc = locs[ix]
            if interaction.spec.startswith("cell:"):
                color = "#FAFAFA"
                stroke = "#ff1ec8"
            else:
                color = "#00F082"
                stroke = "#808080"

            # The node rect
            rect = drawing.rect(
                (loc[0], loc[1]), 
                (80,30), 
                fill=color, 
                stroke=stroke, 
                stroke_width=1
            )
            tooltip = svgwrite.base.Title(repr(interaction._latticeloc)+"\n"+interaction._tooltip)
            rect.add(tooltip)
            drawing.add(rect)

            # The node text
            l = interaction.name
            if not l:
                l = interaction.spec.split(":")[1].split("(")[0]

            if len(l) > 10:
                l = l[:10]+".."
            txt = drawing.text(l, 
                            insert=(loc[0]+nodew/2, loc[1]+nodeh/2+4), 
                            fill='#202020', 
                            text_anchor="middle", 
                            font_size=11, 
                            font_family="monospace")
            drawing.add(txt)
            
            for ord, src_ix in enumerate(interaction.sources):
                if src_ix == -1:
                    continue

                src_loc = locs[src_ix]
                x0 = src_loc[0]+nodew
                y0 = src_loc[1]+nodeh/2
                    
                x1 = loc[0]
                y1 = loc[1]+nodeh/2
                if len(interaction.sources)==2:
                    y1 += 9-(ord*18)
                    
                # Connecting lines
                line = drawing.line(
                    (x0,y0),(x1, y1), 
                    stroke="#c0c0c0"
                )
                drawing.add(line)

                # The ordinal markers
                txt = drawing.text(f"x{ord}", 
                                insert=(x1+5, y1+3), 
                                fill='#202020', 
                                text_anchor="middle", 
                                font_size=7, 
                                font_family="monospace")
                drawing.add(txt)


        if label:
            txt = drawing.text(label, 
                insert=(0, max_y+nodeh+28), 
                fill='#202020', 
                font_size=12, 
                font_family="monospace")
            drawing.add(txt)
        
        if graph.loss_value is not None:
            loss_label = "Loss: %.2E" % (graph.loss_value)
            loc = locs[-1]
            txt = drawing.text(loss_label, 
                            insert=(loc[0]+nodew/2, loc[1]+1.4*nodeh), 
                            fill='#202020', 
                            text_anchor="middle", 
                            font_size=11, 
                            font_family="monospace")
            drawing.add(txt)

        f = io.StringIO()
        drawing.write(f)
        return f.getvalue()


    @staticmethod
    def renderqgraph(graph):
        """
        Render an entire QGraph.
        """
        raise Exception("Not implemented")

