
async function loadFlights(){
    const response =
        await fetch(
            "http://127.0.0.1:8000/flights"
        );
    const flights =
        await response.json();
    const list =
        document.getElementById("flightList");
    list.innerHTML = "";
    flights.forEach(flight => {
        const item =
            document.createElement("div");
        item.className = "flight-item";
        item.textContent =
            `${flight.FlightNumber} - ${flight.Airline} → ${flight.Destination}`;
        item.onclick = function(){
            document.getElementById("flightInput").value =
            flight.FlightNumber;
        };
        list.appendChild(item);
    });
}

function formatDateTime(dateString){
    const date = new Date(dateString);
    return date.toLocaleString(
        "en-GB",
        {
            day: "2-digit",
            month: "short",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}

function formatTime(dateString){
    const date = new Date(dateString);
    return date.toLocaleTimeString(
        "en-GB",
        {
            hour: "2-digit",
            minute: "2-digit"
        }
    );
}

function getStatusBadge(status){
    status = status.toLowerCase();
    if(status === "active" || status === "scheduled"){
        return {
            text: "ON TIME",
            className: "status-green"
        };
    }
    if(status.includes("delay")){
        return {
            text: "DELAYED",
            className: "status-yellow"
        };
    }
    if(status.includes("cancel")){
        return {
            text: "CANCELLED",
            className: "status-red"
        };
    }
    return {
        text: status.toUpperCase(),
        className: "status-gray"
    };
}

function getDelayExplanation(data){
    const explanations = [];
    const probability =
        data.DelayProbability;
    if(probability >= 0.7){
        explanations.push(
            "High predicted delay risk based on historical flight patterns."
        );
    }
    else if(probability >= 0.3){
        explanations.push(
            "Moderate delay risk based on historical flight patterns."
        );
    }
    else{
        explanations.push(
            "Low predicted delay risk."
        );
    }
    if(data.Airline){
        explanations.push(
            `Airline: ${data.Airline}`
        );
    }
    if(data.Origin && data.Destination){
        explanations.push(
            `Route: ${data.Origin} → ${data.Destination}`
        );
    }
    if(data.ScheduledDeparture){
        const hour =
            new Date(
                data.ScheduledDeparture
            ).getHours();
        if(hour < 7){
            explanations.push(
                "Early morning departure usually has lower congestion."
            );
        }
        else if(hour >= 17){
            explanations.push(
                "Evening departure may experience higher airport traffic."
            );
        }
    }
    return explanations;
}

function getCongestionColor(level){
    if(level === "Low"){
        return "green";
    }
    if(level === "Moderate"){
        return "orange";
    }
    return "red";
}

function getWeatherImpactColor(impact){
    if(impact === "Low"){
        return "green";
    }
    if(impact === "Medium"){
        return "orange";
    }
    return "red";
}

async function searchFlight() {
    const flightNumber =
        document.getElementById("flightInput").value;
    const response =
        await fetch(
            `http://127.0.0.1:8000/predict/${flightNumber}`
        );
    const data =
        await response.json();
        const status = getStatusBadge(data.FlightStatus);
        const delayExplanation = getDelayExplanation(data);
        const probability = data.DelayProbability;
        let riskText;
        let riskColor;
        if (probability < 0.3) {
            riskText = "Low";
            riskColor = "green";
        } else if (probability < 0.7) {
            riskText = "Medium";
            riskColor = "orange";
        } else {
            riskText = "High";
            riskColor = "red";
        }
    const result =
        document.getElementById("result");

        result.innerHTML = `
<div class="card">
    <h2>${data.FlightNumber}</h2>
    <p>
        ✈️ <strong>${data.Airline}</strong>
    </p>
    <p>
        🛫 <strong>From:</strong><br>
        ${data.OriginAirport} (${data.Origin})
    </p>
    <p>
        🛬 <strong>To:</strong><br>
        ${data.DestinationAirport} (${data.Destination})
    </p>
    <div class="flight-timeline">
    <div class="airport">
        <strong>${data.Origin}</strong>
        <span>
            ${formatTime(data.ScheduledDeparture)}
        </span>
    </div>
    <div class="line">
        ✈️
    </div>
    <div class="airport">
        <strong>${data.Destination}</strong>
        <span>
            ${formatTime(data.ScheduledArrival)}
        </span>
    </div>
</div>
    <p>
        🏢 <strong>Terminal:</strong>
        ${data.Terminal}
    </p>
    <p>
        🚪 <strong>Gate:</strong>
        ${data.Gate}
    </p>
    <p>
        📌 <strong>Status:</strong>
        <span class="status-badge ${status.className}">
        ${status.text}
    </span>
    </p>
    <p>
        🕒 <strong>Scheduled departure:</strong><br>
        ${formatDateTime(data.ScheduledDeparture)}
    </p>
    <p>
        🕘 <strong>Scheduled arrival:</strong><br>
        ${formatDateTime(data.ScheduledArrival)}
    </p>
    <p>
        🔴 <strong>Delay risk:</strong>
        <span style="color:${riskColor}">
            ${riskText}
            (${Math.round(probability*100)}%)
        </span>
    </p>
<div class="delay-explanation">
    <strong>
        Why?
    </strong>
    <ul>
        ${
            delayExplanation
            .map(item =>
                `<li>${item}</li>`
            )
            .join("")
        }
    </ul>
</div>
<div class="congestion-card">
    <h3>
        🚶 Airport congestion
    </h3>
    <div class="progress-container">
        <div 
            class="progress-bar"
            style="
            width:${data.Congestion.percentage}%;
            background:${getCongestionColor(data.Congestion.level)}
            ">
        </div>
    </div>
    <p>
        <strong>
            ${data.Congestion.level}
            traffic
        </strong>
        (${data.Congestion.percentage}%)
    </p>
    <p>
        Recommended:
        Arrive earlier during busy periods.
    </p>
</div>
<div class="weather-card">
    <h3>
        🌦️ Weather impact
    </h3>
    <p>
        🌡️ Temperature:
        ${data.Weather.temperature}°C
    </p>
    <p>
        ☁️ Condition:
        ${data.Weather.condition}
    </p>
    <p>
        💨 Wind:
        ${data.Weather.wind} km/h
    </p>
    <p>
        Flight operation impact:
        <span
        style="
        color:${getWeatherImpactColor(data.Weather.impact)}
        ">
        ${data.Weather.impact}
        </span>
    </p>
</div>
    <p>
        ⏰ <strong>Recommended arrival:</strong><br>
        ${data.RecommendedArrival}
    </p>
</div>
`;
}

window.onload = function(){
    loadFlights();
};
