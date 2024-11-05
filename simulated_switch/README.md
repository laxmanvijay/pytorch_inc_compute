# Distributed AllReduce Implementation

A TCP server-based implementation of the AllReduce collective communication operation using Python multiprocessing.

## Overview

The system consists of:

- **TCP Server**: Listens on port 10000 for incoming data
- **Master Node**: Coordinates the AllReduce operation by:
  - Parsing TCP packets
  - Distributing data chunks to workers
  - Aggregating results
- **Worker Nodes**: Process data chunks in parallel
- **AllReduce Operation**: Implements sum reduction across distributed data

## Requirements

- Python 3.7+
- scapy
- unittest

## Setup with Virtual Environment (Recommended)

It's recommended to use a virtual environment to avoid conflicts with system packages:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Mac/Linux
# or
.\venv\Scripts\activate  # On Windows
```

Running the server:

```bash
python server.py
```

Testing:

```bash
python -m unittest test_allreduce.py -v
```