// Reads all elements with 'calendar' class
let dateInput = document.getElementsByClassName('calendar')

// Sets the maximum allowable date for all items with 'calendar' class
function limitUpperDate() {
    let upperDate = new Date()
    upperDate = upperDate.toLocaleDateString('en-CA')

    for(let i = 0; i < dateInput.length; i++) {
        dateInput[i].setAttribute("max", upperDate)
    }

    return upperDate
}

// Sets the minimum allowable date for all elements with 'calendar' class
function limitLowerDate() {
    let lowerDate = new Date()
    let day = lowerDate.getDate()

    if (day >= cutoffDay) {
        lowerDate.setDate(cutoffDay)
    } else {
        lowerDate.setDate(lowerDate.getDate() - day)
        lowerDate.setDate(cutoffDay)
    }

    lowerDate = lowerDate.toLocaleDateString('en-CA')

    for(let i = 0; i < dateInput.length; i++) {
        dateInput[i].setAttribute("min", lowerDate)
    }

    return lowerDate
}

limitUpperDate()
limitLowerDate()