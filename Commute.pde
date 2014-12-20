class Commute {
    ArrayList<Segment> segments;

    Commute(ArrayList<Segment> tempSegments) {
        segments = tempSegments;
    }

    int duration() {
        int duration = 0;
        for (int i = 0; i < segments.size(); i++) {
            duration += segments.get(i).getDuration();
        }
        return duration;
    }

    void draw(int xPos, int yPos) {
        for (int i = 0; i < segments.size(); i++) {
            segments.get(i).draw(xPos, yPos);
            xPos += segments.get(i).getDuration();
        }
    }
}
