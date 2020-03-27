$(document).ready(function () {


    let selected = -1

    let addBoards = (boards) => {
        let boardContainer = document.getElementById("radio-group-boards")
        for (i = 0; i < boards.length; i++) {
            addBoard(boardContainer, boards[i])
        }
        addDummyBoards(boardContainer)
        selectFirstBoard()
    }

    let selectFirstBoard = () => {
        let boardContainer = document.getElementById("radio-group-boards")
        let firstChild = boardContainer.firstChild
        firstChild.setAttribute("class", "radio selected")
        selected = firstChild.getAttribute("data-value")

    }

    let addDummyBoards = (boardContainer) => {
        let bogusIds = [5, 10, 8, 11, 7, 3, 9]
        for (id of bogusIds) {
            addBoard(boardContainer, id)
        }
    }

    let addBoard = (boardContainer, id) => {
        let radio = document.createElement("div")
        radio.setAttribute("class", "radio")
        radio.setAttribute("data-value", id)
        let radioText = document.createTextNode("Board " + id)
        radio.appendChild(radioText)
        boardContainer.appendChild(radio)
    }
    let initBoards = () => {
        fetch('http://klevang.dk:19409/boards')
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                addBoards(data)
            }).then(addEventListeners);
    }

    let updatePreview = () => {
        let preview = document.getElementById("rgb-preview")
        let r = document.getElementById("range-red").value
        let g = document.getElementById("range-green").value
        let b = document.getElementById("range-blue").value
        let previewBG = "rgb(" + r + "," + g + "," + b + ")"
        preview.style.backgroundColor = previewBG
    }

    let submitColor = () => {
        let r = parseInt(document.getElementById("range-red").value)
        let g = parseInt(document.getElementById("range-green").value)
        let b = parseInt(document.getElementById("range-blue").value)
        let boardID = parseInt(selected)
        let data = {
            "board_id": boardID,
            "red": r,
            "green": g,
            "blue": b
        }
        console.log(data)
        fetch('http://klevang.dk:19409/submitcolor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });


    }

    let initPreviewListener = () => {
        document.getElementById("hover-preview").addEventListener('click', submitColor)
    }

    let initRangeSliderListeners = () => {
        document.getElementById("range-red").addEventListener("input", updatePreview)
        document.getElementById("range-green").addEventListener("input", updatePreview)
        document.getElementById("range-blue").addEventListener("input", updatePreview)
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

