# aid_curriculum_backend

## Setup

This project uses [Pipenv](https://pipenv.pypa.io/) for dependency and environment management.

### Prerequisites

- Python 3.12 or higher
- pip

### Installation

1. Install Pipenv (if not already installed):
   ```bash
   pip install --user pipenv
   ```

2. Install project dependencies:
   ```bash
   pipenv install
   ```

3. Install development dependencies:
   ```bash
   pipenv install --dev
   ```

### Usage

#### Activating the Virtual Environment

```bash
pipenv shell
```

#### Running Commands in the Virtual Environment

Without activating the shell:
```bash
pipenv run python <script.py>
```

#### Adding Dependencies

For production dependencies:
```bash
pipenv install <package-name>
```

For development dependencies:
```bash
pipenv install --dev <package-name>
```

#### Updating Dependencies

```bash
pipenv update
```

#### Removing Dependencies

```bash
pipenv uninstall <package-name>
```

#### Checking for Security Vulnerabilities

```bash
pipenv check
```

### Additional Resources

- [Pipenv Documentation](https://pipenv.pypa.io/en/latest/)
- [Pipenv Basic Usage](https://pipenv.pypa.io/en/latest/basics/)