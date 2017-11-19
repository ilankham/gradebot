[![Python 3.6](https://img.shields.io/badge/python-3.6-brightgreen.svg)](#prerequisites)  [![license](https://img.shields.io/badge/license-MIT%20License-blue.svg)](LICENSE)

# Virtual TA
A package for managing student grades

## Getting Started

1. Download this repo.
2. Follow the examples in [example_client.py](example_client.py).

An API token can be generated by
- visiting [https://api.slack.com/custom-integrations/legacy-tokens](https://api.slack.com/custom-integrations/legacy-tokens) and generating a Legacy Token, or
- visiting [https://api.slack.com/apps](https://api.slack.com/apps) and creating a new app with permission scopes for chat:write:user, im:read, and users:read

Additional documentation for the Slack Web API can be found at [https://api.slack.com/web](https://api.slack.com/web)

### Prerequisites

This package requires Python 3.6 or greater, along with the Python modules specified in [requirements.txt](requirements.txt).

The Slack Account features of this package also require non-guest access to a Slack Workspace, which can be setup for free at [https://www.slack.com/](https://www.slack.com/)

## Running the tests

The provided functional and unit tests can be run as follows:
```
python -m unittest tests/functional_tests.py
```
and
```
python -m unittest tests/unit_tests.py
```

## License
This project is licensed under the MIT License; see the [LICENSE](LICENSE) file for details.

## Author
* [ilankham](https://github.com/ilankham)
* [kaiichang](https://github.com/kaiichang)

## Disclaimer

This project is in no way affiliated with Slack.
