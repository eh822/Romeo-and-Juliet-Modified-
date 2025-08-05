"""
Simple example of building and posting app data to the endpoints.
"""

import os
import csv


import rich_click as click

from cowdao_cowpy.app_data.utils import build_all_app_codes

@click.group()
def cli():
    """
    CLI for building and posting app data.
    """
    pass

@click.command()
@click.option(
    "--play_path",
    default="Moomeo.txt",
    help="Path to the play file (default: Moomeo.txt)",
)
@click.option(
    "--output_path",
    default="output.csv",
    help="Path to the output CSV file (default: output.csv)",
)
def write_play_to_app_data(
    play_path: str = "Moomeo.txt",
    output_path: str = "output.csv",
):
    """
    Writes the play to the app data.
    """
    lines = []

    with open(play_path, "r") as file:
        for line in file:
            if line.strip() != "":
                lines.append(line.strip())
                print("Line from Moomeo.txt:", line.strip())

    output_path = os.path.abspath(output_path)
    with open(output_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Line", "Hash"])

        for ix, line in enumerate(lines):
            print(f"Line no: {ix + 1}: {line}")
            hash_value = build_all_app_codes(graffiti=line)
            print(f"Hash value: {hash_value}")
            writer.writerow([line, hash_value])





def create_play_onchain(
    output_path: str = "output.csv",
):
    """
    Creates the play on-chain by posting the app data as part of an order.
    """



cli.add_command(write_play_to_app_data)


if __name__ == "__main__":
    cli()
