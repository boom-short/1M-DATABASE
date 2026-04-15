// ana-engine.js
class ANAEngine {
    constructor() {
        this.history = [];
    }

    // JSON থেকে ডাটা রিড করা
    async syncData() {
        try {
            const response = await fetch('data.json');
            this.history = await response.json();
            this.analyzePatterns();
        } catch (err) {
            console.error("Sync Error:", err);
        }
    }

    // অদৃশ্য ধারাবাহিকতা (Neural Mapping) শনাক্তকরণ
    analyzePatterns() {
        if (this.history.length < 5) return;

        // শেষ ১০টি রেকর্ড থেকে প্যাটার্ন বের করা
        const recent = this.history.slice(0, 10);
        const numbers = recent.map(d => parseInt(d.number));
        
        // উদাহরণ লজিক: গড় বা ট্রেন্ড বিশ্লেষণ
        const sum = numbers.reduce((a, b) => a + b, 0);
        const avg = sum / numbers.length;

        this.updateUI(avg > 4.5 ? "BIG" : "SMALL", avg);
    }

    updateUI(prediction, confidence) {
        document.getElementById('predict-box').innerText = prediction;
        document.getElementById('accuracy').innerText = `${(confidence * 10).toFixed(2)}%`;
        
        // লাস্ট ডাটা রেন্ডার করা
        const list = document.getElementById('history-list');
        list.innerHTML = this.history.slice(0, 5).map(item => `
            <div class="data-row">
                <span>#${item.issueNumber.slice(-3)}</span>
                <span class="val">${item.number}</span>
                <span class="col" style="color:${item.color.includes(',') ? 'violet' : item.color}">${item.color}</span>
            </div>
        `).join('');
    }
}

const engine = new ANAEngine();
setInterval(() => engine.syncData(), 3000); // প্রতি ৩ সেকেন্ডে অটো আপডেট
engine.syncData();
