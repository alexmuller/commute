class Day {
    Commute commute;

    Day(Commute tempCommute) {
        commute = tempCommute;
    }

    void draw(int xPos, int yPos) {
        commute.draw(xPos, yPos);
    }
}
