#pragma once

#include <Arduino.h>
#include <stdlib.h>

struct messages
{
    long long ts_ms;
    String device_name;
    String description;
    float value;
    String unit;
    int msgIdx;
};

static messages tempSensorESP32
{
    .ts_ms = 0,
    .device_name = "esp32",
    .description = "onBoardTemp",
    .value = 0.0,
    .unit = "C",
    .msgIdx = 1
};
