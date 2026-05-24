import qrcode from 'qrcode-generator';

export const generateQrSvg = (text, size = 200) => {
    if (!text) return "";
    try {
        // qrcode(0, 'L') automatically chooses the best typeNumber (0 is auto)
        const qr = qrcode(0, 'L');
        qr.addData(text);
        qr.make();
        
        // Calculate appropriate cell size based on target size and module count
        const count = qr.getModuleCount();
        const cellSize = Math.max(1, Math.round(size / count));
        
        // Return data URL directly
        return qr.createDataURL(cellSize, 0);
    } catch (e) {
        console.error("QR Error:", e);
        return "";
    }
};
