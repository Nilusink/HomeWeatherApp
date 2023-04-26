/*
index.js
27. November 2022

functions for index.html

Author:
Nilusink
*/
let current_data = {};


function update_values() {
    fetch("/current_data")
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            if (data !== current_data) {
                graph_data = data;
                document.getElementById("daytime").innerText = data.ftime.split(",")[0];
                document.getElementById("time").innerText = data.ftime.split(",").splice(1).join();
                document.getElementById("humidity").innerText = data.humidity + "%";
                document.getElementById("temperature").innerText = data.temperature + "°C";
                document.getElementById("temperature_index").innerText = data.temperature_index + "°C";
            }
        });
}