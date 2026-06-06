import plotly.express as px
import pandas as pd


def points_per_season_chart(season_stats):
    """
    Line chart showing points scored each season.
    """
    df = pd.DataFrame(season_stats)

    fig = px.line(
        df,
        x="season",
        y="points",
        title="Points Per Season",
        markers=True, # shows dots at each data point          
        labels={"season": "Season", "points": "Points"}
    )

    fig.update_traces(line_color="#FF1801")   # F1 red
    fig.update_layout(
        plot_bgcolor="#0F0F0F",
        paper_bgcolor="#0F0F0F",
        font_color="white",
        title_font_size=20
    )

    return fig


def wins_per_season_chart(season_stats):
    """
    Bar chart showing wins each season.
    """
    df = pd.DataFrame(season_stats)

    all_seasons = pd.DataFrame({
        "season": range(df["season"].min(), df["season"].max() + 1)
    })
    df = all_seasons.merge(df, on="season", how="left").fillna(0)
    df["position"] = df["position"].astype(int)
    df["wins"] = df["wins"].astype(int)

    df["label"] = df["position"].apply(lambda x: "🏆" if x == 1 else "")

    fig = px.bar(
        df,
        x="season",
        y="wins",
        title="Wins Per Season",
        text="label", # shows trophy emoji on bars where position is 1
        labels={"season": "Season", "wins": "Wins"}
    )

    fig.update_traces(
        marker_color="#FF1801",
        textposition="outside",        # places text outside/above the bar
        textfont_size=16,
        hovertemplate="<b>Season:</b> %{x}<br><b>Wins:</b> %{y}<extra></extra>"
    )

    fig.update_layout(
        plot_bgcolor="#0F0F0F",
        paper_bgcolor="#0F0F0F",
        font_color="white",
        title_font_size=20,
        uniformtext_minsize=16,
        uniformtext_mode="hide",
        bargap=0.2,
        hoverdistance=30,           # how close cursor needs to be
        hovermode="x unified"       # smoother single tooltip following cursor
    )

    return fig