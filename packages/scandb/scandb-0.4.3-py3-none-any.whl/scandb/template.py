import argparse
import sqlite3

HOST_BY_PID = "SELECT distinct address,port,protocol,service,severity,plugin_id,plugin_name,plugin,info,xref,description,synopsis,solution FROM vuln join host on vuln.host_id = host.id WHERE plugin_id = ? ;"


def get_hosts_by_plugin(db, query="", plugin=""):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(query, (plugin,))
    rows = cur.fetchall()
    conn.close()
    return rows


def vulns_cli():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--db", type=str, required=False, default="scandb.sqlite")
    parser.add_argument("--plugin", type=int, required=True, help="Nessus Plugin-ID")
    parser.add_argument("--docx", metavar="FILE", required=True, type=str,
                        help="The docx template file.")
    parser.add_argument("-o", "--outfile", required=False, default="scandb-finding", help="Prefix for output files.")
    args = parser.parse_args()

    result = get_hosts_by_plugin(args.db, HOST_BY_PID, args.plugin)

    for r in result:
        print (r)
