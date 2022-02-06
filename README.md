# Air Quality Index CLI
[![Go Report Card](https://goreportcard.com/badge/github.com/yankeexe/air-quality-cli)](https://goreportcard.com/report/github.com/yankeexe/air-quality-cli)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache-yellow.svg)](https://opensource.org/licenses/Apache-2.0)
![Latest GitHub release](https://img.shields.io/github/release/yankeexe/air-quality-cli)

Get Air Quality index for your City.


## Installation

```bash
curl -f https://raw.githubusercontent.com/yankeexe/air-quality-cli/master/install.sh | sudo sh
```

### Manual Installation
Download the [latest release](https://github.com/yankeexe/air-quality-cli/releases).


### Verification of artifacts

All artifacts are checksummed and the checksum file is signed with [cosign](https://github.com/sigstore/cosign#installation) (keyless).

* Download checksum and sig file for verification.

  ```bash
  wget https://github.com/yankeexe/air-quality-cli/releases/download/v0.0.6/checksums.txt

  wget https://github.com/yankeexe/air-quality-cli/releases/download/v0.0.6/checksums.txt.sig
  ```
* Verify the signature

  ```bash
  COSIGN_EXPERIMENTAL=1 cosign verify-blob --signature checksums.txt.sig checksums.txt
  ```
  If the signature is valid, verify the SHA256 match with the downloaded binary.

* Verify Downloaded Binary

  Store downloaded binary on the same dir as `checksums.txt`
  ```bash
  sha256sum --ignore-missing -c checksums.txt
  ```


<img src="https://i.imgur.com/FsnXPXw.png" width="800" />

## Contents
- [Air Quality Index CLI](#air-quality-index-cli)
  - [Installation](#installation)
  - [Contents](#contents)
  - [Usage](#usage)
    - [Initialization](#initialization)
    - [Search for air quality based on country or city name](#search-for-air-quality-based-on-country-or-city-name)
    - [Save your city to config for quick view.](#save-your-city-to-config-for-quick-view)
    - [Remove saved city from your config](#remove-saved-city-from-your-config)
  - [Contributing](#contributing)
## Usage
### Initialization
One time setup to initialize the CLI using API token.

> [Get your API Token!](https://aqicn.org/data-platform/token/#/)

```bash
$ air init
```

### Search for air quality based on country or city name

```bash
$ air search kathmandu

# by default, stations whose data is not avaiable is hidden.
# use --all or -a to show stations even if there's no data.

$ air search kathmandu --all
```

```bash
$ air search Nepal
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/KtEEfRV.gif" width="700" alt="demo of air quality cli search" />

</details>

**Fuzzy search the stations from your query.**

Alternative to viewing all the stations as table, you can also fuzzy search the stations returned from your query.

Use `-f` or `--fuzzy` flag to initiage fuzzy searching.

```bash
$ air search kathmandu -f

# by default, stations whose data is not avaiable is hidden.
# use --all or -a to show stations even if there's no data.
$ air search kathmandu -fa
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/9M5akjp.gif" width="700" alt="demo of air quality cli search" />

</details>

### Save your city to config for quick view.

You can save stations from a number of locations to quickly view air quality there.

**Save the location**

```bash
$ air add kathmandu
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/DmpFBEH.gif" width="700" alt="demo of air quality cli add stations" />

</details>

**Show air quality from all your saved locations**

```bash
$ air show

# by default, stations whose data is not avaiable is hidden.
# use --all or -a to show stations even if there's no data.

$ air show --all
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/YLtIWIz.gif" width="700" alt="demo of air quality cli show" />


### Remove saved city from your config

You can remove any saved stations/city from your config if you no longer need its information.


```bash
$ air remove
```

> <details><summary><strong>Demo</strong></summary>
> <img src = "https://i.imgur.com/DXZI4sG.gif" width="700" alt="demo of air quality cli remove" />


## Contributing

For guidance on setting up a development environment and how to make a contribution to `air-quality-cli`, see the [contributing guidelines](https://github.com/yankeexe/air-quality-cli/blob/master/CONTRIBUTING.md).
