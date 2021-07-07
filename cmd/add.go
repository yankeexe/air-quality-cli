/*
Copyright © 2021 Yankee Maharjan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package cmd

import (
	"os"

	"github.com/gookit/color"
	"github.com/spf13/cobra"
	"github.com/yankeexe/air-quality-cli/pkg/aqi"
	"github.com/yankeexe/air-quality-cli/pkg/utils"
)

type stationsStore struct {
	stations map[string]utils.Stations
}

func (s *stationsStore) add(name string, uid int) map[string]utils.Stations {
	s.stations[name] = utils.Stations{StationName: name, UID: uid}
	return s.stations
}

// addCmd represents the add command
var addCmd = &cobra.Command{
	Use:     "add",
	Short:   "Add locations to config to view them later",
	Long:    `Add locations to config to view them later`,
	Example: "air add kathmandu",
	Run: func(cmd *cobra.Command, args []string) {
		// Show help message if no arguments are passed.
		if len(args) == 0 {
			cmd.Help()
			os.Exit(0)
		}

		c := utils.NewConfig()

		err := utils.CheckConfig(c)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		// utils.CheckConfig()
		searchQuery := args[0]

		res, err := aqi.HTTPClient.Fetch(searchQuery)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		if len(res.Data) == 0 {
			color.Warn.Println("No data found for search query:", searchQuery)
			os.Exit(0)
		}

		var stationNames []string
		stationsStore := stationsStore{}

		// Initialize map (would be nil map if not set)
		stationsStore.stations = map[string]utils.Stations{}

		for _, data := range res.Data {
			stationNames = append(stationNames, data.Station.Name)
			stationsStore.add(data.Station.Name, data.UID)
		}

		selectionMessage := "Choose a station to add to your config file"
		selectedStations, err := utils.ShowSelectionMenu(stationNames, selectionMessage)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		config, err := updateStationsConfig(selectedStations, stationsStore, searchQuery)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		err = utils.SaveConfig(*config)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}
		color.Success.Println("Station/s added:", selectedStations)

	},
}

func init() {
	rootCmd.AddCommand(addCmd)
}

// updateStationsConfig updates the stations dictionary for config file.
func updateStationsConfig(selectedStations []string, stationsStore stationsStore, searchQuery string) (*utils.Config, error) {
	// config := utils.GetCurrentConfig()
	c := utils.NewConfig()

	config, err := utils.GetCurrentConfig(c)
	if err != nil {
		return nil, err
	}
	currentConfig := config.Stations

	// Initialize map (would be nil map if not set)
	config.Stations = make(map[string]utils.Stations)

	stations := stationsStore.stations
	for _, station := range selectedStations {
		config.Stations[station] = utils.Stations{StationName: station, UID: stations[station].UID, SearchQuery: searchQuery}
	}

	// Append previous config (if exists) with newly added config.
	if len(currentConfig) > 0 {
		for k, v := range currentConfig {
			config.Stations[k] = v
		}
	}

	return config, nil
}
