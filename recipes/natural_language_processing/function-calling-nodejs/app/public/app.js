function app () {
  const sendMessageButton = document.getElementById('sendMessage');
  const userMessageText = document.getElementById('userMessage');
  const statusSpinner = document.getElementById('statusSpinner');
  const chartCtx = document.getElementById('myChart');
  let myLineChart;

  userMessageText.onkeydown = function(e){
    if (e.key === 'Enter') {
      messageHander();
    }
  };

  sendMessageButton.addEventListener('click', (evt) => {
    evt.preventDefault();

    messageHander();

  });

  function messageHander() {
    // If send is pressed and nothing is in the input, it does nothing
    const userMessageTextValue = userMessageText.value;

    if (userMessageTextValue.trim().length < 1) {
      return;
    }

    // reset the input
    userMessageText.value = '';

    // Disable the button
    sendMessageButton.setAttribute('disabled', 'disabled');

    //unhide the spinner
    statusSpinner.style.display = '';

    // Send to the server
    sendToServer(userMessageTextValue);
  }

  function createChart(temperatureData) {
    // Create the chart from the data
    if (myLineChart) {
      myLineChart.destroy();
    }

    myLineChart = new Chart(chartCtx, {
      type: 'line',
      data: {
        labels: temperatureData.hourly.time,
        datasets: [{
          label: 'Temperatures',
          data: temperatureData.hourly.temperature_2m,
          borderWidth: 1
        }]
      },
      options: {
      }
    });
  }

  async function sendToServer(city) {
    const result = await fetch('/api/temperatures', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        city: city
      })
    });

    const jsonResult = await result.json();

    // undisable the button
    sendMessageButton.removeAttribute('disabled');

    //hide the spinner
    statusSpinner.style.display = 'none';
    createChart(jsonResult.result);
  }
}

app();