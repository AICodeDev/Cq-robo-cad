extern void MoveMotor1Pulses(
    long noOfPulseSteps,
    float initialTargetPPS,
    float minTargetPPS,
    float maxTargetPPS,
    int pwmRangeStart,
    int pwmRangeEnd
);
extern void MoveMotor2Pulses(
    long noOfPulseSteps,
    float initialTargetPPS,
    float minTargetPPS,
    float maxTargetPPS,
    int pwmRangeStart,
    int pwmRangeEnd
);
extern void CurveTurnCommand(float radius_cm, int direction);

void ForwardmovePulse(long targetPulses, int pps=500, int rangeStart=60, int rangeEnd=320)
{
   
    MoveMotor1Pulses(
        targetPulses,
        pps,
        MIN_PPS,
        MAX_PPS,
        rangeStart,
        rangeEnd
    );

    MoveMotor2Pulses(
        targetPulses,
        pps,
        MIN_PPS,
        MAX_PPS,
        rangeStart,
        rangeEnd
    );
}

void ExecuteRobotTour(const char* cmd)
{
    for (int i = 0; cmd[i] != '\0'; i++)
    {
        switch (cmd[i])
        {
            case 'F':
                ForwardmovePulse(FORWARD_CM*10*2.5);
                break;

            case 'R':
                CurveTurnCommand(25.0, -1);
                break;

            case 'L':
                CurveTurnCommand(25.0, +1);
                break;
        }
    }
}
