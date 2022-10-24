def get_response():
    return {
        "id": "1234",
        "type": "checkout",
        "cart": [
            {
                "id": "5678",
                "item": "socks",
                "quantity": 42,
                "price": 3.50,
            },
        ],
    }


def cart_total(r):
    return r["cart"]["quantity"] * r["cart"]["price"]


def error_locations_example():
    print(cart_total(get_response()))


def main():
    error_locations_example()


if __name__ == "__main__":
    main()
