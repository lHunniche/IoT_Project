package com.example.iotapplication;

import java.util.Map;

public class RGBModel {
    private Map<String, Integer> dict;
    private Integer board_id;
    private Integer red;
    private Integer green;
    private Integer blue;

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
