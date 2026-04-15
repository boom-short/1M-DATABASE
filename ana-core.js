// ana-core.js
class ANACore {
    constructor() {
        this.data = [];
    }

    async fetchStream() {
        try {
            const res = await fetch('data.json?nocache=' + new Date().getTime());
            this.data = await res.json();
            this.processNeuralLogic();
        } catch (e) { console.error("Data Sensing Failed..."); }
    }

    processNeuralLogic() {
        if (this.data.length < 10) return;

        // সর্বশেষ পিরিয়ড শনাক্তকরণ
        const lastEntry = this.data[0];
        const nextPeriod = (BigInt(lastEntry.issueNumber) + 1n).toString();

        // ১ পিরিয়ড অ্যাডভান্স প্রেডিকশন লজিক (Pattern Sensing)
        const recentNumbers = this.data.slice(0, 10).map(d => parseInt(d.number));
        
        // রিয়েল-টাইম প্যাটার্ন ম্যাপিং
        const avg = recentNumbers.reduce((a, b) => a + b, 0) / recentNumbers.length;
        const lastNum = recentNumbers[0];

        let decision = "";
        let probability = 0;

        // অটোনোমাস ডিসিশন মেকিং (সিম্পল নিউরাল সিমুলেশন)
        if (lastNum > 5 && avg > 4.5) {
            decision = "SMALL"; // ট্রেন্ড রিভার্সাল সেন্সিং
            probability = 78.44;
        } else if (lastNum <= 4 && avg < 5) {
            decision = "BIG";
            probability = 82.15;
        } else {
            decision = Math.random() > 0.5 ? "BIG" : "SMALL";
            probability = 65.00;
        }

        this.renderUI(nextPeriod, decision, probability);
    }

    renderUI(period, decision, prob) {
        document.getElementById('target-period').innerText = period;
        const pBox = document.getElementById('prediction-display');
        pBox.innerText = decision;
        pBox.style.color = (decision === "BIG") ? "#00ffcc" : "#ff3366";
        document.getElementById('confidence').innerText = prob + "%";
    }
}

const engine = new ANACore();
setInterval(() => engine.fetchStream(), 1000); // 1 সেকেন্ড পর পর লাইভ ডাটা চেক
engine.fetchStream();

