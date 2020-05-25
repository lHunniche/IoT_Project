package com.example.iotapplication;

import com.google.gson.annotations.SerializedName;

public class Board {
    private String name;
    @SerializedName("board_id")
    private String boardId;
    private boolean hasUpdate;
    @SerializedName("led_intensity")
    private int ledIntensity;
    @SerializedName("auto_adjust_light")
    private boolean autoAdjustLight;
    private int setpoint;
    private RGBModel color;
    @SerializedName("blue_light_filter")
    private boolean blueLightFilter;

    public Board(String boardId, boolean hasUpdate, int ledIntensity, boolean autoAdjustLight, int setpoint, RGBModel color, boolean blueLightFilter) {
        this.boardId = boardId;
        this.hasUpdate = hasUpdate;
        this.ledIntensity = ledIntensity;
        this.autoAdjustLight = autoAdjustLight;
        this.setpoint = setpoint;
        this.color = color;
        this.blueLightFilter = blueLightFilter;
    }

    public String getBoardId() {
        return boardId;
    }

    public void setBoardId(String boardId) {
        this.boardId = boardId;
    }

    public boolean isHasUpdate() {
        return hasUpdate;
    }

    public void setHasUpdate(boolean hasUpdate) {
        this.hasUpdate = hasUpdate;
    }

    public int getLedIntensity() {
        return ledIntensity;
    }

    public void setLedIntensity(int ledIntensity) {
        this.ledIntensity = ledIntensity;
    }

    public boolean isAutoAdjustLight() {
        return autoAdjustLight;
    }

    public void setAutoAdjustLight(boolean autoAdjustLight) {
        this.autoAdjustLight = autoAdjustLight;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getSetpoint() {
        return setpoint;
    }

    public void setSetpoint(int setpoint) {
        this.setpoint = setpoint;
    }

    @Override
    public String toString() {
        return "Board{" +
                "name='" + name + '\'' +
                ", boardId='" + boardId + '\'' +
                ", hasUpdate=" + hasUpdate +
                ", ledIntensity=" + ledIntensity +
                ", autoAdjustLight=" + autoAdjustLight +
                ", setpoint=" + setpoint +
                ", color=" + color +
                ", blueLight=" + blueLightFilter +
                '}';
    }

    public RGBModel getColor() {
        return color;
    }

    public void setColor(RGBModel color) {
        this.color = color;
    }

    public boolean isBlueLightFilter() {
        return blueLightFilter;
    }

    public void setBlueLightFilter(boolean blueLightFilter) {
        this.blueLightFilter = blueLightFilter;
    }
}

