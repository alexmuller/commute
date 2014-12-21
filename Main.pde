import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Map;

static int ROW_GAP = 5;
static int ROW_HEIGHT = 10;

static int WINDOW_WIDTH = 400;
static int WINDOW_HEIGHT = 200;

Map<String, Mode> modeMap = new HashMap<String, Mode>();

Commute makeCommute(String timeOfDay, JSONObject datum) {
    JSONArray rawSegments = datum.getJSONArray(timeOfDay);
    ArrayList<Segment> segments = new ArrayList<Segment>();

    for (int j = 0; j < rawSegments.size(); j++) {
        JSONObject rawSegment = rawSegments.getJSONObject(j);
        Segment segment = new Segment(
            rawSegment.getInt("duration"),
            modeMap.get(rawSegment.getString("mode")));
        segments.add(segment);
    }

    Commute commute = new Commute(segments);
    return commute;
}

void setup() {
    size(WINDOW_WIDTH, WINDOW_HEIGHT);
    background(240);
    noStroke();

    int xPos = ROW_HEIGHT,
        yPos = ROW_HEIGHT;

    // Colour definitions for London Buses and London Underground are from
    // Transport for London's colour standard:
    // http://www.tfl.gov.uk/cdn/static/cms/documents/tfl-colour-standard.pdf
    modeMap.put("bus", new Mode("Bus", color(220, 36, 31)));
    modeMap.put("tube", new Mode("Tube", color(0, 25, 168)));
    modeMap.put("walking", new Mode("Walking", color(130, 130, 130)));
    modeMap.put("cycling", new Mode("Cycling", color(252, 76, 2)));

    for (Map.Entry entry : modeMap.entrySet()) {
        Mode m = modeMap.get(entry.getKey());

        fill(m.getColour());
        rect(xPos, yPos, 10, 10);

        fill(0, 0, 0);
        textSize(10);
        float width = textWidth(m.getName()) + 40;
        text(m.getName(), xPos + 15, yPos + 9);

        xPos += width;
    }

    xPos = ROW_HEIGHT;
    yPos += 20;

    fill(150, 150, 150);
    rect(xPos, yPos, WINDOW_WIDTH - (ROW_HEIGHT * 2), 1);

    yPos += 10;

    JSONArray data = loadJSONArray("example.json");

    ArrayList<Day> days = new ArrayList<Day>();

    SimpleDateFormat dateformat = new SimpleDateFormat("yyyy-MM-dd");

    for (int i = 0; i < data.size(); i++) {
        // Iterate over each day
        JSONObject datum = data.getJSONObject(i);
        String dateString = datum.getString("date");
        Date date = new Date();

        try {
            date = dateformat.parse(dateString);
        } catch(ParseException e) {
            println("Could not parse date from JSON: " + dateString);
        }

        Commute morningCommute = makeCommute("morning", datum);
        Commute eveningCommute = makeCommute("evening", datum);
        Day day = new Day(date, morningCommute, eveningCommute);

        day.draw(xPos, yPos);

        yPos = yPos + (ROW_HEIGHT + ROW_GAP);
    }

    noLoop();
}
