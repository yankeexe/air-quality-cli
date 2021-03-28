# Air Quality Index CLI

Get Air Quality index for your City.

<p>
<img src="https://img.shields.io/pypi/v/air-quality-cli" />
<img src="https://img.shields.io/pypi/pyversions/air-quality-cli" />
<img src="https://img.shields.io/pypi/l/air-quality-cli" />
</p>

## Installation

```bash
$ pip install air-quality-cli
```
<img src="https://i.imgur.com/FsnXPXw.png" width="800" />

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

### Search for air quality based on country or city name.

```bash
$ air search kathmandu
```

```bash
$ air search Nepal
```

You can also use --select flag to select a particular station to display details.

```bash
$ air search --select Nepal
```

Shorthand -s is also available for --select flag.

```bash
$ air search -s Nepal
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/KtEEfRV.gif" width="700" alt="demo of air quality cli search" />

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

### Remove your city from the config file.

Later you can remove the stations you saved using remove command.

**Remove a station**

```bash
$ air remove kathmandu
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/1C4tCDM.gif" width="700" alt="demo of air quality cli | add and show" />

## Contributing

For guidance on setting up a development environment and how to make a contribution to `air-quality-cli`, see the [contributing guidelines](https://github.com/yankeexe/air-quality-cli/blob/master/CONTRIBUTING.md).
