from rich.console import Console
from rich.progress import Progress
from rich.table import Table


console = Console()

progress_bar = Progress(
    "[progress.description]{task.description}",
    "[yellow]Completed: {task.completed}",
    "[yellow]Elapsed Time: {task.elapsed:5.1f}s ",
    "[blue]Speed: {task.speed} it/s ",
)

elapsed_time = Progress(
    "[progress.description]{task.description}", "[yellow] {task.elapsed:5.1f}s ",
)


def print_table(df, title):
    table = Table(*[str(col) for col in df.columns], title=title)
    for _, row in df.iterrows():
        table.add_row(*[str(cell) for cell in row])
    console.print(table)
