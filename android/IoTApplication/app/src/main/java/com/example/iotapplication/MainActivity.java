package com.example.iotapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.SeekBar;
import android.widget.Switch;
import android.widget.TextView;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "Retrofit";

    private IRetrofitClient retrofitClient;
    private int red, green, blue, led, setpoint;
    private TextView rText, gText, bText, ledText, setpointText;
    private Button submitButton, setpointButton;
    private SeekBar rSeekbar, gSeekBar, bSeekbar, ledSeekbar, setpointSeekbar;
    private RecyclerView recyclerView;
    private RecyclerViewAdapter adapter;
    private Switch autoLightSwitch, blueLightSwitch;
    private Board board;

    private boolean updateBoard;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        retrofitClient = Utils.getRetrofitClient();
        submitButton = findViewById(R.id.submitbutton);
        setpointButton = findViewById(R.id.setpointButton);

        rText = findViewById(R.id.RTextView);
        rSeekbar = findViewById(R.id.RSeekbar);

        gText = findViewById(R.id.gTextView);
        gSeekBar = findViewById(R.id.GSeekbar);

        bText = findViewById(R.id.BTextView);
        bSeekbar = findViewById(R.id.BSeekbar);

        ledSeekbar = findViewById(R.id.ledSeekbar);
        ledText = findViewById(R.id.LEDTextView);

        autoLightSwitch = findViewById(R.id.autoLightSwitch);
        blueLightSwitch = findViewById(R.id.bluelightFilterSwitch);

        setpointSeekbar = findViewById(R.id.setpointSeekbar);
        setpointText = findViewById(R.id.setpointTextView);

        recyclerView = findViewById(R.id.recyclerview);
        adapter = new RecyclerViewAdapter(this, new ArrayList<Board>());
        recyclerView.setAdapter(adapter);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        getBoards();

        ledSeekbar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                led = i;
                ledText.setText("" + i);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        setpointSeekbar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                setpoint = i;
                setpointText.setText("" + i);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        rSeekbar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                red = i;
                rText.setText("" + i);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
            }
        });

        gSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                green = i;
                gText.setText("" + i);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
            }
        });

        bSeekbar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                blue = i;
                bText.setText("" + i);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
            }
        });


        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                updateBoardState(board.getBoardId(), red, blue, green, led, setpoint);
            }
        });

        setpointButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                updateBoardState(board.getBoardId(), red, blue, green, led, setpoint);
            }
        });


        adapter.onBoardSelected = new OnBoardSelected() {
            @Override
            public void onBoardSelected(Board board) {
                MainActivity.this.selectBoard(board);
            }
        };

        autoLightSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                if (!updateBoard) {
                    toggleAutoLight(MainActivity.this.board.getBoardId());
                }
            }
        });

        blueLightSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                if (!updateBoard) {
                    toggleBlueLight(MainActivity.this.board.getBoardId());
                }
            }
        });

    }

    private void toggleAutoLight(String boardId) {
        retrofitClient.toggleAutolight(new AutoLight(boardId)).enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                getBoards();
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                Log.e(TAG, "AUTOLIGHT: not working: " + t.getMessage());
            }
        });

    }

    private void toggleBlueLight(String boardId) {
        retrofitClient.toggleBlueLight(new BlueLight(boardId)).enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                getBoards();
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                Log.e(TAG, "BLUELIGHT: not working: " + t.getMessage());
            }
        });
    }

    private void selectBoard(Board board) {
        updateBoard = true;
        ledSeekbar.setProgress(board.getLedIntensity());
        rSeekbar.setProgress(board.getColor().getRed());
        bSeekbar.setProgress(board.getColor().getBlue());
        gSeekBar.setProgress(board.getColor().getGreen());
        autoLightSwitch.setChecked(board.isAutoAdjustLight());
        setpointSeekbar.setProgress(board.getSetpoint());
        blueLightSwitch.setChecked(board.isBlueLightFilter());
        this.board = board;
        updateBoard = false;
    }

    public void getBoards() {

        retrofitClient.getBoards().enqueue(new Callback<GetBoardResponse>() {
            @Override
            public void onResponse(Call<GetBoardResponse> call, Response<GetBoardResponse> response) {
                Log.i(TAG, "onResponse: GET request worked ");
                ArrayList<Board> boardList = response.body().getBoards();
                MainActivity.this.adapter.updateItems(boardList);
            }

            @Override
            public void onFailure(Call<GetBoardResponse> call, Throwable t) {
                Log.i(TAG, "onFailure: GET request not worked: " + t.getMessage());

            }
        });
    }

    public void updateBoardState(String boardId, int red, int blue, int green, int ledIntensity, int setpoint) {
        retrofitClient.updateBoardState(new BoardState(boardId, red, blue, green, ledIntensity, setpoint)).enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                Log.i(TAG, "UPDATE BOARD STATE: Post request went through successfully.");
                getBoards();
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                Log.e(TAG, "UPDATE BOARD STATE: Unable to post the request." + t.getMessage());
            }
        });
    }
}


//    public void submitPost(String board_id, int red, int green, int blue, int ledIntensity) {
//        retrofitClient.saveValues(new RGBPostModel(red, green, blue, ledIntensity, board_id)).enqueue(new Callback<Void>() {
//            @Override
//            public void onResponse(Call<Void> call, Response<Void> response) {
//                String text = response.code() + "";
//                Log.e("Test", text);
//                if(response.isSuccessful()) {
//                    Log.i(TAG, "SUBMIT COLOR: Post request went through successfully.");
//
//                    getBoards();
//                }
//            }
//            @Override
//            public void onFailure(Call<Void> call, Throwable t) {
//                Log.e("Error",call.request().toString());
//
//                Log.e(TAG,"SUBMIT COLOR: Unable to post the request.");
//
//            }
//        });
//
//    }

//    public void updateSetPoint(String board_id, int setpoint) {
//        retrofitClient.updateSetpoint(new Setpoint(board_id, setpoint)).enqueue(new Callback<Void>() {
//            @Override
//            public void onResponse(Call<Void> call, Response<Void> response) {
//                String text = response.code() + "";
//                Log.e("Update Setpoint test", text);
//                if (response.isSuccessful()) {
//                    Log.i(TAG, "UPDATE SETPOINT: Post request went through successfully.");
//                    getBoards();
//                }
//            }
//            @Override
//            public void onFailure(Call<Void> call, Throwable t) {
//                Log.e("Error",call.request().toString());
//
//                Log.e(TAG,"UPDATE SETPOINT: Unable to post the request." + t.getMessage());
//
//            }
//        });
//    }
