package com.example.iotapplication;

import androidx.appcompat.app.AppCompatActivity;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.SeekBar;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "Test: ";
    private IRetrofitClient retrofitClient;
    private int red, green, blue;
    private TextView rText, gText, bText;
    private Button button;
    private ProgressBar rProgressBar, gProgressBar, bProgressBar;
    private SeekBar rSeekbar, gSeekBar, bSeekbar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        retrofitClient = Utils.getRetrofitClient();
        button = (Button) findViewById(R.id.button);

        rText = (TextView) findViewById(R.id.RTextView);
        rProgressBar = (ProgressBar) findViewById(R.id.RProgressBar);
        rSeekbar = (SeekBar) findViewById(R.id.RSeekbar);

        gText = (TextView) findViewById(R.id.gTextView);
        gProgressBar = (ProgressBar) findViewById(R.id.GProgressBar);
        gSeekBar = (SeekBar) findViewById(R.id.GSeekbar);

        bText = (TextView) findViewById(R.id.BTextView);
        bProgressBar = (ProgressBar) findViewById(R.id.BProgressBar);
        bSeekbar = (SeekBar) findViewById(R.id.BSeekbar);

        rSeekbar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                red = i;
                seekBar.setMax(255);
                rText.setText("" + i);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        gSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                blue = i;
                seekBar.setMax(255);
                gText.setText("" + i);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        bSeekbar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                green = i;
                seekBar.setMax(255);
                bText.setText("" + i);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) { }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) { }
        });

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendPost(2, red, green, blue);
            }
        });
    }

    public void sendPost(int board_id, int red, int green, int blue) {
        retrofitClient.saveValues(2, red, green, blue).enqueue(new Callback<RGBModel>() {
            @Override
            public void onResponse(Call<RGBModel> call, Response<RGBModel> response) {
                if(response.isSuccessful()) {
                    Log.i(TAG, "Post request went through successfully. " + response.body().toString());
                }g
            }

            @Override
            public void onFailure(Call<RGBModel> call, Throwable t) {
                Log.e(TAG,"Unable to post the request.");
            }
        });

    }
}