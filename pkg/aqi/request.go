package aqi

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"net/url"

	"github.com/spf13/viper"
)

// httpClient fetches data from the API.
type httpClient interface {
	Fetch(query string) (*Response, error)
}

// Request represents the request data sent to the API.
type Request struct {
	URL string
}

var HTTPClient httpClient = &Request{URL: "https://api.waqi.info/search/?"}

// Fetch makes HTTP request to the waqi API to retrieve AQI information.
func (req *Request) Fetch(query string) (*Response, error) {
	params := url.Values{}
	params.Add("keyword", query)
	params.Add("token", viper.GetString("apiKey"))

	resp, err := http.Get("https://api.waqi.info/search/?" + params.Encode())
	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	response := &Response{}
	if err := json.Unmarshal(body, &response); err != nil {
		return nil, err
	}

	return response, nil
}
