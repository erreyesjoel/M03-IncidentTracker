package com.example.incidenttrackerauditor;

import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import java.io.IOException;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    // Tag per filtrar al Logcat
    private static final String TAG = "AUDIT_JOEL";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Busquem el botó pel seu ID (el que farem servir amb Appium després)
        // Assegura't que al teu activity_main.xml el botó es digui "ioc_button" o similar
        Button auditButton = findViewById(R.id.ioc_button);

        if (auditButton != null) {
            auditButton.setOnClickListener(v -> {
                Toast.makeText(MainActivity.this, "Connectant amb Django...", Toast.LENGTH_SHORT).show();
                fetchIncidents();
            });
        } else {
            // Si el botó és nul, fem la crida directament al carregar per testar
            fetchIncidents();
        }
    }

    private void fetchIncidents() {
        // IP 10.0.2.2 és el pont cap al localhost del teu PC des de l'emulador
        String url = "http://10.0.2.2:8002/api/incidents/";

        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder()
                .url(url)
                .build();

        Log.d(TAG, "Iniciant petició a: " + url);

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                // Si falla, ho veurem en vermell al Logcat
                Log.e(TAG, "ERROR DE CONNEXIÓ: " + e.getMessage());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    String jsonData = response.body().string();

                    // Aquesta és l'evidència clau: aquí sortirà el nom
                    Log.i(TAG, "JSON REBUT AMB ÈXIT: " + jsonData);

                    // Si vols mostrar el JSON a la pantalla del mòbil:
                    runOnUiThread(() -> {
                        // Opcional: Toast o actualitzar un TextView
                        Toast.makeText(MainActivity.this, "Dades rebudes!", Toast.LENGTH_LONG).show();
                    });
                } else {
                    Log.e(TAG, "Error del servidor: " + response.code());
                }
            }
        });
    }
}