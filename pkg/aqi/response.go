package aqi

// Response represents the main response body from the API.
type Response struct {
	Data []Weather `json:"data"`
}

// Weather represents the mappings inside "data" array of response body.
type Weather struct {
	AirQuality string  `json:"aqi"`
	UID        int     `json:"uid"`
	Station    Station `json:"station"`
}

// Station represents the mappings with weather station data.
type Station struct {
	Name string `json:"name"`
}
