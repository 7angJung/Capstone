package com.example.test1;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.Window;
import android.view.WindowManager;

public class SplashActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 타이틀바를 제거합니다.
        requestWindowFeature(Window.FEATURE_NO_TITLE);

        // 상태바를 숨깁니다 (전체 화면 모드로 만듭니다).
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);

        // 스플래시 화면을 위한 레이아웃 설정
        setContentView(R.layout.activity_splash);

        // 2초 후 메인 액티비티로 이동
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                // 메인 액티비티 시작
                Intent mainIntent = new Intent(SplashActivity.this, MainActivity.class);
                SplashActivity.this.startActivity(mainIntent);
                SplashActivity.this.finish();
            }
        }, 3500); // 2000ms = 2초
    }
}
