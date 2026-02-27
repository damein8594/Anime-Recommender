import pandas as pd
import click
from rich.console import Console
from rich.table import Table
import shlex

df = pd.read_csv("anime-dataset-2023.csv")

@click.group()
def cli():
    pass

@cli.command()
@click.argument("genre", nargs=-1)
def genre(genre):
    genre = " ".join(genre)
    df_filtered = df[df["Genres"].str.contains(str(genre), na=False, case=False)]
    df_filtered = df_filtered.copy()
    df_filtered["Score"] = pd.to_numeric(df_filtered["Score"], errors="coerce")
    df_filtered = df_filtered.sort_values("Score", ascending=False)
    df_filtered = df_filtered.head(10)

    console = Console()
    table = Table(title=f"Top 10 {genre} Anime")
    table.add_column("Title", style="cyan")
    table.add_column("Genres", style="green")
    table.add_column("Score", style="yellow")

    for _, row in df_filtered.iterrows():
        table.add_row(
            str(row["English name"]),
            str(row["Genres"]),
            str(row["Score"])
        )

    console.print(table)


@cli.command()
@click.argument("title", nargs=-1)
def title(title):
    title = " ".join(title)
    df_filtered = df[df["English name"].str.contains(str(title), na=False, case=False)].copy()
    df_filtered["Aired"] = pd.to_datetime(df_filtered["Aired"].str.split(" to ").str[0], errors="coerce")
    df_filtered = df_filtered.sort_values("Aired", ascending=True)

    console = Console()
    table = Table(title=f"Results for '{title}'")
    table.add_column("Title", style="cyan")
    table.add_column("Genres", style="green")
    table.add_column("Score", style="yellow")
    table.add_column("Episodes", style="magenta")
    table.add_column("Type", style="blue")

    for _, row in df_filtered.iterrows():
        table.add_row(
            str(row["English name"]) if row["English name"] != "UNKNOWN" else str(row["Name"]),
            str(row["Genres"]),
            str(row["Score"]),
            str(row["Episodes"]),
            str(row["Type"])
        )
    console.print(table)

if __name__ == "__main__":
    while True:
        user_input = input("Enter command: ")
        if user_input == "quit":
            break
        cli(shlex.split(user_input), standalone_mode=False)