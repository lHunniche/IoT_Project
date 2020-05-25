package com.example.iotapplication;

import com.google.gson.annotations.SerializedName;

public class RGBPostModel {

    private int red;
    private int green;
    private int blue;
    @SerializedName("led_intensity")
    private int ledIntensity;

    public RGBPostModel(int red, int green, int blue, int ledIntensity, String boardId) {
        this.red = red;
        this.green = green;
        this.blue = blue;
        this.ledIntensity = ledIntensity;
        this.boardId = boardId;
    }

    @SerializedName("board_id")
    private String boardId;


    public int getRed() {
        return red;
    }

    public void setRed(int red) {
        this.red = red;
    }

    public int getGreen() {
        return green;
    }

    public void setGreen(int green) {
        this.green = green;
    }

    public int getBlue() {
        return blue;
    }

    public void setBlue(int blue) {
        this.blue = blue;
    }

    public int getLedIntensity() {
        return ledIntensity;
    }

    public void setLedIntensity(int ledIntensity) {
        this.ledIntensity = ledIntensity;
    }

    public String getBoardId() {
        return boardId;
    }

    public void setBoardId(String boardId) {
        this.boardId = boardId;
    }
}
