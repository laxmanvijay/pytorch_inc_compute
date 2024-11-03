# PyTorch Inc Backend

Welcome to the PyTorch Inc Compute repository. This project acts as a standalone library for performing tensor computations over the network.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

To install the necessary dependencies, install vcpkg first.

```bash
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg

./bootstrap-vcpkg.sh  # Linux/macOS
.\bootstrap-vcpkg.bat  # Windows
```

Add the install directory to `VCPKG_ROOT`

Then create a virtual environment:

```bash
python -m venv venv
source ./venv/bin/activate
```

At the time of writing, pytorch doesn't yet support python >3.13. Therefore it is better to use something less that 3.13 like:

```bash
python3.12 -m venv venv
source ./venv/bin/activate
```

Install the dependencies for both c++ and python:

```bash
cd pytoch_inc_compute/
vcpkg install
pip install -r requirements.txt
```

## Usage

This package can be built as a static library using cmake and then manually distributed.

To build the package:

```bash
cmake --preset=default
cmake --build build
```

Or it could be consumed by vcpkg directly by required packages using overlay ports (like pytorch_inc_backend package for example). 

To install it as a vcpkg port, cd outside this project and run:

```bash
vcpkg install incc --overlay-ports=pytorch_inc_compute
```

Then on the dependent package, configure the vcpkg-configuration.json file and point it to this directory:

```json
{
    "overlay-ports": [
        "../pytorch_inc_compute"
    ]
}
```

Then run `vcpkg install` on the dependent package to install `incc`.

Overlay ports is configured using the following files:
* portfile.cmake

For every change in this library, this process has to be repeated to see the changes in the dependent packages.