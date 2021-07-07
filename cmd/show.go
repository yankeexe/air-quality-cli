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

	"github.com/olekukonko/tablewriter"

	"github.com/gookit/color"
	"github.com/spf13/cobra"
	"github.com/yankeexe/air-quality-cli/pkg/aqi"
	"github.com/yankeexe/air-quality-cli/pkg/utils"
)

// showCmd represents the show command
var showCmd = &cobra.Command{
	Use:   "show",
	Short: "Show AQI of all the stations in config.",
	Long: `Show AQI of all the stations in config.
Does not take any user arguments.
`,
	Example: "air show",
	Run: func(cmd *cobra.Command, args []string) {

		if len(args) >= 1 {
			cmd.Help()
			os.Exit(0)
		}

		c := utils.NewConfig()

		err := utils.CheckConfig(c)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		config, err := utils.GetCurrentConfig(c)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		currentConfig := config.Stations

		if len(currentConfig) == 0 {
			color.Warn.Println("There are no stations in your config file.")
			color.Info.Println("Use `air add <city/country>` to add new stations.")
			os.Exit(0)
		}

		queries := groupSearchQueries(*config)
		filteredResponse, err := getFilteredResponse(queries)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		all, _ := cmd.Flags().GetBool("all")

		table := tablewriter.NewWriter(os.Stdout)
		utils.CreateTable(*filteredResponse, table, all)
		table.Render()
	},
}

// groupSearchQueries groups stations with same search query from the config file.
func groupSearchQueries(config utils.Config) map[string][]int {
	stations := config.Stations
	storeMap := make(map[string][]int)

	for _, v := range stations {
		// Group together stations with the same searchQuery
		storeMap[v.SearchQuery] = append(storeMap[v.SearchQuery], v.UID)
	}

	return storeMap
}

// getFilteredResponse makes request to the AQI API and filters the stations in the config file.
func getFilteredResponse(groupedStations map[string][]int) (*aqi.Response, error) {
	filteredRes := aqi.Response{}

	for query, uids := range groupedStations {
		res, err := aqi.HTTPClient.Fetch(query)
		if err != nil {
			return nil, err
		}

		for _, data := range res.Data {
			for _, uid := range uids {
				if data.UID == uid {
					filteredRes.Data = append(filteredRes.Data, data)
				}

			}
		}
	}

	return &filteredRes, nil
}

func init() {
	rootCmd.AddCommand(showCmd)
	showCmd.Flags().Bool("all", false, "Show stations even with no station data")
}
