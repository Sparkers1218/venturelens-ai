from database.connection import initialize_database


def main() -> None:
    initialize_database()
    print("VentureLens database initialized.")


if __name__ == "__main__":
    main()
