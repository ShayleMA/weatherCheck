// Fetch weather data from OpenWeatherMap API
async function getWeatherData(apiKey, location, startTime, endTime) {
    const baseUrl = "https://api.openweathermap.org/data/2.5/forecast";
    const params = new URLSearchParams({
        appid: apiKey,
        q: location,
        units: "metric"  // Get temperature in Celsius
    });

    try {
        const response = await fetch(`${baseUrl}?${params}`);
        if (!response.ok) {
            throw new Error(`Error fetching weather data: ${response.statusText}`);
        }

        const data = await response.json();

        // Debugging: Log the entire API response to understand the structure
        console.log("Full API Response:\n", data);

        // Filter data for the specified time range
        const filteredData = data.list.filter(forecast => {
            const forecastTime = new Date(forecast.dt_txt).getTime();
            return forecastTime >= new Date(startTime).getTime() &&
                   forecastTime <= new Date(endTime).getTime();
        });

        return filteredData;
    } catch (error) {
        console.error("Error fetching weather data:", error);
        return [];
    }
}

// Process weather data to give clothing recommendations
function processWeatherData(weatherData) {
    let recommendations = [];

    weatherData.forEach(forecast => {
        const temperatureCelsius = forecast.main.temp;

        //Log the temperature for each forecast
        console.log(`Temperature at ${forecast.dt_txt}: ${temperatureCelsius}°C`);

        // Iterate through weather conditions
        forecast.weather.forEach(weather => {
            const weatherId = weather.id;
            const weatherDescription = weather.description;

            // Debugging: Log the weather condition for each forecast
            console.log(`Weather condition at ${forecast.dt_txt}: ${weatherDescription} (ID: ${weatherId})`);

            // Check for storm or rain conditions
            if ([200, 201, 202, 210, 211, 212, 221, 230, 231, 232].includes(weatherId)) {
                recommendations.push("Bring a coat or umbrella!");
            }
        });

        // Check for cold temperatures
        if (temperatureCelsius < 10) {
            recommendations.push("Bring a jumper!");
        }
    });

    return recommendations.length > 0 ? recommendations.join(", ") : "Go crazy wear whatever!";
}


const apiKey = "";
const location = "Leeds, UK";

// Specify start and end times
const startTime = "2024-09-26 12:00:00";
const endTime = "2024-09-26 18:00:00";

// Fetch and process weather data
getWeatherData(apiKey, location, startTime, endTime)
    .then(weatherData => {
        console.log("\nWeather data from OpenWeatherMap:");
        weatherData.forEach(forecast => {
            console.log(`Date/Time: ${forecast.dt_txt}`);
            console.log(`Temperature: ${forecast.main.temp}°C`);
            console.log(`Weather: ${forecast.weather[0].description}`);
        });

        const clothingRecommendations = processWeatherData(weatherData);
        console.log("\nClothing Recommendations:");
        console.log(clothingRecommendations);
    })
    .catch(error => {
        console.error("Error:", error);
    });