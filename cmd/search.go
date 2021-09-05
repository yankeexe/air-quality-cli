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
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/gookit/color"
	fuzzyfinder "github.com/ktr0731/go-fuzzyfinder"
	"github.com/olekukonko/tablewriter"
	"github.com/spf13/cobra"
	"github.com/yankeexe/air-quality-cli/pkg/aqi"
	"github.com/yankeexe/air-quality-cli/pkg/utils"
)

// searchCmd represents the search command
var searchCmd = &cobra.Command{
	Use:     "search",
	Short:   "Search for city or country to get AQI",
	Long:    `Search for city or country`,
	Example: "air search kathmandu",
	Run: func(cmd *cobra.Command, args []string) {

		// Handle no argument passed
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

		killSignal := make(chan os.Signal, 1)
		signal.Notify(killSignal, os.Interrupt, syscall.SIGTERM)

		go func() {
			<-killSignal
			fmt.Println("Search stopped")
			os.Exit(130)
		}()

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

		all, _ := cmd.Flags().GetBool("all")
		search, _ := cmd.Flags().GetBool("fuzzy")

		table := tablewriter.NewWriter(os.Stdout)

		if search {
			selectedStations, err := fuzzySearchList(res.Data)
			if err != nil {
				color.Warn.Println(err)
				os.Exit(0)
			}
			utils.CreateTable(aqi.Response{Data: *selectedStations}, table, all)
		} else {
			utils.CreateTable(*res, table, all)
		}

		table.Render()
	},
}

func init() {
	rootCmd.AddCommand(searchCmd)
	searchCmd.Flags().BoolP("all", "a", false, "air search -a")
	searchCmd.Flags().BoolP("fuzzy", "f", false, "air search -s")
}

func fuzzySearchList(response []aqi.Weather) (*[]aqi.Weather, error) {
	index, err := fuzzyfinder.FindMulti(response, func(i int) string {
		return response[i].Station.Name
	},
		fuzzyfinder.WithPreviewWindow(func(i, width, height int) string {
			if i == -1 {
				return ""
			}

			return fmt.Sprintf(`%s

			Station Name: %s
			Index: %s`,
				"Use <TAB> to select multiple stations",
				response[i].Station.Name,
				response[i].AirQuality)
		}))

	if err != nil {
		return nil, err
	}

	selectedItems := []aqi.Weather{}

	for _, idx := range index {
		selectedItems = append(selectedItems, response[idx])
	}

	return &selectedItems, nil
}
