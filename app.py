from ui.components import create_app

app = create_app()
app.queue().launch()
