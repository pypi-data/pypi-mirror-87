"""Command-line interface."""
import typer
from rich.console import Console

from ihsan import __version__
from ihsan.schema import IhsanType
from ihsan.sdl.core import to_sdl
from ihsan.utils import read_adfh_file

app = typer.Typer(help="Ihsan CLI.")


@app.command()
def version() -> None:
    """Show project Version."""
    console = Console()
    project_name = "Ihsan"
    console.print(f"{project_name} Version: {__version__}", style="bold green")


@app.command("sdl")
def sdl(
    file: str,
    output: str = typer.Option(None, help="save output into a file."),
) -> None:
    """Generate SDL aka GraphQL schema from ADFH file.

    Args:
        file: Path to ADFH file.
        output: If --output is used, it will save it in file.
    """
    console = Console()
    data = read_adfh_file(file=file)

    if type(data) == str:
        console.print(data, style="bold red")

    else:
        ihsan_type = IhsanType(**data)  # type: ignore
        sdl_output = to_sdl(schema=ihsan_type)
        if output:
            typer.confirm(
                f"The output will be saved in {output}, are you sure?", abort=True
            )
            with open(output, "w") as output_file:
                output_file.write(sdl_output)
        else:
            console.print(sdl_output, style="bold green")
        console.print(
            "Use -> https://app.graphqleditor.com/ to test the schema :)",
            style="bold blue",
        )


if __name__ == "__main__":  # pragma: no cover
    app()
