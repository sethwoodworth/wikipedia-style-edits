import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.InputStreamReader;
import java.nio.CharBuffer;
import java.util.Scanner;
import java.util.Vector;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import eos.TestEOS;

public class pain {
	public static void main(String[] strings) {
		Pattern terminate_this = Pattern.compile("\\S\\s+\\S+\\s+\\S");
		// Step 1: Create a scanner that will provide an iterator
		// over the \n\n-separated junk on stdin
		Scanner scanme = new Scanner(System.in).useDelimiter("\\n\\n+");
		while (scanme.hasNext()) {
			String lame = scanme.next();
			// Time to babysit MXTERMINATOR's bugs
			// if "lame" has only two or one or zero words in it, MXTERMINATOR will
			// print an extra "null" or two.
			Matcher m = terminate_this.matcher(lame);
			if (m.find()) {
				ByteArrayInputStream this_bytes = new ByteArrayInputStream(lame
						.getBytes());
				System.setIn(this_bytes);
				eos.TestEOS.main(strings); // This is right, except that
				// it prints the word "null" if there's only one input word
				// also, the startup cost is tremendous! :-(
				// Maybe I can do better by printing my own \n or something....
			} else
				System.out.println(lame);
		}
	}

}
