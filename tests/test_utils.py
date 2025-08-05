"""
Simple tests for the utils module in the moo package.
"""

import pytest
from main.main import update_output_csv_with_order_id

import os


@pytest.fixture
def tmp_output_hash_file():
    """
    Fixture to create a temporary output CSV file.
    We copy the content from the original output.csv file.
    """
    output_path = "output.csv"
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Expected output file {output_path} does not exist.")

    # Create a temporary file for testing
    temp_path = "temp_output.csv"
    with open(output_path, "r") as original_file, open(temp_path, "w") as temp_file:
        temp_file.write(original_file.read())

    yield temp_path

    os.remove(temp_path)


def test_update_output_csv_with_order_id(tmp_output_hash_file):
    """
    Test the update_output_csv_with_order_id function.
    """
    # Create a temporary CSV file
    order_id = "order123"
    index = 0
    update_output_csv_with_order_id(tmp_output_hash_file, order_id, index)

    # Check if the order ID was updated correctly
    with open(tmp_output_hash_file, "r") as csvfile:
        lines = csvfile.readlines()
        assert len(lines) > 1  # Ensure there is at least a header and one data line
        header = lines[0].strip().split(",")
        assert header == ["Line", "Hash", "Order ID"]

        # Check the first data line for the updated order ID
        first_data_line = lines[1].strip().split(",")
        assert first_data_line[2] == order_id, (
            f"Expected order ID {order_id}, got {first_data_line[2]}"
        )
