package B2;

import java.nio.ByteBuffer;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Random;

public class Probability {
	MessageDigest m;
	
	public Probability() throws NoSuchAlgorithmException {
		m = MessageDigest.getInstance("SHA-1");
	}
	
	public double getProbabilityFor(int length) throws NoSuchAlgorithmException {
		int nrTimesBroken = 0;
		int sampleSize = 666;
		//Given the length of the digest, investigate how many times out of samplesize the binding property is broken.
		//Larger sample size would be nice but this thing already takes forever bruh
		for (int i = 0; i < sampleSize; i++) {
			if(breakBindingProperty(length)){
				nrTimesBroken++;
			}
		}
		return (double)nrTimesBroken/sampleSize;
	}

	public boolean breakBindingProperty(int length) throws NoSuchAlgorithmException {
		Random rand = new Random();
		//Create x = h(v,k)
		int v = 0;
		int k = rand.nextInt(65536);
		int digest = getDigest(length, v, k);
		
		//Since the actual v = 0, in order to break the binding property we want to find an h(1,k)==h(0,k) where 0<=k<=65535 
		for(int i = 0; i <= 65535; i++) {
				if(digest == getDigest(length, 1, i)) {
					return true;
				}	
		}
		return false;
	}

	private int getDigest(int length, int v, int k) throws NoSuchAlgorithmException {
		k <<= 1; //Bitwise shift k one step
		int kv = k | v; //Appends v to the end of k
		byte[] input = ByteBuffer.allocate(4).putInt(kv).array(); //Allocate 4 bytes buffer, write kv into it and return the array.
		byte[] output = m.digest(input); //Get the SHA-1 digest as a byte array
		ByteBuffer wrapped = ByteBuffer.wrap(output); 
		int concatDigest = wrapped.getInt() & ((int)Math.pow(2, length) - 1); //Get the result as an int, then truncate to specified length.
		return concatDigest;
	}

	public static void main(String[] args) {
		try {
			Probability prob = new Probability();
			for(int i = 10; i < 23; i++) {
				double percentage = prob.getProbabilityFor(i) * 100;
				System.out.println("For digest length of: " + i+  ", the binding property breaks with a probability " + percentage + "%");
			}			
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		}
	}

	
}
