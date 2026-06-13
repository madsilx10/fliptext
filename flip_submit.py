import os
import time
import random
import requests

# ===================== CONFIG =====================
REFERRAL_CODE = "TEN223"
API_URL = f"https://fliptexts.com/api/invites/{REFERRAL_CODE}/claim"
EMAILS_FILE = "emails.txt"

FIRST_NAMES = [
    "James", "Michael", "Robert", "John", "David", "William", "Richard",
    "Joseph", "Thomas", "Daniel", "Mark", "Paul", "Steven", "Andrew",
    "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy",
    "Jennifer", "Linda", "Patricia", "Elizabeth", "Susan", "Jessica",
    "Sarah", "Karen", "Nancy", "Lisa", "Margaret", "Betty", "Sandra",
    "Ashley", "Emily", "Donna", "Michelle", "Laura", "Amy", "Rachel"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
]

USE_CASE_OPTIONS = [
    [],
    ["yield-farming"],
    ["credit-card-bonuses"],
    ["yield-farming", "credit-card-bonuses"],
]
# ==================================================


def load_emails():
    emails = []
    with open(EMAILS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                emails.append(line)
    return emails


def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def submit(email):
    full_name = random_name()
    use_cases = random.choice(USE_CASE_OPTIONS)

    payload = {
        "fullName": full_name,
        "email": email,
        "instagram": "",
        "company": "Personal",
        "useCases": use_cases,
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://fliptexts.com",
        "Referer": f"https://fliptexts.com/i/{REFERRAL_CODE}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36",
    }

    print(f"\n  [→] {email}")
    print(f"      Nama: {full_name} | UseCases: {use_cases}")

    try:
        r = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        if r.status_code == 200:
            print(f"  [✓] SUKSES")
        else:
            print(f"  [✗] GAGAL - Status: {r.status_code}")
            print(f"      {r.text[:200]}")
    except Exception as e:
        print(f"  [✗] ERROR: {e}")


def print_menu(total):
    print("\n┌─────────────────────────────────────┐")
    print("│       FLIP WAITLIST AUTO SUBMIT      │")
    print("├─────────────────────────────────────┤")
    print(f"│  Total email: {total:<23}│")
    print("├─────────────────────────────────────┤")
    print("│  1  → Run 1 email                    │")
    print("│  2  → Run semua email                │")
    print("│  3  → Run dari email X sampai akhir  │")
    print("│  q  → Keluar                         │")
    print("└─────────────────────────────────────┘")


def main():
    emails = load_emails()
    if not emails:
        print("[!] emails.txt kosong.")
        return

    print_menu(len(emails))
    choice = input("\nPilihan: ").strip().lower()

    if choice == "q":
        return

    elif choice == "1":
        print("\n  Daftar email:")
        for i, e in enumerate(emails):
            print(f"  {i+1}. {e}")
        idx = input("\n  Pilih nomor: ").strip()
        if idx.isdigit() and 1 <= int(idx) <= len(emails):
            submit(emails[int(idx)-1])
        else:
            print("[!] Nomor tidak valid.")

    elif choice == "2":
        print(f"\n[→] Menjalankan semua {len(emails)} email...\n")
        for e in emails:
            submit(e)
            time.sleep(1)
        print("\n[✓] Selesai semua.")

    elif choice == "3":
        print("\n  Daftar email:")
        for i, e in enumerate(emails):
            print(f"  {i+1}. {e}")
        start = input("\n  Mulai dari nomor: ").strip()
        if start.isdigit() and 1 <= int(start) <= len(emails):
            targets = emails[int(start)-1:]
            print(f"\n[→] Menjalankan email {start} sampai {len(emails)}...\n")
            for e in targets:
                submit(e)
                time.sleep(1)
            print("\n[✓] Selesai.")
        else:
            print("[!] Nomor tidak valid.")

    else:
        print("[!] Pilihan tidak dikenali.")


if __name__ == "__main__":
    main()
