import os
import platform
from datetime import datetime

sites_para_bloquear = [
    "facebook.com",
    "www.facebook.com",
    "instagram.com",
    "www.instagram.com",
    "tiktok.com",
    "www.tiktok.com"
]

redirect = "0.0.0.0"


def obter_hosts_path():
    sistema = platform.system()

    if sistema == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    elif sistema in ["Linux", "Darwin"]:
        return "/etc/hosts"
    else:
        raise Exception("Sistema operacional não suportado")


def backup_hosts(hosts_path):
    backup = f"{hosts_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.system(f'copy "{hosts_path}" "{backup}"' if platform.system() == "Windows"
              else f'cp "{hosts_path}" "{backup}"')

    print(f"[+] Backup criado: {backup}")


def bloquear():
    hosts_path = obter_hosts_path()

    try:
        backup_hosts(hosts_path)

        with open(hosts_path, "r+") as file:
            linhas = file.readlines()
            file.seek(0, os.SEEK_END)

            existentes = set()

            for linha in linhas:
                if linha.strip() and not linha.startswith("#"):
                    partes = linha.split()
                    if len(partes) > 1:
                        existentes.add(partes[1])

            for site in sites_para_bloquear:
                if site not in existentes:
                    file.write(f"{redirect} {site}\n")
                    print(f"[+] Bloqueado: {site}")
                else:
                    print(f"[-] Já existe: {site}")

    except PermissionError:
        print("Execute como ADMIN/root!")


if __name__ == "__main__":
    bloquear()