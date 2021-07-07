package utils

import (
	"errors"
	"io/ioutil"
	"os"
	"os/user"
	"path/filepath"
	"strings"

	"github.com/AlecAivazis/survey/v2"
	"github.com/gookit/color"
	"github.com/spf13/viper"
	"gopkg.in/yaml.v2"
)

type AirConfig interface {
	load() Config
}

// Stations store data related to each station.
type Stations struct {
	StationName string `yaml:"stationName,omitempty"`
	UID         int    `yaml:"uid,omitempty"`
	SearchQuery string `yaml:"searchQuery,omitempty"`
}

// Config store configuration for the CLI.
type Config struct {
	ApiKey   string              `yaml:"apiKey,omitempty"`
	Stations map[string]Stations `yaml:"stations,omitempty"`
}

func (c *Config) UpdateApiKey(newKey string) {
	c.ApiKey = newKey
}

func (c *Config) load() error {
	err := viper.Unmarshal(&c)
	if err != nil {
		return err
	}
	return nil
}

var usr, _ = user.Current()

var ConfigDirPath = filepath.Join(usr.HomeDir, ".air")
var ConfigFilePath = filepath.Join(ConfigDirPath, "aqi")

// CheckConfigDirectory checks if config directory `$HOME/.air` is present.
// If not present, atttempts to create one.
func CheckConfigDirectory() error {
	// Create config directory if it does not exist.
	if _, err := os.Stat(ConfigDirPath); os.IsNotExist(err) {
		if err := os.Mkdir(ConfigDirPath, 0770); err != nil {
			return err
		}
	}
	return nil
}

func NewConfig() *Config {
	c := &Config{}
	return c
}

func CheckConfig(config *Config) error {
	err := config.load()
	if err != nil {
		return errors.New("couldn't read config file")
	}

	if config.ApiKey == "" {
		color.Info.Println("🔑 Get your API key from: https://aqicn.org/data-platform/token/#/")
		return errors.New("no API key found, use `air init` to enter")
	}
	return nil
}

func GetCurrentConfig(config *Config) (*Config, error) {
	err := config.load()
	if err != nil {
		return nil, err
	}

	stations := config.Stations
	updatedStations := make(map[string]Stations)

	// viper isn't case sensitive while Unmarshalling. Make keys case sensitive.
	if len(stations) >= 1 {
		for k, v := range stations {
			title := strings.Title(k)
			updatedStations[title] = v
		}
	}
	config.Stations = updatedStations

	return config, nil
}

// SaveConfig writes new/updated config to the config file.
func SaveConfig(config Config) error {
	data, err := yaml.Marshal(&config)
	if err != nil {
		return err
	}

	err = writeToFile(ConfigFilePath, data)
	if err != nil {
		return err
	}

	return nil
}

func writeToFile(filePath string, data []byte) error {
	err := ioutil.WriteFile(filePath, data, 0777)
	if err != nil {
		return err
	}
	return nil
}

// ShowSelectionMenu renders the selection menu.
func ShowSelectionMenu(stationNames []string, message string) ([]string, error) {
	var selectedStations []string
	prompt := &survey.MultiSelect{
		Message: message,
		Options: stationNames,
	}
	err := survey.AskOne(prompt, &selectedStations)
	if err != nil {
		return nil, err
	}

	return selectedStations, nil
}
