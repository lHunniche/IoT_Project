package com.example.iotapplication;

import retrofit2.Call;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.POST;

public interface IRetrofitClient {
    @FormUrlEncoded
    @POST("/postColor")
    Call<RGBModel> saveValues(@Field("board_id") int id, @Field("red") int red, @Field("green") int green, @Field("blue") int blue);
}
