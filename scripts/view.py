# + tags=["parameters"]
# add default values for parameters here

# +
import solara

def run(upstream, product):
    @solara.component
    def View():
        with solara.VBox() as main:
            solara.HTML(tag="div", unsafe_innerHTML=open(upstream['plot_map_with_slider']['html']).read())
            solara.Image(source=upstream['plot_line_chart']['img'])
        return main

    @solara.component
    def Controls():
        solara.Button(label="Generate Chart", on_click=lambda: print("Button clicked"), icon_name="mdi-chart-bar")

    @solara.component
    def Page():
        with solara.Sidebar():
            Controls()
        View()

    Page()

if __name__ == "__main__":
    upstream = {
        'plot_map_with_slider': {
            'html': 'data/map.html'
        },
        'plot_line_chart': {
            'img': 'data/line_chart.png'
        }
    }
    product = {
        'nb': 'products/view.ipynb'
    }
    run(upstream, product)

