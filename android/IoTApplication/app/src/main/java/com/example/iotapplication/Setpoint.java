package com.example.iotapplication;

import com.google.gson.annotations.SerializedName;

public class Setpoint {
    @SerializedName("board_id")
    private String boardId;
    private int setpoint;

    public Setpoint(String boardId, int setpoint) {
        this.boardId = boardId;
        this.setpoint = setpoint;
    }

    public String getBoardId() {
        return boardId;
    }

    public void setBoardId(String boardId) {
        this.boardId = boardId;
    }

    public int getSetpoint() {
        return setpoint;
    }

    public void setSetpoint(int setpoint) {
        this.setpoint = setpoint;
    }
}
