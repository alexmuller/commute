class Segment {
    int duration;
    Mode mode;

    Segment(int tempDuration, Mode tempMode) {
        duration = tempDuration;
        mode = tempMode;
    }

    int getDuration() {
        return duration;
    }

    void draw(int xPos, int yPos) {
        fill(mode.getColour());
        rect(xPos, yPos, duration, ROW_HEIGHT);
    }
}
