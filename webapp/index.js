function docReady(fn) {
    if (document.readyState === "complete" || document.readyState === "interactive") {
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}   


docReady(function() {
    
    let addEventListeners = () => {
        document.getElementById("range-red").addEventListener("input", updatePreview)
        document.getElementById("range-green").addEventListener("input", updatePreview)
        document.getElementById("range-blue").addEventListener("input", updatePreview)
        document.getElementById("hover-preview").addEventListener('click', submitColor)
    }

    let addBoards = (boards) => {
        let boardContainer = document.getElementById("board-radio-btns")
        for(i = 0; i < boards.length; i++) {
            addBoard(boardContainer, boards[i])
        }   
    }

    let addBoard = (boardContainer, id) => {
        let container = document.createElement("div")
        container.setAttribute("class", "radio-container")
        let radio = document.createElement('input')
        radio.setAttribute("type", "radio")
        radio.setAttribute("id", id)
        radio.setAttribute("name", "board")
        radio.setAttribute("class", "board-radio")
        let label = document.createElement("label")
        label.setAttribute("for", id)
        let idTxtNode = document.createTextNode("Board " + id)
        label.appendChild(idTxtNode)
        container.appendChild(radio)
        container.appendChild(label)
        boardContainer.appendChild(container)
    }

    let initBoards = () => {
        fetch('http://klevang.dk:19409/boards')
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                addBoards(data)
             });
    }

    let updatePreview = () => {
        let preview = document.getElementById("rgb-preview")
        let r = document.getElementById("range-red").value
        let g = document.getElementById("range-green").value
        let b = document.getElementById("range-blue").value
        let previewBG = "rgb("+r+","+g+","+b+")"
        console.log(previewBG)
        preview.style.backgroundColor = previewBG
    }

    let getCheckedId = () => {
        let inputs = document.getElementsByClassName("board-radio")
        for(i = 0; i < inputs.length; i++) {
            if(inputs[i].checked) {
                return parseInt(inputs[i].id)
            }
        }
        
        //.filter(input => input.checked)[0]
    }


    let submitColor = () => {
        let r = parseInt(document.getElementById("range-red").value)
        let g = parseInt(document.getElementById("range-green").value)
        let b = parseInt(document.getElementById("range-blue").value)
        let boardID = getCheckedId()
        let data = {
            "board_id": boardID,
            "red": r,
            "green": g,
            "blue":b
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
    updatePreview()
    addEventListeners()
    initBoards()
   

});

