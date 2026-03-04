package com.example.incidenttrackerauditor;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Això carrega el teu XML amb el botó ioc_button
        setContentView(R.layout.activity_main);
    }
}