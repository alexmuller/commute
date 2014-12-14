import java.text.SimpleDateFormat;
import java.util.Date;

class Day {
    Date date;
    Commute commute;
    SimpleDateFormat outputDateFormat;

    Day(Date tempDate, Commute tempCommute) {
        date = tempDate;
        commute = tempCommute;
        outputDateFormat = new SimpleDateFormat("EEE d MMM yyyy");
    }

    void draw(int xPos, int yPos) {
        fill(0, 0, 0);
        textSize(10);
        text(outputDateFormat.format(date), xPos, yPos + 9);
        commute.draw(xPos + 100, yPos);
    }
}
