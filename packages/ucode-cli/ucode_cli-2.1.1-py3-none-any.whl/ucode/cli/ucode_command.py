import typer

app = typer.Typer()


@app.command(name="upload")
def upload_problem_to_ucode(user_name: str):
    typer.echo(f"Creating user: {user_name}")


if __name__ == "__main__":
    app()