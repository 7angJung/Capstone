package com.example.test1;

import android.Manifest;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.widget.Button;
import android.widget.Toast;
import android.widget.Toolbar;

import androidx.activity.EdgeToEdge;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;

public class MainActivity extends AppCompatActivity {

    private ActivityResultLauncher<String> requestPermissionLauncher;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);

        // 인셋 적용
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.button_camera), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // 권한 요청 결과 처리
        requestPermissionLauncher = registerForActivityResult(new ActivityResultContracts.RequestPermission(), isGranted -> {
            if (isGranted) {
                // 권한이 부여되었을 때 카메라 앱 실행
                launchCamera();
            } else {
                // 권한이 거부되었을 때 사용자에게 토스트 메시지 제공
                Toast.makeText(MainActivity.this, "카메라 권한이 필요합니다.", Toast.LENGTH_SHORT).show();
            }
        });

        // 카메라 버튼 설정
        Button cameraButton = findViewById(R.id.button_camera);
        cameraButton.setOnClickListener(v -> requestCameraPermission());

        // 점자 변환 버튼 설정
        Button brailleConversionButton = findViewById(R.id.button_convert_to_braille);
        brailleConversionButton.setOnClickListener(v -> startBrailleConversionActivity());
    }
    private void requestCameraPermission() {
        if (ContextCompat.checkSelfPermission(
                this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
            // 권한이 이미 부여되었다면 카메라 앱 실행
            launchCamera();
        } else {
            // 권한이 부여되지 않았다면 권한 요청
            requestPermissionLauncher.launch(Manifest.permission.CAMERA);
        }
    }

    private void startBrailleConversionActivity() {
        // 점자 변환 액티비티 실행
        Intent intent = new Intent(MainActivity.this, BraileActivity.class);
        startActivity(intent);
    }
    private Uri saveImageInExternalStorage(Bitmap bitmap) {
        ContentValues values = new ContentValues();
        values.put(MediaStore.Images.Media.DISPLAY_NAME, "image_" + System.currentTimeMillis() + ".jpg");
        values.put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg");
        values.put(MediaStore.Images.Media.RELATIVE_PATH, Environment.DIRECTORY_PICTURES + File.separator + "YourAppName");

        Uri uri = getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values);
        if (uri != null) {
            try (OutputStream outputStream = getContentResolver().openOutputStream(uri)) {
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, outputStream);
                outputStream.flush();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        return uri;
    }
    private void launchCamera() {
        // 이미지 파일을 저장할 Uri 생성
        Uri imageUri = createImageUri();
        if (imageUri != null) {
            Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, imageUri); // 카메라 앱에 Uri 전달
            if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
                startActivity(takePictureIntent);
            }
        }
    }
    private Uri createImageUri() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            ContentValues values = new ContentValues();
            values.put(MediaStore.Images.Media.DISPLAY_NAME, "image_" + System.currentTimeMillis());
            values.put(MediaStore.Images.Media.MIME_TYPE, "image/jpeg");
            values.put(MediaStore.Images.Media.RELATIVE_PATH, Environment.DIRECTORY_PICTURES + File.separator + "YourAppName");
            return getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values);
        } else {
            // Android 9(Pie) 이하 버전을 위한 코드 (권장하지 않음, 가능하면 FileProvider 사용을 고려하세요)
            File imagePath = new File(Environment.getExternalStorageDirectory() + File.separator + "YourAppName");
            imagePath.mkdirs();
            File image = new File(imagePath, "image_" + System.currentTimeMillis() + ".jpg");
            return Uri.fromFile(image);
        }
    }


}
