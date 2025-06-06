#!/usr/bin/env python3

import sys
import requests
import subprocess
import shutil
import time

def fetch_crtsh(domain):
    print("[*] Buscando en crt.sh...")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        res = requests.get(url, timeout=15)
        results = res.json()
        return {entry['name_value'].strip() for entry in results if domain in entry['name_value']}
    except Exception as e:
        print(f"[!] Error en crt.sh: {e}")
        return set()

def fetch_certspotter(domain):
    print("[*] Buscando en certspotter (sslmate)...")
    try:
        url = f"https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names"
        headers = {'User-Agent': 'OSINT-Tool'}
        res = requests.get(url, headers=headers, timeout=15)
        data = res.json()
        subdomains = set()
        for cert in data:
            for name in cert.get("dns_names", []):
                if domain in name:
                    subdomains.add(name)
        return subdomains
    except Exception as e:
        print(f"[!] Error en certspotter: {e}")
        return set()

def fetch_rapiddns(domain):
    print("[*] Buscando en rapiddns.io...")
    try:
        res = requests.get(f"https://rapiddns.io/subdomain/{domain}?full=1", timeout=15)
        return set(line.strip() for line in res.text.splitlines() if domain in line)
    except Exception as e:
        print(f"[!] Error en rapiddns.io: {e}")
        return set()

def run_subfinder(domain):
    if shutil.which("subfinder") is None:
        return set()
    print("[*] Ejecutando subfinder...")
    try:
        output = subprocess.check_output(["subfinder", "-d", domain, "-silent"], text=True)
        return set(output.strip().splitlines())
    except Exception as e:
        print(f"[!] Error en subfinder: {e}")
        return set()

def run_amass(domain):
    if shutil.which("amass") is None:
        return set()
    print("[*] Ejecutando amass (modo pasivo, máximo 5 minutos)...")

    cmd = ["amass", "enum", "-passive", "-d", domain]
    output_lines = []
    try:
        with open("amass_output.txt", "w") as logfile:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            start_time = time.time()

            while True:
                if proc.poll() is not None:
                    break
                if time.time() - start_time > 300:
                    print("[!] Tiempo máximo alcanzado. Finalizando amass...")
                    proc.terminate()
                    break
                line = proc.stdout.readline()
                if line:
                    line = line.strip()
                    output_lines.append(line)
                    logfile.write(line + "\n")

            # Captura lo restante si amass finalizó por su cuenta
            if proc.stdout:
                for line in proc.stdout.read().splitlines():
                    line = line.strip()
                    output_lines.append(line)
                    logfile.write(line + "\n")

        print("[+] Resultados de amass guardados en: amass_output.txt")
        return set(output_lines)
    except Exception as e:
        print(f"[!] Error ejecutando amass: {e}")
        return set()

def check_http_services(subdomains):
    print("\n[*] Verificando si los subdominios responden por HTTP/HTTPS...")
    live = set()
    for sub in sorted(subdomains):
        for proto in ["http", "https"]:
            url = f"{proto}://{sub}"
            try:
                r = requests.get(url, timeout=5)
                if r.status_code < 500:
                    print(f"  [+] {url} -> {r.status_code}")
                    live.add(url)
                    break
            except:
                continue
    return live

def save_to_file(domain, subdomains, live_subs):
    filename = f"subdomains_{domain.replace('.', '_')}.txt"
    with open(filename, "w") as f:
        f.write("# Subdominios encontrados:\n")
        for sub in sorted(subdomains):
            f.write(sub + "\n")
        f.write("\n# Subdominios activos:\n")
        for live in sorted(live_subs):
            f.write(live + "\n")
    print(f"\n[+] Resultados guardados en: {filename}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 subdomain_enum_extended.py ejemplo.com")
        sys.exit(1)

    domain = sys.argv[1]
    all_subdomains = set()

    all_subdomains |= fetch_crtsh(domain)
    all_subdomains |= fetch_certspotter(domain)
    all_subdomains |= fetch_rapiddns(domain)
    all_subdomains |= run_subfinder(domain)
    all_subdomains |= run_amass(domain)

    all_subdomains = {s.strip().lower() for s in all_subdomains if domain in s}

    print(f"\n[+] Total de subdominios encontrados: {len(all_subdomains)}")

    live_subs = check_http_services(all_subdomains)

    save_to_file(domain, all_subdomains, live_subs)

if __name__ == "__main__":
    main()
