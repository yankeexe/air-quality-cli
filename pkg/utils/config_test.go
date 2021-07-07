package utils

import (
	"io/ioutil"
	"os"
	"strings"
	"testing"

	"github.com/spf13/viper"
	"github.com/stretchr/testify/assert"
)

func TestGetCurrentConfig(t *testing.T) {
	data := `
apiKey: abcdef
stations:
  Bhaisipati, KTM, Nepal:
    stationName: Bhaisipati, KTM, Nepal
    uid: 10495
    searchQuery: kathmandu
  US Embassy, Kathmandu, Nepal:
    stationName: US Embassy, Kathmandu, Nepal
    uid: 9468
    searchQuery: kathmandu
    `
	reader := strings.NewReader(data)

	viper.SetConfigType("yaml")
	err := viper.ReadConfig(reader)
	if err != nil {
		t.Log("Viper readconfig err", err)
	}

	stationsConfig := map[string]Stations{
		"Bhaisipati, Ktm, Nepal":       {"Bhaisipati, KTM, Nepal", 10495, "kathmandu"},
		"Us Embassy, Kathmandu, Nepal": {"US Embassy, Kathmandu, Nepal", 9468, "kathmandu"},
	}

	want := &Config{"abcdef", stationsConfig}
	config := Config{}

	got, _ := GetCurrentConfig(&config)

	assert.Equal(t, got, want)

}

func TestCheckConfig(t *testing.T) {

	noAPIKey := `
apiKey:
stations:
    Bhaisipati, KTM, Nepal:
        stationName: Bhaisipati, KTM, Nepal
        uid: 10495
        searchQuery: kathmandu
    US Embassy, Kathmandu, Nepal:
        stationName: US Embassy, Kathmandu, Nepal
        uid: 9468
        searchQuery: kathmandu
        `
	tests := []struct {
		name string
		data string
		want string
	}{
		{
			name: "No API Key in config.",
			data: noAPIKey,
			want: "no API key found, use `air init` to enter",
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			reader := strings.NewReader(tc.data)
			viper.SetConfigType("yaml")
			err := viper.ReadConfig(reader)
			if err != nil {
				t.Fatal(err)
			}

			config := &Config{}
			got := CheckConfig(config)
			assert.Equal(t, got.Error(), tc.want)
		})
	}
}

func TestUpdateApiKey(t *testing.T) {
	config := Config{ApiKey: "abcdef"}
	want := Config{ApiKey: "newAPIKey"}

	config.UpdateApiKey("newAPIKey")

	assert.Equal(t, config, want)
}

func TestWriteToFile(t *testing.T) {
	f, err := ioutil.TempFile("", "config_test")
	if err != nil {
		t.Fatal(err)
	}

	filename := f.Name()
	data := "Something to test the write function"

	err = writeToFile(filename, []byte(data))
	if err != nil {
		t.Fatal(err)
	}

	contents, err := ioutil.ReadFile(filename)
	if err != nil {
		t.Fatal(err)
	}

	assert.Equal(t, string(contents), data)

	// Cleanup
	f.Close()
	os.Remove(filename)
}

func TestLoadConfig(t *testing.T) {
	data := `
apiKey: abcdef
stations:
  Bhaisipati, KTM, Nepal:
    stationName: Bhaisipati, KTM, Nepal
    uid: 10495
    searchQuery: kathmandu
  US Embassy, Kathmandu, Nepal:
    stationName: US Embassy, Kathmandu, Nepal
    uid: 9468
    searchQuery: kathmandu
    `

	stationsConfig := map[string]Stations{
		"bhaisipati, ktm, nepal":       {"Bhaisipati, KTM, Nepal", 10495, "kathmandu"},
		"us embassy, kathmandu, nepal": {"US Embassy, Kathmandu, Nepal", 9468, "kathmandu"},
	}
	reader := strings.NewReader(data)

	viper.SetConfigType("yaml")
	err := viper.ReadConfig(reader)
	if err != nil {
		t.Log("Viper readconfig err", err)
	}

	config := NewConfig()
	config.load()

	want := &Config{ApiKey: "abcdef", Stations: stationsConfig}

	assert.Equal(t, want, config)
}
