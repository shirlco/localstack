def main():
    # initialize repositories
    import localstack.extensions.repository

    localstack.extensions.repository.init()

    from .localstack import create_with_plugins

    cli = create_with_plugins()
    cli()


if __name__ == "__main__":
    main()
