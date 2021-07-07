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
	"github.com/yankeexe/air-quality-cli/pkg/utils"
)

// removeCmd represents the remove command
var removeCmd = &cobra.Command{
	Use:   "remove",
	Short: "Remove stations from the configuration.",
	Long: `Remove stations from the configuration.
Does not take any user arguments.
`,
	Example: "air remove",
	Run: func(cmd *cobra.Command, args []string) {

		if len(args) >= 1 {
			cmd.Help()
			os.Exit(0)
		}

		c := utils.NewConfig()
		config, err := utils.GetCurrentConfig(c)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		currentConfig := config.Stations
		if len(currentConfig) == 0 {
			color.Danger.Println("There are no stations in your config file.\nUse `air add <city/country>` to add new stations.")
			os.Exit(1)
		}

		stationNames := []string{}
		stations := config.Stations

		for name := range stations {
			stationNames = append(stationNames, name)
		}

		selectionMessage := "Choose a station to delete from your config file"
		selectedStations, err := utils.ShowSelectionMenu(stationNames, selectionMessage)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		for _, station := range selectedStations {
			delete(config.Stations, station)
		}

		err = utils.SaveConfig(*config)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		color.Success.Println("Station/s removed:", selectedStations)

	},
}

func init() {
	rootCmd.AddCommand(removeCmd)
}
