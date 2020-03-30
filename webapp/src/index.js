
$(document).ready(function () {
    let selected = -1


    let addBoards = (boards) => {
        let boardContainer = document.getElementById("radio-group-boards")
        for (i = 0; i < boards.length; i++) {
            addBoard(boardContainer, boards[i])
        }
        console.log("BOARDS: " + boards)
        setBoardsColors(boards)
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
        element = document.getElementById('rgb-preview');
        let bogusIds = [5, 10, 8, 11, 7, 3, 9]
        for (id of bogusIds) {
            addBoard(boardContainer, id)
        }
    }

    let addBoard = (boardContainer, id) => {
        let radio = document.createElement("div")
        radio.setAttribute("class", "radio")
        radio.setAttribute("id", id)
        radio.setAttribute("data-value", id)
        let radioText = document.createTextNode("💡" + id)
        radio.appendChild(radioText)
        boardContainer.appendChild(radio)
    }

    let setBoardsColors = (boards) => {
        for(boardId of boards) {
            fetchBoardColor(boardId)
        }
    }

    let fetchBoardColor = (boardid) => {
        fetch("http://klevang.dk:19409/getcurrentcolor?board_id="+boardid)
        .then((response) => {
            return response.json();
          })
          .then((data) => {
            setBoardColor(boardid, data)
          });
    }
    let setBoardColor = (boardId, color) => {
        let boardRadioBtn = document.getElementById(boardId)
        boardRadioBtn.style.backgroundColor = "rgb("+color['r'], +","+color['g']+","+color['b']+")"   
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
        if (hsp>127.5) {
            return true;
        } 
        else {
    
            return false;
        }
    }

    let updatePreview = () => {
        console.log("UPDATE")
        let preview = document.getElementById("rgb-preview")
        let previewHover = document.getElementById("hover-preview")
        let r = document.getElementById("range-red").value
        let g = document.getElementById("range-green").value
        let b = document.getElementById("range-blue").value
        let previewBG = "rgb(" + r + "," + g + "," + b + ")"
        let invertedColor = light([r,g,b]) ? 'rgb(0,0,0)' : 'rgb(255,255,255)'
        previewHover.style.color = invertedColor
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
    //initChart()


});

