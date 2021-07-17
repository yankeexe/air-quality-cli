package utils

import (
	"strconv"

	"github.com/gookit/color"
	"github.com/olekukonko/tablewriter"
	"github.com/yankeexe/air-quality-cli/pkg/aqi"
)

// CreateTable creates table based on response data.
func CreateTable(r aqi.Response, table *tablewriter.Table, all bool) {
	table.SetHeader([]string{"Location", "AQI", "Level", "Implications", "Cautionary"})
	table.SetHeaderColor(
		tablewriter.Colors{tablewriter.Bold},
		tablewriter.Colors{tablewriter.Bold},
		tablewriter.Colors{tablewriter.Bold},
		tablewriter.Colors{tablewriter.Bold, tablewriter.BgBlueColor},
		tablewriter.Colors{tablewriter.Bold, tablewriter.BgHiRedColor},
	)

	table.SetBorder(true)
	table.SetRowLine(true)

	// Create table based on response data.
	FillTable(r, table, all)
}

// FillTable draws table to stdout based on response values from the API.
func FillTable(r aqi.Response, table *tablewriter.Table, all bool) {
	for _, data := range r.Data {
		airQuality := data.AirQuality

		if airQuality == "-" {
			if all {
				info := aqi.NoInfo
				table.Append([]string{data.Station.Name, "-", info.Level, info.Implications, info.Caution})
			}
			continue
		}

		// convert str index value to int
		index, err := strconv.Atoi(airQuality)
		if err != nil {
			panic(err)
		}

		// good
		if index <= 50 {
			info := aqi.Good
			table.Append([]string{data.Station.Name, color.Green.Sprint(strconv.Itoa(index)), color.Green.Sprint(info.Level), info.Implications, info.Caution})
		}

		// moderate
		if (index > 50) && (index <= 100) {
			info := aqi.Moderate
			table.Append([]string{data.Station.Name, color.Green.Sprint(strconv.Itoa(index)), color.Green.Sprint(info.Level), info.Implications, info.Caution})
		}

		// unhealthy for sensitive groups
		if (index > 100) && (index <= 150) {
			info := aqi.UnhealthySensitive
			table.Append([]string{data.Station.Name, color.Yellow.Sprint(strconv.Itoa(index)), color.Yellow.Sprint(info.Level), info.Implications, info.Caution})
		}

		// unhealthy
		if (index > 150) && (index <= 200) {
			info := aqi.Unhealthy
			table.Append([]string{data.Station.Name, color.Yellow.Sprint(strconv.Itoa(index)), color.Yellow.Sprint(info.Level), info.Implications, info.Caution})
		}

		// very unhealthy
		if (index > 200) && (index <= 300) {
			info := aqi.VeryUnhealthy
			table.Append([]string{data.Station.Name, color.Red.Sprint(strconv.Itoa(index)), color.Red.Sprint(info.Level), info.Implications, info.Caution})
		}

		// hazardous
		if index > 300 {
			level := aqi.Hazardous
			table.Append([]string{data.Station.Name, color.Red.Sprint(strconv.Itoa(index)), color.Red.Sprint(level.Level), level.Implications, level.Caution})
		}
	}
}
