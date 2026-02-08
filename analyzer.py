import json
import time
from collections import Counter

def perform_deep_analysis(data, lookback=10):
    # শেষ ১০টি ডাটা প্যাটার্ন হিসেবে নেওয়া
    current_pattern = data[-lookback:]
    last_issue = current_pattern[-1]['issueNumber']
    
    print(f"নতুন ডেটা সনাক্ত হয়েছে! ইস্যু নম্বর: {last_issue}")
    
    matches = []
    
    # ৯০০০০ ডেটার মধ্যে ১০টি সিকোয়েন্সের গভীর অনুসন্ধান
    # এখানে Number, Color এবং Premium সবগুলোকে সমান গুরুত্ব দেওয়া হয়েছে
    for i in range(len(data) - lookback - 1):
        match_found = True
        for j in range(lookback):
            if (data[i+j]['number'] != current_pattern[j]['number'] or 
                data[i+j]['color'] != current_pattern[j]['color'] or
                data[i+j]['premium'] != current_pattern[j]['premium']):
                match_found = False
                break
        
        if match_found:
            # ১০টি মিলে গেলে ১১ নম্বর ডেটাটি কী ছিল তা সংগ্রহ করা
            matches.append(data[i + lookback])

    # ফলাফল তৈরি
    result = {
        "sync_issue": last_issue,
        "prediction": "N/A",
        "color": "N/A",
        "confidence": "0%",
        "history_matches": len(matches)
    }

    if matches:
        # নাম্বার এবং কালার ফ্রিকোয়েন্সি ক্যালকুলেশন
        pred_num = Counter([m['number'] for m in matches]).most_common(1)[0]
        pred_col = Counter([m['color'] for m in matches]).most_common(1)[0]
        
        result.update({
            "prediction": pred_num[0],
            "color": pred_col[0],
            "confidence": f"{(pred_num[1]/len(matches))*100:.2f}%"
        })

    # এইচটিএমএল এই ফাইলটি রিড করবে
    with open('live_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

def monitor_file():
    last_processed_issue = None
    
    while True:
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                all_data = json.load(f)
            
            if not all_data:
                continue

            current_issue = all_data[-1]['issueNumber']

            # যদি নতুন ইস্যু আসে, তবেই এনালাইসিস শুরু হবে
            if current_issue != last_processed_issue:
                perform_deep_analysis(all_data)
                last_processed_issue = current_issue
                
        except Exception as e:
            print(f"Error: {e}")
        
        # ফাইলটি প্রতি ২ সেকেন্ড পরপর চেক করবে নতুন ডেটা এলো কি না
        time.sleep(2)

if __name__ == "__main__":
    monitor_file()
    
