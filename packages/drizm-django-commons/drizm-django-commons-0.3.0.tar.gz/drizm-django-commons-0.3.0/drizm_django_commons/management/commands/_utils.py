from typing import Optional, Union, Tuple
from pathlib import Path


def newlines(amount: Optional[int] = None) -> Union[Tuple[str], str]:
    return tuple(
        "" for _ in range(amount)
    ) if amount is not None else ""


def indent(indents: int, line_contents: str) -> str:
    return "{line_contents: >{width}}".format(
        line_contents=line_contents,
        width=len(line_contents) + (indents*4)
    )


def write_file(base_dir: Path,
               filename: str,
               content: Union[tuple, list]) -> None:
    with (base_dir / filename).open("w") as fout:
        for line in content:
            fout.write(f"{line}\n")
