$(document).ready(function () {
    let selected = -1


    let addBoards = (data) => {
        let boardContainer = document.getElementById("radio-group-boards")
        let boards = data["boards"]
        for (i = 0; i < boards.length; i++) {
            addBoard(boardContainer, boards[i])
        }
        selectFirstBoard()
        selectBoard()
    }

    let selectFirstBoard = () => {
        let boardContainer = document.getElementById("radio-group-boards")
        let firstChild = boardContainer.firstChild
        if (firstChild != null) {
            firstChild.setAttribute("class", "radio selected")
            selected = firstChild.getAttribute("data-value")
        }
    }


    let addBoard = (boardContainer, board) => {
        let radio = document.createElement("div")
        radio.setAttribute("class", "radio")
        radio.setAttribute("id", board["board_id"])
        radio.setAttribute("data-value", board["board_id"])
        let radioText = document.createTextNode("💡" + board["name"])
        radio.appendChild(radioText)
        boardContainer.appendChild(radio)
        let red = board["color"]["red"]
        let green = board["color"]["green"]
        let blue = board["color"]["blue"]
        radio.style.backgroundColor = "rgb(" + red + "," + green + "," + blue + ")"
        radio.style.color = light([red, green, blue]) ? 'rgb(0,0,0)' : 'rgb(255,255,255)'
    }




    let initBoards = () => {
        fetch('http://klevang.dk:19409/boards?secret=QmGZADAipmhKsovsIhyQQcsTxgFkiy')
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                addBoards(data)
            }).then(addEventListeners)
            .then(updateUI)
            .catch(e => console.log("Couldnt fetch boards"))
    }

    let light = (color) => {
        let r, g, b, hsp;

        r = color[0];
        g = color[1];
        b = color[2];

        hsp = Math.sqrt(
            0.299 * (r * r) +
            0.587 * (g * g) +
            0.114 * (b * b)
        )
        if (hsp > 127.5) {
            return true;
        }
        else {

            return false;
        }
    }

    let initRangeSliderListeners = () => {
        let sliders = ["range-red", "range-green", "range-blue", "range-pwm"]
        for (slider of sliders) {
            document.getElementById(slider).addEventListener("input", updatePreviewUI)
        }
    }
    let initRadioEventListener = () => {
        $('.radio-group .radio').click(function () {
            $(this).parent().find('.radio').removeClass('selected');
            $(this).addClass('selected');
            boardId = this.id
            let val = $(this).attr('data-value');
            selected = val
            selectBoard()
        });
    }


    let selectBoard = () => {
        fetch("http://klevang.dk:19409/getboardinforaw?board_id=" + selected)
            .then((response) => {
                return response.json();
            })
            .then((response) => updateUI(response))
    }

    let updateUI = (board) => {
        console.log(board)
        let color = board["color"]
        let r = color["red"]
        let g = color["green"]
        let b = color["blue"]
        let intensity = board["led_intensity"]
        let autoAdjust = JSON.parse(board["auto_adjust_light"])
        let nightMode = JSON.parse(board["blue_light_filter"])
        let setpoint = board["setpoint"]
        //console.log(autoAdjust)
        //console.log(nightMode)
        updateSlidersUI(r, g, b, intensity)
        updateToggleBtnsUI(autoAdjust, nightMode)
        updateSetPointUI(setpoint)
        updatePreviewUI()
    }

    let updateSlidersUI = (r, g, b, intensity) => {
        document.getElementById("range-red").value = r
        document.getElementById("range-green").value = g
        document.getElementById("range-blue").value = b
        document.getElementById("range-pwm").value = intensity
    }

    let updateToggleBtnsUI = (autoAdjust, nightMode) => {
        updateNightModeBtnUI(nightMode)
        updateAutoAdjustBtnUI(autoAdjust)
    }
    let updateNightModeBtnUI = (nightMode) => {
        let btnNight = $("#btn-night-mode")
        nightMode ? btnNight.attr("class", "night-mode-on") : btnNight.removeClass("night-mode-on")
    }

    let updateAutoAdjustBtnUI = (autoAdjust) => {
        let btnAutoAdjust = $("#btn-auto-adjust")
        autoAdjust ? btnAutoAdjust.attr("class", "auto-adjust-on") : btnAutoAdjust.removeClass("auto-adjust-on")
    }

    let updatePreviewUI = () => {
        let preview = document.getElementById("rgb-preview")
        let percentDisplay = document.getElementById("percent-display")
        let rangePWM = document.getElementById("range-pwm").value
        let previewHover = document.getElementById("hover-preview")

        let r = document.getElementById("range-red").value
        let g = document.getElementById("range-green").value
        let b = document.getElementById("range-blue").value

        let previewBG = "rgb(" + r + "," + g + "," + b + ")"
        let invertedColor = light([r, g, b]) ? 'rgb(0,0,0)' : 'rgb(255,255,255)'
        percentDisplay.innerHTML = rangePWM + "%"
        percentDisplay.style.color = invertedColor
        previewHover.style.color = invertedColor
        preview.style.backgroundColor = previewBG
    }

    let updateSetPointUI = (setpoint) => {
        for (setpoint in document.getElementById("setpoints")) {
            if (setpoint.value == setpoint) {

            }
        }
    }

    let addAutoAdjustListener = () => {
        $("#btn-auto-adjust").click(function () {
            let currState = $(this).attr("value")
            let newState = !JSON.parse(currState)
            $(this).attr("value", newState)
            updateState()
        })
    }

    let addNightModeListener = () => {
        $("#btn-night-mode").click(function () {
            let currState = $(this).attr("value")
            let newState = !JSON.parse(currState)
            $(this).attr("value", newState)
            updateState()
        })
    }

    let init = () => {
        initBoards()
    }

    let addEventListeners = () => {
        initRadioEventListener()
        initRadioSetPointEventListener()
        addAutoAdjustListener()
        addNightModeListener()
        addSubmitColorListener()
        initRangeSliderListeners()
    }

    let initRadioSetPointEventListener = () => {
        $('.radio-group-setpoints .radio').click(function () {
            $(this).parent().find('.radio').removeClass('selected');
            $(this).addClass('selected');
            boardId = this.id
            let val = $(this).attr('data-value');
            selected = val
        });
    }

    let addSubmitColorListener = () => {
        document.getElementById("hover-preview").addEventListener("click", function () {
            updateState()
        })
    }


    let getSetPoint = () => {
        return 200
    }


    let updateState = () => {
        let boardId = selected
        let red = document.getElementById("range-red").value
        let green = document.getElementById("range-green").value
        let blue = document.getElementById("range-blue").value
        let intensity = document.getElementById("range-pwm").value
        let auto_adjust_light = document.getElementById("btn-auto-adjust").value
        let blue_light_filter = document.getElementById("btn-night-mode").value
        let set_point = getSetPoint()
        let updatedState = {
            "board_id": boardId,
            "red": red,
            "green": green,
            "blue": blue,
            "led_intensity": intensity,
            "blue_light_filter": blue_light_filter,
            "auto_adjust_light": auto_adjust_light,
            "setpoint": set_point

        }
        fetch("http://klevang.dk:19409/updateboardstate", {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedState)
        })
            .then((response) => {
                return response.json()
            }).then((response) => {
                console.log(response)
                updateUI(response["board"])
            })
    }

    init()

})