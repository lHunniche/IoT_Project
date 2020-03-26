package com.example.iotapplication;

public class Utils {
    public static final String baseUrl = "http://klevang.dk:19409/init/";

    public static IRetrofitClient getRetrofitClient() {
        return RetrofitClient.getClient(baseUrl).create(IRetrofitClient.class);
    }
}
