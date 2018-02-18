package jSCRDRtagger;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.HashMap;
import java.util.List;

/**
 * @author DatQuocNguyen
 * 
 */
public class RDRPOSTagger
{
	public Node root;

	public RDRPOSTagger()
	{
	}

	public RDRPOSTagger(Node node)
	{
		root = node;
	}

	public void constructTreeFromRulesFile(String rulesFilePath)
		throws IOException
	{
		BufferedReader buffer = new BufferedReader(new InputStreamReader(
			new FileInputStream(new File(rulesFilePath)), "UTF-8"));
		String line = buffer.readLine();

		this.root = new Node(new FWObject(false), "NN", null, null, null, 0);

		Node currentNode = this.root;
		int currentDepth = 0;

		for (; (line = buffer.readLine()) != null;) {
			int depth = 0;
			for (int i = 0; i <= 6; i++) { // Supposed that the maximum
											// exception level is up to 6.
				if (line.charAt(i) == '\t')
					depth += 1;
				else
					break;
			}

			line = line.trim();
			if (line.length() == 0)
				continue;

			if (line.contains("cc:"))
				continue;

			FWObject condition = Utils
				.getCondition(line.split(" : ")[0].trim());
			String conclusion = Utils.getConcreteValue(line.split(" : ")[1]
				.trim());

			Node node = new Node(condition, conclusion, null, null, null, depth);

			if (depth > currentDepth) {
				currentNode.setExceptNode(node);
			}
			else if (depth == currentDepth) {
				currentNode.setIfnotNode(node);
			}
			else {
				while (currentNode.depth != depth)
					currentNode = currentNode.fatherNode;
				currentNode.setIfnotNode(node);
			}
			node.setFatherNode(currentNode);

			currentNode = node;
			currentDepth = depth;
		}
		buffer.close();
	}

	public Node findFiredNode(FWObject object)
	{
		Node currentN = root;
		Node firedN = null;
		while (true) {
			if (currentN.satisfy(object)) {
				firedN = currentN;
				if (currentN.exceptNode == null) {
					break;
				}
				else {
					currentN = currentN.exceptNode;
				}
			}
			else {
				if (currentN.ifnotNode == null) {
					break;
				}
				else {
					currentN = currentN.ifnotNode;
				}
			}

		}

		return firedN;
	}

	public String tagInitializedSentence(String inInitializedSentence)
	{
		StringBuilder sb = new StringBuilder();
		List<WordTag> wordtags = Utils.getWordTagList(inInitializedSentence);
		int size = wordtags.size();
		for (int i = 0; i < size; i++) {
			FWObject object = Utils.getObject(wordtags, size, i);
			Node firedNode = findFiredNode(object);
			if (firedNode.depth > 0)
				sb.append(wordtags.get(i).word + "/" + firedNode.conclusion
					+ " ");
			else {
				// Fired at root, return initialized tag.
				sb.append(wordtags.get(i).word + "/" + wordtags.get(i).tag
					+ " ");
			}
		}
		return sb.toString();
	}

	public void tagInitializedCorpus(String inInitializedFilePath)
		throws IOException
	{
		BufferedReader buffer = new BufferedReader(new InputStreamReader(
			new FileInputStream(new File(inInitializedFilePath)), "UTF-8"));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(
			new FileOutputStream(inInitializedFilePath + ".TAGGED"), "UTF-8"));

		for (String line; (line = buffer.readLine()) != null;) {
			line = line.replace("“", "''").replace("”", "''")
				.replace("\"", "''").trim();
			if (line.length() == 0) {
				bw.write("\n");
				continue;
			}
			bw.write(tagInitializedSentence(line) + "\n");
		}
		buffer.close();
		bw.close();
	}

	public String tagVnSentence(HashMap<String, String> FREQDICT,
		String sentence)
		throws IOException
	{
		StringBuilder sb = new StringBuilder();

		String line = sentence.trim();
		if (line.length() == 0) {
			return "\n";
		}

		List<WordTag> wordtags = InitialTagger.VnInitTagger4Sentence(FREQDICT,
			line);

		int size = wordtags.size();
		for (int i = 0; i < size; i++) {
			FWObject object = Utils.getObject(wordtags, size, i);
			Node firedNode = findFiredNode(object);
			sb.append(wordtags.get(i).word + "/" + firedNode.conclusion + " ");
		}

		return sb.toString();
	}

	public void tagVnCorpus(HashMap<String, String> FREQDICT,
		String inRawFilePath)
		throws IOException
	{
		BufferedReader buffer = new BufferedReader(new InputStreamReader(
			new FileInputStream(new File(inRawFilePath)), "UTF-8"));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(
			new FileOutputStream(inRawFilePath + ".TAGGED"), "UTF-8"));
		for (String line; (line = buffer.readLine()) != null;) {
			bw.write(tagVnSentence(FREQDICT, line) + "\n");
		}
		buffer.close();
		bw.close();
	}

	public String tagEnSentence(HashMap<String, String> FREQDICT,
		String sentence)
		throws IOException
	{
		StringBuilder sb = new StringBuilder();

		String line = sentence.trim();
		if (line.length() == 0) {
			return "\n";
		}

		List<WordTag> wordtags = InitialTagger.EnInitTagger4Sentence(FREQDICT,
			line);

		int size = wordtags.size();
		for (int i = 0; i < size; i++) {
			FWObject object = Utils.getObject(wordtags, size, i);
			Node firedNode = findFiredNode(object);
			sb.append(wordtags.get(i).word + "/" + firedNode.conclusion + " ");
		}
		return sb.toString();
	}

	public void tagEnCorpus(HashMap<String, String> FREQDICT,
		String inRawFilePath)
		throws IOException
	{
		BufferedReader buffer = new BufferedReader(new InputStreamReader(
			new FileInputStream(new File(inRawFilePath)), "UTF-8"));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(
			new FileOutputStream(inRawFilePath + ".TAGGED"), "UTF-8"));
		for (String line; (line = buffer.readLine()) != null;) {
			bw.write(tagEnSentence(FREQDICT, line) + "\n");
		}
		buffer.close();
		bw.close();
	}

	public String tagSentence(HashMap<String, String> FREQDICT, String sentence)
		throws IOException
	{
		StringBuilder sb = new StringBuilder();
		String line = sentence.trim();
		if (line.length() == 0) {
			return "\n";
		}

		List<WordTag> wordtags = InitialTagger.InitTagger4Sentence(FREQDICT,
			line);

		int size = wordtags.size();
		for (int i = 0; i < size; i++) {
			FWObject object = Utils.getObject(wordtags, size, i);
			Node firedNode = findFiredNode(object);
			if (firedNode.depth > 0)
				sb.append(wordtags.get(i).word + "/" + firedNode.conclusion
					+ " ");
			else {
				// Fired at root, return initialized tag.
				sb.append(wordtags.get(i).word + "/" + wordtags.get(i).tag
					+ " ");
			}
		}
		return sb.toString();
	}

	public void tagCorpus(HashMap<String, String> FREQDICT, String inRawFilePath)
		throws IOException
	{
		BufferedReader buffer = new BufferedReader(new InputStreamReader(
			new FileInputStream(new File(inRawFilePath)), "UTF-8"));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(
			new FileOutputStream(inRawFilePath + ".TAGGED"), "UTF-8"));
		for (String line; (line = buffer.readLine()) != null;) {
			bw.write(tagSentence(FREQDICT, line) + "\n");
		}
		buffer.close();
		bw.close();

	}

	public static void printHelp()
	{
		System.out.println("\n===== Usage =====");
		System.out
			.println("\n=> To use a pre-trained RDRPOSTagger model for POS tagging on a raw text corpus:");
		System.out
			.println("\njava RDRPOSTagger PATH-TO-PRETRAINED-MODEL PATH-TO-LEXICON PATH-TO-RAW-TEXT-CORPUS");
		System.out
			.println("\nExample 1: java RDRPOSTagger ../Models/MORPH/German.RDR ../Models/MORPH/German.DICT ../data/GermanRawTest");
		System.out
			.println("\n=> RDRPOSTagger has an additional parameter specialized for POS tagging in English and Vietnamse:");
		System.out
			.println("\nExample 2: java RDRPOSTagger en ../Models/POS/English.RDR ../Models/POS/English.DICT ../data/en/rawTest");
		System.out
			.println("\nExample 3: java RDRPOSTagger vn ../Models/POS/Vietnamese.RDR ../Models/POS/Vietnamese.DICT ../data/vn/rawTest");
		
		System.out.println("\n=> In case of using an external initial POS tagger:");
		System.out
			.println("\njava RDRPOSTagger ex PATH-TO-TRAINED-MODEL PATH-TO-TEST-CORPUS-INITIALIZED-BY-EXTERNAL-TAGGER");
		System.out
			.println("\nExample 4: java RDRPOSTagger ex ../data/initTrain.RDR ../data/initTest");
		System.out
			.println("\nFind the full usage at http://rdrpostagger.sourceforge.net !");

	}

	public static void run(String args[])
		throws IOException
	{
		try {
			if (args.length == 4) {
				if (args[0].equals("en") || args[0].equals("vn")) {
					RDRPOSTagger tree = new RDRPOSTagger();
					System.out.println("\nRead a POS tagging model from: "
						+ args[1]);
					tree.constructTreeFromRulesFile(args[1]);
					System.out.println("Read a lexicon from: " + args[2]);
					HashMap<String, String> FREQDICT = Utils
						.getDictionary(args[2]);
					if (args[0].equals("en")) {
						System.out.println("Perform English POS tagging on:"
							+ args[3]);
						tree.tagEnCorpus(FREQDICT, args[3]);
					}
					else {
						System.out.println("Perform Vietnamese POS tagging on:"
							+ args[3]);
						tree.tagVnCorpus(FREQDICT, args[3]);
					}
				}
				else {
					printHelp();
				}
			}
			else if (args.length == 3) {
				if (args[0].equals("ex")) {
					RDRPOSTagger tree = new RDRPOSTagger();
					System.out.println("\nRead a POS tagging model from: "
						+ args[1]);
					tree.constructTreeFromRulesFile(args[1]);
					System.out.println("Perform POS tagging on:" + args[2]);
					tree.tagInitializedCorpus(args[2]);
				}
				else {
					RDRPOSTagger tree = new RDRPOSTagger();
					System.out.println("\nRead a POS tagging model from: "
						+ args[0]);
					tree.constructTreeFromRulesFile(args[0]);
					System.out.println("Read a lexicon from: " + args[1]);
					HashMap<String, String> FREQDICT = Utils
						.getDictionary(args[1]);
					System.out.println("Perform POS tagging on:" + args[2]);
					tree.tagCorpus(FREQDICT, args[2]);
				}
			}
			else {
				printHelp();
			}
		}
		catch (Exception e) {
			System.out.println(e.getMessage());
			printHelp();
		}

	}

	public static void main(String[] args)
		throws IOException
	{
		run(args);
	}
}
