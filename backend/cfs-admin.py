import sys
import uvicorn
import argparse
import subprocess

from config.load import CONFIG

def main():
    parser = argparse.ArgumentParser(
        prog = "cfs-admin-cli",
        description = "Herramienta de despliegue de servicio de monitoreo para cfs-cs"
    )

    subparser = parser.add_subparsers(dest = "accion", required = True)

    parser_run = subparser.add_parser("run")
    parser_run.add_argument("target", choices = ["app", "db"])

    parser_create = subparser.add_parser("create")
    parser_create.add_argument("service", choices = ["db"])

    args = parser.parse_args()


    if (args.accion == "run"):
        if (args.target == "db"): 
            subprocess.run(["docker", "compose", "down", "-v"])
            subprocess.run(["docker", "compose", "up", "-d"])

        else:
            uvicorn.run("core.app:application", host = "localhost", port = CONFIG.PORT_APP)

        sys.exit(0)

    elif (args.accion == "create"):
        if (args.service == "db"):
            from db.controller import create_tables
            create_tables()

        sys.exit(0)


if __name__ == "__main__":
    main()