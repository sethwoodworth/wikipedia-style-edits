// DataProcessingWriter.java - XML writer for data-oriented files.

// This is a copy of DataWriter.java that has been modified
// by Asheesh Laroia.  Released into the public domain.  No rights reserved.

package com.megginson.sax;

import java.io.*; 
import java.io.Writer;
import java.util.Stack;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.XMLReader;


import opennlp.maxent.io.SuffixSensitiveGISModelReader;
import opennlp.tools.sentdetect.SentenceDetectorME;
// import opennlp.tools.sentdetect.EnglishSentenceDetectorME;
import com.megginson.sax.XMLWriter;

/**
 * Write data- or field-oriented XML.
 *
 * <p>This filter pretty-prints field-oriented XML without mixed content.
 * all added indentation and newlines will be passed on down
 * the filter chain (if any).</p>
 *
 * <p>In general, all whitespace in an XML document is potentially
 * significant, so a general-purpose XML writing tool like the
 * {@link com.megginson.sax.XMLWriter XMLWriter} class cannot
 * add newlines or indentation.</p>
 *
 * <p>There is, however, a large class of XML documents where information
 * is strictly fielded: each element contains either character data
 * or other elements, but not both.  For this special case, it is possible
 * for a writing tool to provide automatic indentation and newlines
 * without requiring extra work from the user.  Note that this class
 * will likely not yield appropriate results for document-oriented
 * XML like XHTML pages, which mix character data and elements together.</p>
 *
 * <p>This writer will automatically place each start tag on a new line,
 * optionally indented if an indent step is provided (by default, there
 * is no indentation).  If an element contains other elements, the end
 * tag will also appear on a new line with leading indentation.  Consider,
 * for example, the following code:</p>
 *
 * <pre>
 * DataProcessingWriter w = new DataProcessingWriter();
 *
 * w.setIndentStep(2);
 * w.startDocument();
 * w.startElement("Person");
 * w.dataElement("name", "Jane Smith");
 * w.dataElement("date-of-birth", "1965-05-23");
 * w.dataElement("citizenship", "US");
 * w.endElement("Person");
 * w.endDocument();
 * </pre>
 *
 * <p>This code will produce the following document:</p>
 *
 * <pre>
 * &lt;?xml version="1.0" standalone="yes"?>
 *
 * &lt;Person>
 *   &lt;name>Jane Smith&lt;/name>
 *   &lt;date-of-birth>1965-05-23&lt;/date-of-birth>
 *   &lt;citizenship>US&lt;/citizenship>
 * &lt;/Person>
 * </pre>
 *
 * <p>This class inherits from {@link com.megginson.sax.XMLWriter
 * XMLWriter}, and provides all of the same support for Namespaces.</p>
 *
 * @author David Megginson, david@megginson.com
 * @version 0.2
 * @see com.megginson.sax.XMLWriter
 */
public class DataProcessingWriter extends XMLWriter
{



    ////////////////////////////////////////////////////////////////////
    // Constructors.
    ////////////////////////////////////////////////////////////////////

    StringBuffer sb;
    boolean isInteresting = false;
    SentenceDetectorME sdetector;

    public void init_sentence_model(String model)  {
	try {
		sdetector = new SentenceDetectorME(
			new SuffixSensitiveGISModelReader(
				new File(model)
				).getModel());
		}
	catch (IOException whatever) {
		System.out.println("Abandon all hope for future plans.");
	}
	}

    public String detect_sentences(String input) {
	BufferedWriter output_buffer = new BufferedWriter(new StringWriter());
	try {
    StringBuffer para = new StringBuffer();
    BufferedReader inReader = new BufferedReader(new StringReader(input));
    for (String line = inReader.readLine(); line != null; line = inReader.readLine()) {
      if (line.equals("")) {
        if (para.length() != 0) {
          //System.err.println(para.toString());
          String[] sents = sdetector.sentDetect(para.toString());
          for (int si = 0, sn = sents.length; si < sn; si++) {
            output_buffer.write(sents[si] + "\n");
          }
        }
        output_buffer.write("\n");
        para.setLength(0);
      }
      else {
        para.append(line).append(" ");
      }
    }
    if (para.length() != 0) {
      String[] sents = sdetector.sentDetect(para.toString());
      for (int si = 0, sn = sents.length; si < sn; si++) {
        output_buffer.write(sents[si] + "\n");
      }
    }
		}
	catch (IOException whatever) {
		System.out.println("Abandon all hope for future plans.");
	}
	return output_buffer.toString();
}


    /**
     * Create a new data writer for standard output.
     */
    public DataProcessingWriter () // String model)
    {
	super();
	sb = new StringBuffer();
    }


    /**
     * Create a new data writer for standard output.
     *
     * <p>Use the XMLReader provided as the source of events.</p>
     *
     * @param xmlreader The parent in the filter chain.
     */
    public DataProcessingWriter (XMLReader xmlreader) // , String model)
    {
	super(xmlreader);
	sb = new StringBuffer();
    }


    /**
     * Create a new data writer for the specified output.
     *
     * @param writer The character stream where the XML document
     *        will be written.
     */
    public DataProcessingWriter (Writer writer)
    {
	super(writer);
	sb = new StringBuffer();
    }


    /**
     * Create a new data writer for the specified output.
     * <p>Use the XMLReader provided as the source of events.</p>
     *
     * @param xmlreader The parent in the filter chain.
     * @param writer The character stream where the XML document
     *        will be written.
     */
    public DataProcessingWriter (XMLReader xmlreader, Writer writer)
    {
	super(xmlreader, writer);
	sb = new StringBuffer();
    }



    ////////////////////////////////////////////////////////////////////
    // Accessors and setters.
    ////////////////////////////////////////////////////////////////////


    ////////////////////////////////////////////////////////////////////
    // Override methods from XMLWriter.
    ////////////////////////////////////////////////////////////////////


    /**
     * Reset the writer so that it can be reused.
     *
     * <p>This method is especially useful if the writer failed
     * with an exception the last time through.</p>
     *
     * @see com.megginson.sax.XMLWriter#reset
     */
    public void reset ()
    {
	depth = 0;
	state = SEEN_NOTHING;
	stateStack = new Stack();
	super.reset();
    }


    /**
     * Write a start tag.
     *
     * <p>Each tag will begin on a new line, and will be
     * indented by the current indent step times the number
     * of ancestors that the element has.</p>
     *
     * <p>The newline and indentation will be passed on down
     * the filter chain through regular characters events.</p>
     *
     * @param uri The element's Namespace URI.
     * @param localName The element's local name.
     * @param qName The element's qualified (prefixed) name.
     * @param atts The element's attribute list.
     * @exception org.xml.sax.SAXException If there is an error
     *            writing the start tag, or if a filter further
     *            down the chain raises an exception.
     * @see XMLWriter#startElement(String, String, String, Attributes)
     */
    public void startElement (String uri, String localName,
			      String qName, Attributes atts)
	throws SAXException
    {
	stateStack.push(SEEN_ELEMENT);
	state = SEEN_NOTHING;
        if (localName.equals("text")) {
		isInteresting = true;
	}
	super.startElement(uri, localName, qName, atts);
	depth++;
    }


    /**
     * Write an end tag.
     *
     * <p>If the element has contained other elements, the tag
     * will appear indented on a new line; otherwise, it will
     * appear immediately following whatever came before.</p>
     *
     * <p>The newline and indentation will be passed on down
     * the filter chain through regular characters events.</p>
     *
     * @param uri The element's Namespace URI.
     * @param localName The element's local name.
     * @param qName The element's qualified (prefixed) name.
     * @exception org.xml.sax.SAXException If there is an error
     *            writing the end tag, or if a filter further
     *            down the chain raises an exception.
     * @see XMLWriter#endElement(String, String, String)
     */
    public void endElement (String uri, String localName, String qName)
	throws SAXException
    {
	if (isInteresting && localName.equals("text")) {
		String result = sb.toString();
		// Now call some function ...
		// zomg
		result = "zomg";
		char [] processedChars = result.toCharArray();
		super.characters(processedChars, 0, processedChars.length);
		// finally, clear the string buffer
		sb = new StringBuffer();
	}
	depth--;
	super.endElement(uri, localName, qName);
	state = stateStack.pop();
	isInteresting = false;
    }


    /**
     * Write a empty element tag.
     *
     * <p>Each tag will appear on a new line, and will be
     * indented by the current indent step times the number
     * of ancestors that the element has.</p>
     *
     * <p>The newline and indentation will be passed on down
     * the filter chain through regular characters events.</p>
     *
     * @param uri The element's Namespace URI.
     * @param localName The element's local name.
     * @param qName The element's qualified (prefixed) name.
     * @param atts The element's attribute list.
     * @exception org.xml.sax.SAXException If there is an error
     *            writing the empty tag, or if a filter further
     *            down the chain raises an exception.
     * @see XMLWriter#emptyElement(String, String, String, Attributes)
     */
    public void emptyElement (String uri, String localName,
			      String qName, Attributes atts)
	throws SAXException
    {
	state = SEEN_ELEMENT;
	super.emptyElement(uri, localName, qName, atts);
    }


    /**
     * Write a sequence of characters.
     *
     * @param ch The characters to write.
     * @param start The starting position in the array.
     * @param length The number of characters to use.
     * @exception org.xml.sax.SAXException If there is an error
     *            writing the characters, or if a filter further
     *            down the chain raises an exception.
     * @see XMLWriter#characters(char[], int, int)
     */
    public void characters (char ch[], int start, int length)
	throws SAXException
    {
	state = SEEN_DATA;
	// logic: buffer all characters if we're interested
	if (isInteresting) {
		sb.append(ch, start, length);
	} // this had BETTER get flushed on the close tag
	else {
		super.characters(ch, start, length);
	}
    }


    ////////////////////////////////////////////////////////////////////
    // Constants.
    ////////////////////////////////////////////////////////////////////

    private final static Object SEEN_NOTHING = new Object();
    private final static Object SEEN_ELEMENT = new Object();
    private final static Object SEEN_DATA = new Object();



    ////////////////////////////////////////////////////////////////////
    // Internal state.
    ////////////////////////////////////////////////////////////////////

    private Object state = SEEN_NOTHING;
    private Stack stateStack = new Stack();

    private int depth = 0;

}

// end of DataProcessingWriter.java
