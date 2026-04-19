function sha256(message) {
    function rightRotate(value, amount) {
        return (value >>> amount) | (value << (32 - amount)) >>> 0;
    }

    function Ch(x, y, z) { return (x & y) ^ (~x & z); }
    function Maj(x, y, z) { return (x & y) ^ (x & z) ^ (y & z); }
    function Sigma0(x) { return rightRotate(x, 2) ^ rightRotate(x, 13) ^ rightRotate(x, 22); }
    function Sigma1(x) { return rightRotate(x, 6) ^ rightRotate(x, 11) ^ rightRotate(x, 25); }
    function sigma0(x) { return rightRotate(x, 7) ^ rightRotate(x, 18) ^ (x >>> 3); }
    function sigma1(x) { return rightRotate(x, 17) ^ rightRotate(x, 19) ^ (x >>> 10); }

    let H = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ];

    const K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ];

    const encoder = new TextEncoder();
    let data = encoder.encode(message);

    const originalBitLen = data.length * 8;
    data = new Uint8Array([...data, 0x80]);
    while (data.length % 64 !== 56) {
        const newData = new Uint8Array(data.length + 1);
        newData.set(data);
        newData[data.length] = 0;
        data = newData;
    }
    const lenBuf = new ArrayBuffer(8);
    const lenView = new DataView(lenBuf);
    lenView.setUint32(0, Math.floor(originalBitLen / 0x100000000));
    lenView.setUint32(4, originalBitLen >>> 0);
    const lenBytes = new Uint8Array(lenBuf);
    const combined = new Uint8Array(data.length + 8);
    combined.set(data);
    combined.set(lenBytes, data.length);
    data = combined;

    for (let i = 0; i < data.length; i += 64) {
        const block = data.slice(i, i + 64);
        let W = new Array(64);
        for (let t = 0; t < 16; t++) {
            const off = t * 4;
            W[t] = (block[off] << 24) | (block[off + 1] << 16) | (block[off + 2] << 8) | block[off + 3];
        }
        for (let t = 16; t < 64; t++) {
            W[t] = (sigma1(W[t - 2]) + W[t - 7] + sigma0(W[t - 15]) + W[t - 16]) >>> 0;
        }

        let [a, b, c, d, e, f, g, h] = H;

        for (let t = 0; t < 64; t++) {
            const T1 = (h + Sigma1(e) + Ch(e, f, g) + K[t] + W[t]) >>> 0;
            const T2 = (Sigma0(a) + Maj(a, b, c)) >>> 0;
            h = g;
            g = f;
            f = e;
            e = (d + T1) >>> 0;
            d = c;
            c = b;
            b = a;
            a = (T1 + T2) >>> 0;
        }

        H[0] = (H[0] + a) >>> 0;
        H[1] = (H[1] + b) >>> 0;
        H[2] = (H[2] + c) >>> 0;
        H[3] = (H[3] + d) >>> 0;
        H[4] = (H[4] + e) >>> 0;
        H[5] = (H[5] + f) >>> 0;
        H[6] = (H[6] + g) >>> 0;
        H[7] = (H[7] + h) >>> 0;
    }

    function toHex(word) {
        return word.toString(16).padStart(8, '0');
    }
    return H.map(toHex).join('');
}
