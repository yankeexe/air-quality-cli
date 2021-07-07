package cmd

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/yankeexe/air-quality-cli/pkg/aqi"
	"github.com/yankeexe/air-quality-cli/pkg/utils"
)

func TestGetSearchQueries(t *testing.T) {
	stationsConfig := map[string]utils.Stations{
		"Bhaisipati, Ktm, Nepal":       {"Bhaisipati, KTM, Nepal", 10495, "kathmandu"},
		"Us Embassy, Kathmandu, Nepal": {"US Embassy, Kathmandu, Nepal", 9468, "kathmandu"},
	}

	config := utils.Config{ApiKey: "abcdef", Stations: stationsConfig}

	want := map[string][]int{"kathmandu": {10495, 9468}}
	got := groupSearchQueries(config)

	assert.Equal(t, want, got)
}

type MockRequest struct {
	handleRequest func() (*aqi.Response, error)
}

func (req *MockRequest) Fetch(query string) (*aqi.Response, error) {
	return req.handleRequest()
}

func TestGetFilteredStations(t *testing.T) {

	res := &aqi.Response{Data: []aqi.Weather{
		{
			AirQuality: "100", UID: 11, Station: aqi.Station{Name: "Kathmandu"},
		},
		{
			AirQuality: "80", UID: 55, Station: aqi.Station{Name: "Bhaktapur"},
		},
	}}

	req := &MockRequest{}
	aqi.HTTPClient = req

	req.handleRequest = func() (*aqi.Response, error) {
		return res, nil
	}

	groupedStations := map[string][]int{"kathmandu": {11, 55}}

	got, _ := getFilteredResponse(groupedStations)

	assert.Equal(t, res, got)

}

func TestGetFilteredStationsReturnsError(t *testing.T) {
	req := &MockRequest{}
	aqi.HTTPClient = req

	req.handleRequest = func() (*aqi.Response, error) {
		return nil, errors.New("api is not responsive")
	}

	groupedStations := map[string][]int{"kathmandu": {11, 55}}
	_, err := getFilteredResponse(groupedStations)

	want := "api is not responsive"
	assert.Equal(t, want, err.Error())
}
