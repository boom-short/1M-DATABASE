import json
from collections import Counter

def complex_analysis(file_path, output_file='result.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return

    # ১০টি ডেটার প্যাটার্ন চেক করার জন্য সেটআপ
    lookback = 10 
    if len(data) < lookback + 1:
        return

    # বর্তমানের শেষ ১০টি মার্কেটের অবস্থা
    current_trend = data[-lookback:]
    
    matches = []

    # গভীর স্ক্যানিং (Number, Color, Premium/Issue গুরুত্ব সহকারে)
    for i in range(len(data) - lookback - 1):
        is_match = True
        for j in range(lookback):
            # প্রতিটি পয়েন্ট চেক করা হচ্ছে
            if (data[i+j]['number'] != current_trend[j]['number'] or 
                data[i+j]['color'] != current_trend[j]['color']):
                is_match = False
                break
        
        if is_match:
            # ১০টি প্যাটার্ন মিলে গেলে ১১ নম্বরটি কী ছিল তা সংগ্রহ করা
            matches.append(data[i + lookback])

    # ফলাফল প্রস্তুত করা
    if matches:
        pred_numbers = [m['number'] for m in matches]
        pred_colors = [m['color'] for m in matches]
        
        best_num = Counter(pred_numbers).most_common(1)[0]
        best_col = Counter(pred_colors).most_common(1)[0]
        
        result = {
            "prediction": {
                "number": best_num[0],
                "color": best_col[0],
                "confidence": f"{(best_num[1]/len(matches))*100:.2f}%",
                "history_found": len(matches),
                "status": "Success"
            }
        }
    else:
        result = {"prediction": {"status": "New Pattern", "msg": "ইতিহাসে এই ১০টি সিকোয়েন্সের মিল নেই।"}}

    # এইচটিএমএল এর ব্যবহারের জন্য রেজাল্ট সেভ করা
    with open(output_file, 'w') as f:
        json.dump(result, f)
    print("এনালাইসিস সম্পন্ন এবং এইচটিএমএল-কে নির্দেশ পাঠানো হয়েছে।")

if __name__ == "__main__":
    complex_analysis('data.json')
  
