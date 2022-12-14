package com.example.smartboard;


import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Message;
import android.util.Log;
import android.os.Handler;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;


public class ManageActivity extends Activity {
    TextView last_day, korState, engState;
    TextView korWord1, korWord2, korWord3, korWord4;
    TextView korYN1, korYN2, korYN3, korYN4;
    TextView engWord1, engWord2, engWord3, engWord4;
    TextView engYN1, engYN2, engYN3, engYN4;

    SeekBar seekBar;
    String TAG = "mytag";

    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_manage);

        last_day = (TextView) findViewById(R.id.last_day);
        seekBar = (SeekBar) findViewById(R.id.corr_goal);

        korState = (TextView) findViewById(R.id.korState);
        engState = (TextView) findViewById(R.id.engState);

        korWord1 = (TextView) findViewById(R.id.korWord1);
        korWord2 = (TextView) findViewById(R.id.korWord2);
        korWord3 = (TextView) findViewById(R.id.korWord3);
        korWord4 = (TextView) findViewById(R.id.korWord4);

        korYN1 = (TextView) findViewById(R.id.korYN1);
        korYN2 = (TextView) findViewById(R.id.korYN2);
        korYN3 = (TextView) findViewById(R.id.korYN3);
        korYN4 = (TextView) findViewById(R.id.korYN4);

        engWord1 = (TextView) findViewById(R.id.engWord1);
        engWord2 = (TextView) findViewById(R.id.engWord2);
        engWord3 = (TextView) findViewById(R.id.engWord3);
        engWord4 = (TextView) findViewById(R.id.engWord4);

        engYN1 = (TextView) findViewById(R.id.engYN1);
        engYN2 = (TextView) findViewById(R.id.engYN2);
        engYN3 = (TextView) findViewById(R.id.engYN3);
        engYN4 = (TextView) findViewById(R.id.engYN4);

        // OnSeekBarChange ????????? - Seekbar ??? ????????? ??????????????? Listener
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                // onProgressChange - Seekbar ??? ?????????????????? ??????
            }
            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                // onStartTeackingTouch - SeekBar ??? ???????????? ??? ????????? ??????
            }
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                // onStopTrackingTouch - SeekBar ??? ?????? ????????? ????????? ?????? ??????
                Log.d(TAG, String.format("onStopTrackingTouch ??? ?????? ??????: progress [%d]", seekBar.getProgress()));
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","??????,"+seekBar.getProgress());
                startService(intent);
            }
        });
    }

    @Override
    // ?????????????????? ????????? ???????????? ???????????? ???????????????. processCommand??? ?????????????????? ?????????
    // ???????????? oncreate?????? ?????? ?????? ????????? ?????????(????????? ????????????) oncreate?????? ???????????? ??????
    // onNewIntent() ??? ?????? ?????? ??????. ????????? -> ?????????????????? ??????????????????.
    protected void onNewIntent(Intent intent) {
        processIntent(intent);
        super.onNewIntent(intent);
    }


    private void processIntent(Intent intent){
        int step1 = intent.getIntExtra("step",0);
        Log.d("TAG","recv step ??????");
        if(step1==3){
            Log.d("TAG","recv data ??????");
            String data = intent.getStringExtra("data");
            Log.d("TAG","data "+ data);

            String[] array = data.split(",");
            if (array[0].equals("??????")){
                last_day.setText("????????? ????????????: "+array[1]);
                seekBar.setProgress(Integer.parseInt(array[2]));
                korState.setText(array[3]);
                if(array[3].equals("?????? 1")) { // ??????
                    korWord1.setText("??????");
                    korWord2.setText("??????");
                    korWord3.setText("??????");
                    korWord4.setText("??????");
                } else if(array[3].equals("?????? 2")){
                    korWord1.setText("?????????");
                    korWord2.setText("?????????");
                    korWord3.setText("?????????");
                    korWord4.setText("?????????");
                } else if(array[3].equals("?????? 3")){
                    korWord1.setText("?????????");
                    korWord2.setText("????????????");
                    korWord3.setText("????????????");
                    korWord4.setText("????????????");
                }
                korYN1.setText(array[4]);
                korYN2.setText(array[5]);
                korYN3.setText(array[6]);
                korYN4.setText(array[7]);
                engState.setText(array[8]);
                if(array[8].equals("?????? 1")) { // ??????
                    engWord1.setText("sky");
                    engWord2.setText("box");
                    engWord3.setText("lam");
                    engWord4.setText("mom");
                } else if(array[8].equals("?????? 2")){
                    engWord1.setText("good");
                    engWord2.setText("apple");
                    engWord3.setText("hello");
                    engWord4.setText("korea");
                } else if(array[8].equals("?????? 3")){
                    engWord1.setText("pencil");
                    engWord2.setText("window");
                    engWord3.setText("airplane");
                    engWord4.setText("building");
                }
                engYN1.setText(array[9]);
                engYN2.setText(array[10]);
                engYN3.setText(array[11]);
                engYN4.setText(array[12]);
            }
        }
    }
}
