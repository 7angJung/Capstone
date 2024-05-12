package com.example.test1;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.HashMap;
import java.util.Map;

public class BraileActivity extends AppCompatActivity {

    private EditText editText;
    private Button convertButton;
    private TextView brailleTextView;

    // 점자 변환 맵
    private static final Map<Character, String> brailleMap = new HashMap<>();

    static {
        // 알파벳을 점자로 매핑
        brailleMap.put('a', "⠁");
        brailleMap.put('b', "⠃");
        brailleMap.put('c', "⠉");
        // 이하 알파벳 추가...
        brailleMap.put('z', "⠵");

        // 숫자를 점자로 매핑 (숫자 접두사 ⠼ 사용)
        brailleMap.put('1', "⠼⠁");
        brailleMap.put('2', "⠼⠃");
        // 이하 숫자 추가...
        brailleMap.put('0', "⠼⠚");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_braile); // 레이아웃 설정

        editText = findViewById(R.id.editText);
        convertButton = findViewById(R.id.convertButton);
        brailleTextView = findViewById(R.id.resultTextView);

        convertButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String inputText = editText.getText().toString();
                String brailleText = convertToBraille(inputText);
                brailleTextView.setText(brailleText);
            }
        });
    }

    private String convertToBraille(String text) {
        StringBuilder brailleBuilder = new StringBuilder();
        for (char character : text.toLowerCase().toCharArray()) {
            String brailleChar = brailleMap.get(character);
            if (brailleChar != null) {
                brailleBuilder.append(brailleChar);
            } else {
                brailleBuilder.append(character); // 매핑되지 않은 문자는 그대로 둠
            }
        }
        return brailleBuilder.toString();
    }
}
