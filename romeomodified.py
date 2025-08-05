"""
Simple example of building and posting app data to the endpoints.
"""

import os
import asyncio
import csv

from cowdao_cowpy.app_data.utils import PartnerFee, generate_app_data
from cowdao_cowpy.common.config import SupportedChainId
from cowdao_cowpy.cow.swap import OrderBookAPIConfigFactory, OrderBookApi
from cowdao_cowpy.order_book.api import AppDataHash


def app_data_exists(orderbook: OrderBookApi, app_data_hash: AppDataHash) -> bool:
    try:
        # Attempt to fetch the app data from the orderbook
        asyncio.run(orderbook.get_app_data(app_data_hash))
    except Exception as e:
        print(f"App data not found: {e}")
        return False
    return True


def build_and_post_app_data(
    orderbook: OrderBookApi,
    app_code: str,
    graffiti: str,
    referrer_address: str,
    partner_fee: PartnerFee,
) -> str:
    create_app_data = generate_app_data(
        app_code=app_code,
        graffiti=graffiti,
        referrer_address=referrer_address,
        partner_fee=partner_fee,
    )
    if not app_data_exists(orderbook, create_app_data.app_data_hash):
        print("App data does not exist, uploading...")
        asyncio.run(
            orderbook.put_app_data(
                create_app_data.app_data_object, create_app_data.app_data_hash
            )
        )
    return create_app_data.app_data_hash.root


def main(chunk):
    chain_id = SupportedChainId.BASE
    env = "prod"  # or "staging" depending on your setup
    order_book_api = OrderBookApi(OrderBookAPIConfigFactory.get_config(env, chain_id))
    app_code = "exampleAppCode"
    referrer_address = "0x1234567890abcdef1234567890abcdef12345678"
    partner_fee_address = "0x1234567890abcdef1234567890abcdef12345679"
    partner_fee = PartnerFee(
        bps=1, recipient=partner_fee_address
    )  # Example fee structure
    app_data_hash = build_and_post_app_data(
        order_book_api,
        chunk,
        app_code,
        referrer_address,
        partner_fee,
    )
    return app_data_hash


# if __name__ == "__main__":
#    linenum = 0
#    with open("Moomeo.txt", "r") as file:
#        for line in file:
#           if line.strip() != "":
#              linenum += 1
#              print("Line from Moomeo.txt: ", line.strip())
#    for i in range(linenum):
#       print("Hash " + str(i) + " is: " + str(main(i)))

if __name__ == "__main__":
    lines = []

    with open("Moomeo.txt", "r") as file:
        for line in file:
            if line.strip() != "":
                lines.append(line.strip())
                print("Line from Moomeo.txt:", line.strip())

    output_path = os.path.abspath("output.csv")
    with open(output_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Line", "Hash"])

        for i, line in enumerate(lines):
            hash_value = main(i)
            print("Hash", i, "is:", hash_value)
            writer.writerow([line, hash_value])
