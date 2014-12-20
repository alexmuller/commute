import java.text.SimpleDateFormat;
import java.util.Date;

class Day {
    Date date;
    Commute morningCommute;
    Commute eveningCommute;
    SimpleDateFormat outputDateFormat;

    Day(Date tempDate, Commute tempMorningCommute, Commute tempEveningCommute) {
        date = tempDate;
        morningCommute = tempMorningCommute;
        eveningCommute = tempEveningCommute;
        outputDateFormat = new SimpleDateFormat("EEE d MMM yyyy");
    }

    void draw(int xPos, int yPos) {
        fill(0, 0, 0);
        textSize(10);
        text(outputDateFormat.format(date), xPos, yPos + 9);
        xPos += 100;
        morningCommute.draw(xPos, yPos);

        int duration = morningCommute.duration(),
            roundedDuration = ((duration + 99) / 100) * 100;

        xPos += roundedDuration;
        eveningCommute.draw(xPos, yPos);
    }
}
