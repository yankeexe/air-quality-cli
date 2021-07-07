package aqi

// Info represents the information based on Air Quality Index.
type Info struct {
	Level, Implications, Caution string
}

var (
	// Good represents the information when AQI is below 50.
	Good = Info{"Good", "Air quality is considered satisfactory, and air pollution poses little or no risk", "-"}

	// Moderate represents the information when AQI is above 50 and less than or equal to 100.
	Moderate = Info{"Moderate", "Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.", "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion."}

	// UnhealthySensitive represents the information when AQI is above 100 and less than or equal to 150.
	UnhealthySensitive = Info{"Unhealthy for Sensitive Groups", "Members of sensitive groups may experience health effects. The general public is not likely to be affected.", "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion."}

	// Unhealthy represents the information when AQI is above 150 and less than or equal to 200.
	Unhealthy = Info{"Unhealthy", "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects", "Active children and adults, and people with respiratory disease, such as asthma, should avoid prolonged outdoor exertion; everyone else, especially children, should limit prolonged outdoor exertion"}

	// VeryUnhealthy represents the information when AQI is above 200 and less than or equal to 300.
	VeryUnhealthy = Info{"Very Unhealthy", "Health warnings of emergency conditions. The entire population is more likely to be affected.", "Active children and adults, and people with respiratory disease, such as asthma, should avoid all outdoor exertion; everyone else, especially children, should limit outdoor exertion."}

	// Hazardous represents the information when AQI is above 300.
	Hazardous = Info{"Hazardous", "Health alert: everyone may experience more serious health effects", "Everyone should avoid all outdoor exertion"}

	NoInfo = Info{"-", "-", "-"}
)
