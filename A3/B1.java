import java.nio.ByteBuffer;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Random;

public class B1 {
	MessageDigest m;

	public B1() throws NoSuchAlgorithmException {
		m = MessageDigest.getInstance("MD5");
	}

	public int getTruncated(int vk, int bits) {
		byte[] bytes = ByteBuffer.allocate(4).putInt(vk).array();
		int digest = ByteBuffer.wrap(m.digest(bytes)).getInt();
		bits = (int) Math.pow(2, bits) - 1;
		digest = digest & bits;
		return digest;
	}

	public static void main(String[] args) throws NoSuchAlgorithmException {
		Random r = new Random();
		B1 b = new B1();

		for (int bits = 20; bits < 21; bits++) {
			int nrBreaks = 0;
			for (int i = 0; i < 1000; i++) {
				int v = r.nextInt(2) << 16;
				int k = r.nextInt(65536);
				int digest = b.getTruncated(v + k, bits);
				System.out.println(digest);

				for (int j = 0; j <= 65535; j++) {
					int d0 = b.getTruncated(j + 0, bits);
					int d1 = b.getTruncated(j + (1 << 16), bits);
					if (digest == d1 || digest == d0) {
						nrBreaks++;
						break;
					}
				}
			}
			System.out.println("Simulated probability(" + bits + "): " + nrBreaks/10 + "%");
		}

	}

}
