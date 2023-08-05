#!/usr/bin/env python3
import argparse
import os
import typing as tp

from hsc_instructions.errors import AsmException
from hsc_instructions.instruction import encode_instructions
from hsc_instructions.utilities import exit_open

from hsc_assembler.asm_parser import parse
from hsc_assembler.scanner import scan

Path = tp.Union[str, bytes, os.PathLike]
__all__ = ["assemble", "assemble_file", "cli"]


def assemble(assembly_code: str) -> bytes:
    return encode_instructions(*parse(scan(assembly_code)))


def assemble_file(source: Path, destination: Path) -> None:
    with exit_open(source) as source_file:
        machine_code = assemble(source_file.read())
    with exit_open(destination, "wb") as destination_file:
        destination_file.write(machine_code)


def cli() -> None:
    parser = argparse.ArgumentParser(description="Assembler for the TBD ISA")
    parser.add_argument(
        "source", metavar="source", type=str, help="The path of the source file"
    )
    parser.add_argument(
        "destination",
        metavar="destination",
        type=str,
        help="The path of the destination file",
    )
    args = parser.parse_args()
    try:
        assemble_file(args.source, args.destination)
    except AsmException as exc:
        exc.error_exit()


if __name__ == "__main__":
    cli()
