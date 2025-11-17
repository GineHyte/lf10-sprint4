/**
 * Return a synchronous hex string of the requested length using secure random bytes.
 * Example: `randomHex(8)` -> "a3f4b1c2"
 * @param {number} length - number of hex characters to return (positive integer)
 * @returns {string} hex string of length `length`
 */
function randomHex(length = 8) {
    const n = Math.max(0, Math.floor(Number(length) || 0));
    if (n === 0) return '';
    const bytesNeeded = Math.ceil(n / 2);
    const rnd = crypto.getRandomValues(new Uint8Array(bytesNeeded));
    const hex = Array.from(rnd).map(b => b.toString(16).padStart(2, '0')).join('');
    return hex.slice(0, n);
}
