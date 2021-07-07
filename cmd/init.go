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
	"strings"

	"github.com/AlecAivazis/survey/v2"
	"github.com/spf13/cobra"
	"github.com/yankeexe/air-quality-cli/pkg/utils"

	"github.com/gookit/color"
)

// initCmd represents the init command
var initCmd = &cobra.Command{
	Use:   "init",
	Short: "Initialize the application using the API token.",
	Long: `Initialize the application using the API token.
Does not take any user arguments.`,
	Example: "air init",
	Run: func(cmd *cobra.Command, args []string) {

		if len(args) >= 1 {
			cmd.Help()
			os.Exit(0)
		}

		token := ""
		prompt := &survey.Password{
			Message: "Enter your API Token",
		}

		err := survey.AskOne(prompt, &token)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		err = utils.CheckConfigDirectory()
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		c := utils.NewConfig()
		config, err := utils.GetCurrentConfig(c)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		config.UpdateApiKey(strings.TrimSpace(token))

		err = utils.SaveConfig(*config)
		if err != nil {
			color.Danger.Println(err)
			os.Exit(1)
		}

		color.Info.Println("Successfully added your API token.\nRun `air search <city-name>` to get started.")
	},
}

func init() {
	rootCmd.AddCommand(initCmd)
}
