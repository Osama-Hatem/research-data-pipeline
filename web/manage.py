import os
import sys


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


if PROJECT_ROOT not in sys.path:

    sys.path.insert(
        0,
        PROJECT_ROOT
    )


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "research_web.settings"
)


def main():

    try:

        from django.core.management import (
            execute_from_command_line
        )

    except ImportError as error:

        raise ImportError(

            "Django is not installed. "
            "Install it with: pip install django"

        ) from error


    execute_from_command_line(
        sys.argv
    )


if __name__ == "__main__":

    main()