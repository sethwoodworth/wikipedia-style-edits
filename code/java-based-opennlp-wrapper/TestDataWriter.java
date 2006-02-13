import com.megginson.sax.DataProcessingWriter;

public class TestDataWriter
{

    public static void main (String args[])
	throws Exception
    {
	DataProcessingWriter w = new DataProcessingWriter();

	w.startDocument();
	w.startElement("foo");
	w.dataElement("bar", "1");
	w.dataElement("bar", "2");
	w.startElement("hack");
	w.dataElement("fubar", "zing");
	w.endElement("hack");
	w.dataElement("bar", "3");
	w.endElement("foo");
	w.endDocument();
    }

}
