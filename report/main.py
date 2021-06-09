from time import sleep
from reporter import Reporter


def countdown(x: int):
    for i in range(0, x):
        print(f"Starting in {x - i}")
        sleep(1)


def main():
    countdown(3)
    reporter = Reporter()
    reporter.report_all_players()


if __name__ == "__main__":
    main()
