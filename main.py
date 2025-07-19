# -*- coding: utf-8 -*-
"""
--- Metadata (Used by UV/Pip/Installer) ---
[package]
name = "countdown"
version = "0.1.0"
dependencies = [
    "click>=8.2.1",
    "rich>=14.0.0",
]
"""
import click
import time
import datetime as dt
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout

c = Console()


@click.command()
@click.argument("times")
def main(times: str) -> None:
    c.print("[green bold]Starting countdown[/]")

    for_time = dt.datetime.strptime(times, "%M:%S").time()
    delta = dt.timedelta(
        minutes=for_time.minute,
        seconds=for_time.second,
    )
    time_start = dt.datetime.now()

    c.print(f"For: {delta}")
    c.print(f"Approximate finish time {time_start + delta}")

    progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    task = progress.add_task("Time elapsed", total=delta.total_seconds())
    panel = Panel.fit(str(delta))

    layout = Layout()
    layout.split_column(
        Layout(
            progress,
            name="progress",
            size=1,
        ),
        Layout(panel, name="countdown", size=5),
        Layout(
            "Press [bold]Ctrl+C[/bold] to exit",
            name="bottom",
            size=1,
        ),
    )
    with Live(layout, auto_refresh=True, refresh_per_second=10) as live:
        while dt.datetime.now() < time_start + delta:
            time_left = (time_start + delta) - dt.datetime.now()
            panel = Panel.fit(
                f"{time_left}",
                title="Countdown",
                title_align="left",
                padding=(1, 4),
                border_style="magenta bold",
            )
            progress.update(
                task,
                completed=delta.total_seconds() - time_left.total_seconds(),
            )
            layout["progress"].update(progress)
            layout["countdown"].update(panel)
            live.update(layout)
            time.sleep(0.1)

    c.print(
        Panel.fit(
            "[magenta bold]TIME's UP!",
            title="Timer finished",
            title_align="left",
            border_style="red bold",
            padding=(2, 5),
        )
    )


if __name__ == "__main__":
    main()
