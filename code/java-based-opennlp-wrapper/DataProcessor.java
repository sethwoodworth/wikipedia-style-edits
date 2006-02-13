// TestXMLWriter.java - Test harness for the XML writer.
// Usage: java -Dorg.xml.sax.driver="..." TestXMLWriter [files...]

// $Id: TestXMLWriter.java,v 1.1.1.1 2000/09/16 14:15:33 david Exp $

import java.io.FileReader;

import org.xml.sax.XMLReader;
//import org.xml.sax.parsers.SAXParser;
import org.xml.sax.InputSource;
import org.xml.sax.helpers.ParserAdapter;
import org.xml.sax.helpers.XMLReaderFactory;
import org.apache.*;
import com.megginson.sax.DataProcessingWriter;


/**
 * Simple test harness for XMLWriter.
 */
public class DataProcessor
{
    public static void main (String args[])
	throws Exception	// yech!
    {
//		System.setProperty(
//			"org.xml.sax.driver", "org.apache.xerces.parsers.SAXParser");



	if (args.length == 0) {
	    System.err.println("Usage java -Dorg.xml.sax.driver=<driver> DataProcessor model.gz");
	    System.exit(1);
	}

	String model = args[0];
	DataProcessingWriter w = new DataProcessingWriter(XMLReaderFactory.createXMLReader()); // , model);


	for (int i = 0; i < args.length; i++) {
	    w.parse(new InputSource(new FileReader("/dev/stdin")));
	}
    }
}

// end of TestXMLWriter.java
