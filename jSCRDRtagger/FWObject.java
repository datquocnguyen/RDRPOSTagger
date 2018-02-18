package jSCRDRtagger;

/**
 * @author DatQuocNguyen
 * 
 */

/*
 * Define a 5-word/tag window object to capture the context surrounding a word
 */
public class FWObject
{
	public String[] context;

	public FWObject(boolean check)
	{
		// Previous2ndWord, Previous2ndTag, PreviousWord, PreviousTag, Word,
		// Tag, NextWord, NextTag, Next2ndWord, Next2ndTag, 2-chars suffix,
		// 3-char suffix, 4-char suffix
		context = new String[13];
		if (check == true) {
			for (int i = 0; i < 10; i += 2) {
				context[i] = "<W>";
				context[i + 1] = "<T>";
			}
			context[10] = "<SFX>";
			context[11] = "<SFX>";
			context[12] = "<SFX>";
		}
	}
}
