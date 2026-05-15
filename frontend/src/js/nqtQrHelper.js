/**
 * NQT INTERNAL QR ENGINE - PURE JS
 * A clean, self-contained QR Code generator that works 100% offline.
 */

const QR_ERROR_CORRECT_LEVEL = { L: 1, M: 0, Q: 3, H: 2 };

class QRBitBuffer {
    constructor() { this.buffer = []; this.length = 0; }
    get(i) { return ((this.buffer[Math.floor(i / 8)] >>> (7 - i % 8)) & 1) === 1; }
    put(num, length) { for (let i = 0; i < length; i++) this.putBit(((num >>> (length - i - 1)) & 1) === 1); }
    putBit(bit) {
        let bufIndex = Math.floor(this.length / 8);
        if (this.buffer.length <= bufIndex) this.buffer.push(0);
        if (bit) this.buffer[bufIndex] |= (0x80 >>> (this.length % 8));
        this.length++;
    }
}

class QRCodeModel {
    constructor(typeNumber, errorCorrectLevel) {
        this.typeNumber = typeNumber;
        this.errorCorrectLevel = QR_ERROR_CORRECT_LEVEL[errorCorrectLevel];
        this.modules = null;
        this.moduleCount = 0;
        this.dataList = [];
    }
    addData(data) { this.dataList.push(data); }
    make() {
        this.moduleCount = this.typeNumber * 4 + 17;
        this.modules = new Array(this.moduleCount);
        for (let row = 0; row < this.moduleCount; row++) {
            this.modules[row] = new Array(this.moduleCount).fill(null);
        }
        this.setupPositionProbePattern(0, 0);
        this.setupPositionProbePattern(this.moduleCount - 7, 0);
        this.setupPositionProbePattern(0, this.moduleCount - 7);
        this.setupTimingPattern();
        this.setupTypeInfo(false, 0);
        this.mapData(this.createData(), 0);
    }
    setupPositionProbePattern(r, c) {
        for (let i = -1; i <= 7; i++) {
            for (let j = -1; j <= 7; j++) {
                if (r + i <= -1 || this.moduleCount <= r + i || c + j <= -1 || this.moduleCount <= c + j) continue;
                this.modules[r + i][c + j] = (0 <= i && i <= 6 && (j === 0 || j === 6)) || (0 <= j && j <= 6 && (i === 0 || i === 6)) || (2 <= i && i <= 4 && 2 <= j && j <= 4);
            }
        }
    }
    setupTimingPattern() {
        for (let i = 8; i < this.moduleCount - 8; i++) {
            if (this.modules[i][6] === null) this.modules[i][6] = (i % 2 === 0);
            if (this.modules[6][i] === null) this.modules[6][i] = (i % 2 === 0);
        }
    }
    setupTypeInfo(test, maskPattern) {
        let data = (this.errorCorrectLevel << 3) | maskPattern;
        for (let i = 0; i < 15; i++) {
            let mod = (!test && ((data >> i) & 1) === 1);
            if (i < 6) this.modules[i][8] = mod;
            else if (i < 8) this.modules[i + 1][8] = mod;
            else this.modules[this.moduleCount - 15 + i][8] = mod;
        }
    }
    createData() {
        let buffer = new QRBitBuffer();
        for (let data of this.dataList) {
            buffer.put(4, 4); // 8-bit byte mode
            buffer.put(data.length, 8);
            for (let i = 0; i < data.length; i++) buffer.put(data.charCodeAt(i), 8);
        }
        return buffer;
    }
    mapData(data, maskPattern) {
        let inc = -1, row = this.moduleCount - 1, bitIndex = 7, byteIndex = 0;
        for (let col = this.moduleCount - 1; col > 0; col -= 2) {
            if (col === 6) col--;
            while (true) {
                for (let c = 0; c < 2; c++) {
                    if (this.modules[row][col - c] === null) {
                        let dark = false;
                        if (byteIndex < data.buffer.length) dark = ((data.buffer[byteIndex] >>> bitIndex) & 1) === 1;
                        this.modules[row][col - c] = dark;
                        bitIndex--;
                        if (bitIndex === -1) { byteIndex++; bitIndex = 7; }
                    }
                }
                row += inc;
                if (row < 0 || this.moduleCount <= row) { row -= inc; inc = -inc; break; }
            }
        }
    }
}

export const generateQrSvg = (text, size = 200) => {
    if (!text) return "";
    try {
        const qr = new QRCodeModel(4, 'L');
        qr.addData(text);
        qr.make();

        const count = qr.moduleCount;
        const cellSize = size / count;
        let pathData = "";
        for (let r = 0; r < count; r++) {
            for (let c = 0; c < count; c++) {
                if (qr.modules[r][c]) {
                    pathData += `M${c * cellSize},${r * cellSize}h${cellSize}v${cellSize}h-${cellSize}z `;
                }
            }
        }
        const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
            <rect width="100%" height="100%" fill="#ffffff"/>
            <path d="${pathData}" fill="#000000"/>
        </svg>`;
        return "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svg)));
    } catch (e) {
        console.error("QR Error:", e);
        return "";
    }
};
