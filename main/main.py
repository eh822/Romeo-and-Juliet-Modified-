"""
Simple example of building and posting app data to the endpoints.
"""

import os
import csv


import rich_click as click
from rich.progress import Progress

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
        writer.writerow(["Line", "Hash", "Order ID"])

        for ix, line in enumerate(lines):
            print(f"Line no: {ix + 1}: {line}")
            hash_value = build_all_app_codes(graffiti=line)
            print(f"Hash value: {hash_value}")
            writer.writerow([line, hash_value, None])


def update_output_csv_with_order_id(output_path: str, order_id: str, index: int):
    """
    Updates the output CSV file with the order ID.
    """
    temp_path = output_path + ".tmp"
    with (
        open(output_path, "r") as csvfile,
        open(temp_path, "w", newline="") as temp_csvfile,
    ):
        reader = csv.reader(csvfile)
        writer = csv.writer(temp_csvfile)

        header = next(reader)
        writer.writerow(header)

        for ix, row in enumerate(reader):
            if ix == index:
                row[2] = order_id
            writer.writerow(row)

    os.replace(temp_path, output_path)
    print(f"Updated order ID {order_id} at index {index} in {output_path}")


@click.command()
@click.option(
    "--hash_output_path",
    default="output.csv",
    help="Path to the output CSV file (default: output.csv)",
)
def create_play_onchain(
    hash_output_path: str = "output.csv",
):
    """
    Creates the play on-chain by posting the app data as part of an order.
    """
    hashes = []
    with open(hash_output_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for ix, row in enumerate(reader):
            _, hash_value, order_id = row
            if order_id:
                print("Skipping row with existing order ID:", row)
                continue
            hashes.append((ix, hash_value))

    print("Total hashes to post:", len(hashes))
    with Progress() as progress_bar:
        task = progress_bar.add_task("Posting app data", total=len(hashes))
        for index, hash_value in hashes:
            # order_id = swap_tokens(
            #     hash_value=hash_value,
            #     token_in="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
            #     token_out="0x6B175474E89094C44Da98b954EedeAC495271d0F",  # DAI
            #     amount=1e18,  # 1 WETH
            # )
            order_id = "mock_order_id"  # Replace with actual order ID from swap_tokens
            update_output_csv_with_order_id(hash_output_path, order_id, index)
            progress_bar.update(task, advance=1)


cli.add_command(write_play_to_app_data)
cli.add_command(create_play_onchain)


if __name__ == "__main__":
    cli()
