from gui import invoke_gui


def main() -> None:
    """An entry point directly invoked via poetry.scripts"""

    invoke_gui(debug=False)


if __name__ == "__main__":
    main()
