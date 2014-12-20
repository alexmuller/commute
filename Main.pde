import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Map;

static int ROW_HEIGHT = 10;

void setup() {
    size(400, 200);
    background(240);
    noStroke();

    // Colour definitions for London Buses and London Underground are from
    // Transport for London's colour standard:
    // http://www.tfl.gov.uk/cdn/static/cms/documents/tfl-colour-standard.pdf
    Map<String, Mode> modeMap = new HashMap<String, Mode>();
    modeMap.put("bus", new Mode(color(220, 36, 31)));
    modeMap.put("tube", new Mode(color(0, 25, 168)));
    modeMap.put("walking", new Mode(color(130, 130, 130)));
    modeMap.put("cycling", new Mode(color(252, 76, 2)));
    // Temporary mode to visually separate commutes until this Processing
    // code supports morning and evening commutes.
    modeMap.put("spacer", new Mode(color(255, 255, 255)));

    JSONArray data = loadJSONArray("example.json");

    ArrayList<Day> days = new ArrayList<Day>();

    SimpleDateFormat dateformat = new SimpleDateFormat("yyyy-MM-dd");

    int xPos = ROW_HEIGHT,
        yPos = ROW_HEIGHT;

    for (int i = 0; i < data.size(); i++) {
        // Iterate over each day
        JSONObject datum = data.getJSONObject(i);
        JSONArray rawSegments = datum.getJSONArray("segments");
        ArrayList<Segment> segments = new ArrayList<Segment>();
        String dateString = datum.getString("date");
        Date date = new Date();

        try {
            date = dateformat.parse(dateString);
        } catch(ParseException e) {
            println("Could not parse date from JSON: " + dateString);
        }

        for (int j = 0; j < rawSegments.size(); j++) {
            JSONObject rawSegment = rawSegments.getJSONObject(j);
            Segment segment = new Segment(
                rawSegment.getInt("duration"),
                modeMap.get(rawSegment.getString("mode")));
            segments.add(segment);
        }

        Commute commute = new Commute(segments);
        Day day = new Day(date, commute);

        day.draw(xPos, yPos);

        yPos = yPos + (ROW_HEIGHT * 2);
    }

    noLoop();
}
