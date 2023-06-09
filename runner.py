from app.factory import create_belt_service
from argparse import ArgumentParser

from app.utils import Environment

parser = ArgumentParser(
    description="Program to control a conveyor belt for sorting discs"
)

parser.add_argument(
    "--simulate", action="store_true", help="Flag to simulate the run of conveyor"
)

if __name__ == "__main__":
    args = parser.parse_args()

    if not args.simulate:
        Environment().set_live()

    service = create_belt_service()
    service.run()
