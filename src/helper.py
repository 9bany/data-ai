import uuid

def with_spinner(task_description: str, fn):
    from rich.progress import Progress, SpinnerColumn, TextColumn
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(task_description, total=None)
        result = fn()
        progress.remove_task(task)
        return result

def gen_hash_name(length: int = 6): 
    return f"db-{uuid.uuid4().hex[:length]}"