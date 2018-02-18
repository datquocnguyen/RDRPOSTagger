package jSCRDRtagger;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.regex.Pattern;

/**
 * @author DatQuocNguyen
 * 
 */
public class InitialTagger
{
	private static final Pattern QUOTATION = Pattern.compile("(“)|(”)|(\")");

	public static List<WordTag> InitTagger4Sentence(
		HashMap<String, String> DICT, String sentence)
	{
		List<WordTag> wordtags = new ArrayList<WordTag>();

		for (String word : sentence.split("\\s+")) {
			if (QUOTATION.matcher(word).find()) {
				wordtags.add(new WordTag("''", DICT.get("''")));
				continue;
			}

			String tag = "";
			String lowerW = word.toLowerCase();
			if (DICT.containsKey(word))
				tag = DICT.get(word);
			else if (DICT.containsKey(lowerW))
				tag = DICT.get(lowerW);
			else {
				if (CD.matcher(word).find()) {
					tag = DICT.get("TAG4UNKN-NUM");
				}
				else {
					String suffixL2 = null, suffixL3 = null, suffixL4 = null, suffixL5 = null;

					int wordLength = word.length();
					if (wordLength >= 4) {
						suffixL2 = ".*" + word.substring(wordLength - 2);
						suffixL3 = ".*" + word.substring(wordLength - 3);
					}
					if (wordLength >= 5) {
						suffixL4 = ".*" + word.substring(wordLength - 4);
					}
					if (wordLength >= 6) {
						suffixL5 = ".*" + word.substring(wordLength - 5);
					}

					if (DICT.containsKey(suffixL5)) {
						tag = DICT.get(suffixL5);
					}
					else if (DICT.containsKey(suffixL4)) {
						tag = DICT.get(suffixL4);
					}
					else if (DICT.containsKey(suffixL3)) {
						tag = DICT.get(suffixL3);
					}
					else if (DICT.containsKey(suffixL2)) {
						tag = DICT.get(suffixL2);
					}
					else if (Character.isUpperCase(word.codePointAt(0)))
						tag = DICT.get("TAG4UNKN-CAPITAL");
					else
						tag = DICT.get("TAG4UNKN-WORD");
				}
			}

			wordtags.add(new WordTag(word, tag));
		}
		return wordtags;
	}

	private static final Pattern CD = Pattern.compile("[0-9]+");
	private static final Pattern JJ1 = Pattern.compile("([0-9]+-)|(-[0-9]+)");
	private static final Pattern JJ2 = Pattern
		.compile("(^[Ii]nter.*)|(^[nN]on.*)|(^[Dd]is.*)|(^[Aa]nti.*)");
	private static final Pattern JJ3 = Pattern
		.compile("(.*ful$)|(.*ous$)|(.*ble$)|(.*ic$)|(.*ive$)|(.*est$)|(.*able$)|(.*al$)");

	private static final Pattern NN = Pattern
		.compile("(.*ness$)|(.*ment$)|(.*ship$)|(^[Ee]x-.*)|(^[Ss]elf-.*)");
	private static final Pattern NNS = Pattern.compile(".*s$");
	private static final Pattern VBG = Pattern.compile(".*ing$");
	private static final Pattern VBN = Pattern.compile(".*ed$");
	private static final Pattern RB = Pattern.compile(".*ly$");

	public static List<WordTag> EnInitTagger4Sentence(
		HashMap<String, String> DICT, String sentence)
	{
		List<WordTag> wordtags = new ArrayList<WordTag>();

		for (String word : sentence.split("\\s+")) {
			if (QUOTATION.matcher(word).find()) {
				wordtags.add(new WordTag("''", DICT.get("''")));
				continue;
			}

			String tag = "";
			String lowerW = word.toLowerCase();
			if (DICT.containsKey(word))
				tag = DICT.get(word);
			else if (DICT.containsKey(lowerW))
				tag = DICT.get(lowerW);
			else {
				if (JJ1.matcher(word).find())
					tag = "JJ";
				else if (CD.matcher(word).find())
					tag = "CD";
				else if (NN.matcher(word).find())
					tag = "NN";
				else if (NNS.matcher(word).find()
					&& Character.isLowerCase(word.charAt(0)))
					tag = "NNS";
				else if (Character.isUpperCase(word.charAt(0)))
					tag = "NNP";
				else if (JJ2.matcher(word).find())
					tag = "JJ";
				else if (VBG.matcher(word).find() && !word.contains("-"))
					tag = "VBG";
				else if (VBN.matcher(word).find() && !word.contains("-"))
					tag = "VBN";
				else if (word.contains("-") || JJ3.matcher(word).find())
					tag = "JJ";
				else if (RB.matcher(word).find())
					tag = "RB";
				else
					tag = "NN";
			}

			wordtags.add(new WordTag(word, tag));
		}
		return wordtags;
	}

	public static void EnInitTagger4Corpus(HashMap<String, String> DICT,
		String inputRawFilePath, String outFilePath)
		throws IOException
	{
		BufferedReader buffer = new BufferedReader(new InputStreamReader(
			new FileInputStream(new File(inputRawFilePath)), "UTF-8"));

		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(
			new FileOutputStream(outFilePath), "UTF-8"));

		for (String line; (line = buffer.readLine()) != null;) {
			line = line.trim();
			if (line.length() == 0) {
				bw.write("\n");
				continue;
			}
			for (WordTag st : EnInitTagger4Sentence(DICT, line))
				bw.write(st.word + "/" + st.tag + " ");
			bw.write("\n");
		}

		buffer.close();
		bw.close();
	}

	public static List<WordTag> VnInitTagger4Sentence(
		HashMap<String, String> DICT, String sentence)
	{
		List<WordTag> wordtags = new ArrayList<WordTag>();

		for (String word : sentence.split("\\s+")) {
			if (QUOTATION.matcher(word).find()) {
				wordtags.add(new WordTag("''", DICT.get("''")));
				continue;
			}

			String lowerW = word.toLowerCase();
			String tag = "";
			if (DICT.containsKey(word)) {
				tag = DICT.get(word);
			}
			else if (DICT.containsKey(lowerW)) {
				tag = DICT.get(lowerW);
			}
			else {
				if (CD.matcher(word).find()) {
					tag = DICT.get("TAG4UNKN-NUM");
				}
				else if (word.length() == 1
					&& Character.isUpperCase(word.charAt(0))) {
					tag = "Y";
				}
				else if (Utils.isAbbre(word)) {
					tag = "Ny";
				}
				else if (Utils.isVnProperNoun(word)) {
					tag = "Np";
				}
				else {
					String suffixL2 = null, suffixL3 = null, suffixL4 = null, suffixL5 = null;

					int wordLength = word.length();
					if (wordLength >= 4) {
						suffixL2 = ".*" + word.substring(wordLength - 2);
						suffixL3 = ".*" + word.substring(wordLength - 3);
					}
					if (wordLength >= 5) {
						suffixL4 = ".*" + word.substring(wordLength - 4);
					}
					if (wordLength >= 6) {
						suffixL5 = ".*" + word.substring(wordLength - 5);
					}

					if (DICT.containsKey(suffixL5)) {
						tag = DICT.get(suffixL5);
					}
					else if (DICT.containsKey(suffixL4)) {
						tag = DICT.get(suffixL4);
					}
					else if (DICT.containsKey(suffixL3)) {
						tag = DICT.get(suffixL3);
					}
					else if (DICT.containsKey(suffixL2)) {
						tag = DICT.get(suffixL2);
					}
					else
						tag = DICT.get("TAG4UNKN-WORD");
				}

			}

			wordtags.add(new WordTag(word, tag));
		}
		return wordtags;
	}

	public static void VnInitTagger4Corpus(HashMap<String, String> DICT,
		String inputRawFilePath, String outFilePath)
		throws IOException
	{
		BufferedReader buffer = new BufferedReader(new InputStreamReader(
			new FileInputStream(new File(inputRawFilePath)), "UTF-8"));

		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(
			new FileOutputStream(outFilePath), "UTF-8"));

		for (String line; (line = buffer.readLine()) != null;) {
			line = line.trim();
			if (line.length() == 0) {
				bw.write("\n");
				continue;
			}
			for (WordTag st : VnInitTagger4Sentence(DICT, line))
				bw.write(st.word + "/" + st.tag + " ");
			bw.write("\n");
		}

		buffer.close();
		bw.close();
	}
}
