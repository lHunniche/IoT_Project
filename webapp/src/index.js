
$(document).ready(function () {
    let selected = -1


    let addBoards = (data) => {
        let boardContainer = document.getElementById("radio-group-boards")
        let boards = data["boards"]
        for (i = 0; i < boards.length; i++) {
            console.log("A BOARD: ")
            console.log(boards[i])
            addBoard(boardContainer, boards[i])
        }
        selectFirstBoard()
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




    let setBoardColor = (boardId, color) => {
        console.log("Trying to color ")
        console.log(boardId)
        console.log(color)
        let boardRadioBtn = document.getElementById(boardId)

        let rgbString = "rgb(" + color['red'] + "," + color['green'] + "," + color['blue'] + ")"
        let fontColor = light([color['red'], color['green'], color['blue']]) ? 'rgb(0,0,0)' : 'rgb(255,255,255)'
        boardRadioBtn.style.backgroundColor = rgbString
        boardRadioBtn.style.color = fontColor
    }


    let initBoards = () => {
        fetch('http://klevang.dk:19409/boards?secret=QmGZADAipmhKsovsIhyQQcsTxgFkiy')
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                addBoards(data)
            }).then(addEventListeners)
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

    let updatePreview = () => {
        let preview = document.getElementById("rgb-preview")
        let percentDisplay = document.getElementById("percent-display")
        let rangePWM = document.getElementById("range-pwm").value
        console.log(rangePWM)
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

    let submitColor = () => {
        let r = parseInt(document.getElementById("range-red").value)
        let g = parseInt(document.getElementById("range-green").value)
        let b = parseInt(document.getElementById("range-blue").value)
        let pwmPercentage = parseInt(document.getElementById("range-pwm").value)
        let boardID = selected
        setBoardColor(boardID, { "red": r, "green": g, "blue": b })
        let colorData = {
            "board_id": boardID,
            "red": r,
            "green": g,
            "blue": b,
            "pwm_duty_cycle": pwmPercentage
        }
        fetch('http://klevang.dk:19409/submitcolor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(colorData),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log('Success:', data);
            })
            .then(setBoardColor(colorData["board_id"], colorData))
            .catch((error) => {
                console.error('Error:', error);
            });


    }

    let initPreviewListener = () => {
        document.getElementById("hover-preview").addEventListener('click', submitColor)
    }

    let initRangeSliderListeners = () => {
        let sliders = ["range-red", "range-green", "range-blue", "range-pwm"]
        for(slider of sliders) {
            document.getElementById(slider).addEventListener("input", updatePreview)
        }
    }
    let initRadioEventListener = () => {
        $('.radio-group .radio').click(function () {
            $(this).parent().find('.radio').removeClass('selected');
            $(this).addClass('selected');
            var val = $(this).attr('data-value');
            selected = val
        });
    }

    let addEventListeners = () => {
        initRadioEventListener()
        initRangeSliderListeners()
        initPreviewListener()
    }

    updatePreview()
    initBoards()


});

