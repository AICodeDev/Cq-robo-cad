#pragma once




void inline setupButton() {

    pinMode(BUTTON_PIN, INPUT_PULLUP);
    pinMode(BUZZER_PIN, OUTPUT);
}

void onPress() {
    Serial.println("Button Pressed");
    TestMove();
    // Trigger buzzer or other logic here
}

void checkButtonPress() {
    bool current_reading = (digitalRead(BUTTON_PIN) == LOW);
    unsigned long now = millis();

    // 1. Only act if the state has changed (from not pressed to pressed)
    // 2. Only act if enough time has passed (debounce)
    if (current_reading && !button_was_pressed && (now - last_debounce_time > debounce_delay)) {
        onPress();
        last_debounce_time = now; // Update the timer
    }

    button_was_pressed = current_reading;
}

