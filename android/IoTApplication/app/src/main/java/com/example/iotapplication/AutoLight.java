package com.example.iotapplication;

import com.google.gson.annotations.SerializedName;

public class AutoLight {
    public AutoLight(String boardId) {
        this.boardId = boardId;
    }

    @SerializedName("board_id")
    private String boardId;

    public String getBoardId() {
        return boardId;
    }

    public void setBoardId(String boardId) {
        this.boardId = boardId;
    }

}
