package com.example.smartboard;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.Toast;

public class MenuActivity extends Activity {
    ImageButton btnhan, btneng, btnmanage;
    @Override
    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);

        ImageButton btnhan = (ImageButton) findViewById(R.id.btnhan);
        ImageButton btneng = (ImageButton) findViewById(R.id.btneng);
        ImageButton btnmanage = (ImageButton) findViewById(R.id.btnmanage);
        ImageButton btncheck = (ImageButton) findViewById(R.id.btncheck);

        btnhan.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","νκΈ");
                startService(intent);

                Intent han_intent = new Intent(getApplicationContext(), HanActivity.class);
                startActivity(han_intent);
            }
        });
        btneng.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","μμ΄");
                startService(intent);

                Intent eng_intent = new Intent(getApplicationContext(), EngActivity.class);
                startActivity(eng_intent);
            }
        });
        btnmanage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","μ λ³΄");
                startService(intent);

                Intent man_intent = new Intent(getApplicationContext(), ProgressActivity.class);
                startActivity(man_intent);
            }
        });
        btncheck.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(getApplicationContext(), MyService.class);
                intent.putExtra("step", 1);
                intent.putExtra("mode","νμ¬νμ΅νμΈ");
                startService(intent);

                Intent man_intent = new Intent(getApplicationContext(), ReturnActivity.class);
                startActivity(man_intent);
            }
        });
    }
}
