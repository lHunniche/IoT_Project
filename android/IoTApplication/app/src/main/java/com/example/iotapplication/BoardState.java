package com.example.iotapplication;

import com.google.gson.annotations.SerializedName;

public class BoardState {
    @SerializedName("board_id")
    private String boardId;
    private int red;
    private int blue;
    private int green;
    @SerializedName("led_intensity")
    private int ledIntensity;
    private int setpoint;

    public BoardState(String boardId, int red, int blue, int green, int ledIntensity, int setpoint) {
        this.boardId = boardId;
        this.red = red;
        this.blue = blue;
        this.green = green;
        this.ledIntensity = ledIntensity;
        this.setpoint = setpoint;
    }

    public String getBoardId() {
        return boardId;
    }

    public void setBoardId(String boardId) {
        this.boardId = boardId;
    }

    public int getRed() {
        return red;
    }

    public void setRed(int red) {
        this.red = red;
    }

    public int getBlue() {
        return blue;
    }

    public void setBlue(int blue) {
        this.blue = blue;
    }

    public int getGreen() {
        return green;
    }

    public void setGreen(int green) {
        this.green = green;
    }

    public int getLedIntensity() {
        return ledIntensity;
    }

    public void setLedIntensity(int ledIntensity) {
        this.ledIntensity = ledIntensity;
    }

    public int getSetpoint() {
        return setpoint;
    }

    public void setSetpoint(int setpoint) {
        this.setpoint = setpoint;
    }
}
