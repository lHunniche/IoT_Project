package com.example.iotapplication;

public class RGBModel {
    private Integer board_id;
    private Integer red;
    private Integer green;
    private Integer blue;

    public int getId() { return board_id; }

    public void setBoard_id(Integer board_id) { this.board_id = board_id; }

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
}
