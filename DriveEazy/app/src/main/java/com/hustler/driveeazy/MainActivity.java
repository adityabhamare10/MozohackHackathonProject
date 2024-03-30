package com.hustler.driveeazy;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;


public class MainActivity extends AppCompatActivity {

    Button object, sleep;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sleep = findViewById(R.id.sleep);
        object = findViewById(R.id.object);

//        if(!Python.isStarted()){
//            Python.start(new AndroidPlatform(this));
//        }

//        Python py = Python.getInstance();
//        PyObject pyobj = py.getModule("sleep_detection");



        sleep.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent i = new Intent(MainActivity.this, SleepActivity.class);
                startActivity(i);
                Toast.makeText(MainActivity.this, "Sleep Watcher getting started", Toast.LENGTH_SHORT).show();
            }
        });

        object.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(MainActivity.this, "Object Detection get Started", Toast.LENGTH_SHORT).show();
            }
        });

    }
}