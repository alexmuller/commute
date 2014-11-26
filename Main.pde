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

    JSONArray data = loadJSONArray("example.json");

    ArrayList<Segment> segments = new ArrayList<Segment>();

    int initialXPos = 10,
        initialYPos = 10;

    for (int i = 0; i < data.size(); i++) {
        Segment segment = new Segment(
            data.getJSONObject(i).getInt("duration"),
            modeMap.get(data.getJSONObject(i).getString("mode")));
        segments.add(segment);
    }

    Commute commute = new Commute(segments);

    commute.draw(initialXPos, initialYPos);

    noLoop();
}
