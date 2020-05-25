package com.example.iotapplication;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;

public interface IRetrofitClient {

    @GET("/boards?secret=QmGZADAipmhKsovsIhyQQcsTxgFkiy")
    Call<GetBoardResponse> getBoards();

    @POST("/updateboardstate")
    Call<Void> toggleAutolight(@Body AutoLight body);

    @POST("/updateboardstate")
    Call<Void> toggleBlueLight(@Body BlueLight blueLight);

    @POST("/updateboardstate")
    Call<Void> updateBoardState(@Body BoardState boardState);
}


