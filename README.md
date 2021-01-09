# Air Quality Index CLI

Get Air Quality index for your City.

## Installation

```bash
$ pip install air-quality-cli
```

## Contents
- [Air Quality Index CLI](#air-quality-index-cli)
  - [Installation](#installation)
  - [Contents](#contents)
  - [Usage](#usage)
    - [Initialization](#initialization)
    - [Seach for air quality based on country or city name](#seach-for-air-quality-based-on-country-or-city-name)
    - [Save your city to config for quick view.](#save-your-city-to-config-for-quick-view)
  - [Contributing](#contributing)
## Usage
### Initialization
One time setup to initialize the CLI using API token.

> [Get your API Token!](https://aqicn.org/data-platform/token/#/)

```bash
$ air init
```

### Seach for air quality based on country or city name

```bash
$ air search kathmandu
```

```bash
$ air search Nepal
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/71vLztO.gif" width="700" alt="demo of air quality cli search" />

</details>

### Save your city to config for quick view.

You can save stations from a number of locations to quickly view air quality there.

**Save the location**

```bash
$ air add kathmandu
```

**Show air quality from all your saved locations**

```bash
$ air show
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/1C4tCDM.gif" width="700" alt="demo of air quality cli | add and show" />

## Contributing

For guidance on setting up a development environment and how to make a contribution to `air-quality-cli`, see the [contributing guidelines](https://github.com/yankeexe/air-quality-cli/blob/master/CONTRIBUTING.md).
