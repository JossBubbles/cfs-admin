import sys
import uvicorn
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(
        prog = "cfs-admin-cli", description = "Herramienta de despliegue de servicio de monitoreo para cfs-cs."
    )

    subparser = parser.add_subparsers(dest = "accion", required = True)

    parser_run = subparser.add_parser("run")
    parser_run.add_argument("target", choices = ["app", "aplicacion", "db", "database"])

    parser_create = subparser.add_parser("create")
    parser_create.add_argument("target", choices = ["db", "database"])

    args = parser.parse_args()



    if (args.target in ("db", "database")):
        if (args.accion == "run"):
            subprocess.run(["docker", "compose", "down", "-v"])
            subprocess.run(["docker", "compose", "up", "-d"])

        elif (args.subparser == "create"):
            from db.create_db import create_database
            create_database()

        sys.exit(0)


    elif  (args.target in ("app", "aplicacion")):
        if (args.accion == "run"):
            uvicorn.run("config.app:Aplicacion", host = "127.0.0.1", port = 8000, reload = True)

        sys.exit(0)



if __name__ == "__main__":
    main()