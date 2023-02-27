// Runs the displayTime function every second
setInterval(displayTime, 1000)

function displayTime() {
    const date = new Date()

    document.getElementById('clock-box').innerHTML = date.toLocaleString('sv-SE')
}

// Reads all elements with 'calendar' class
let dateInput = document.getElementsByClassName('calendar')

// Sets the minimum and maximum allowable dates for all items with 'calendar' class
function limitDates() {
    const currentDate = new Date()
    const today = currentDate.getDate()
    let lowerDate = new Date()

    if (today < cutoffDay) {
        lowerDate = currentDate.getDate() - today
    }

    lowerDate.setDate(cutoffDay)

    lowerDate = lowerDate.toLocaleString('sv-SE').slice(0, 10)
    upperDate = currentDate.toLocaleString('sv-SE').slice(0, 10)

    for(let i = 0; i < dateInput.length; i++) {
        dateInput[i].setAttribute('max', upperDate)
        dateInput[i].setAttribute('min', lowerDate)
    }
    
    return [lowerDate, upperDate]
}

limitDates()