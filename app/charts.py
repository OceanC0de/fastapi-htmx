# app/charts.py
import plotly.graph_objects as go

def make_chart(x_data: list, y_data: list, ticker_symbol="", line_color="rgba(42, 157, 143, 0.7)", x_axis_title="", y_axis_title=""):
    fig = go.Figure(data=go.Scatter(x=x_data, y=y_data))
    fig.update_traces(line=dict(color=line_color))
    
    fig.update_xaxes(
        showgrid=False,
        showticklabels=True,
        showline=False,
        zeroline=False,
        title=x_axis_title,
        title_font=dict(color="rgba(255, 255, 255, 0.7)"),
        tickfont=dict(color="rgba(255, 255, 255, 0.4)"),
    )
    
    fig.update_yaxes(
        showgrid=False,
        showticklabels=True,
        showline=False,
        zeroline=False,
        title=y_axis_title,
        title_font=dict(color="rgba(255, 255, 255, 0.7)"),
        tickfont=dict(color="rgba(255, 255, 255, 0.4)"),
    )
    
    fig.update_layout(
        clickmode="none",
        hovermode=False,
        dragmode=False,
        selectdirection=None,
        showlegend=False,
        autosize=True,
        title=ticker_symbol,
        title_font=dict(color="rgba(255, 255, 255, 0.7)"),
        plot_bgcolor="#1f1f1f",  # Set plot background color to match container background
        paper_bgcolor="#1f1f1f",  # Set paper background color to match container background
        font=dict(color="white"),
        margin=dict(l=0, r=0, t=30, b=0),
        modebar_remove=['zoom', 'pan', 'lasso', 'select', 'zoomin', 'zoomout', 'autoscale', 'resetScale2d']
    )
    
    html = fig.to_html(include_plotlyjs=False, full_html=False, config=dict(displaylogo=False))
    return html