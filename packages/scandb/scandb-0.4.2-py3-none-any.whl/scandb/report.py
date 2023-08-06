import argparse
import sqlite3
from docxtpl import DocxTemplate, RichText
from io import StringIO, BytesIO

from scandb.models import init_db, Vuln, Host

HOST_BY_PID = "SELECT distinct address,port,protocol,service,severity,plugin_id,plugin_name,plugin,info,xref,description,synopsis,solution FROM vuln join host on vuln.host_id = host.id WHERE plugin_id = ? ;"


class Vuln(object):

    def __init__(self, addr="", port = "", protocol = "", service = "", solution = "", severity = "",
                 description = "", synopsis = "", xref = "" , info = "", plugin_id = "", plugin_name = "",  plugin = ""):
        self.addr = addr
        self.port = port
        self.protocol = protocol
        self.service = service
        self.solution = solution
        self.severity = severity
        self.description = description
        self.synopsis = synopsis
        self.xref = xref
        self.info = info
        self.plugin_id = plugin_id
        self.plugin_name = plugin_name
        self.plugin = plugin


def get_hosts_by_plugin(db, query="", plugin=""):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(query, (plugin,))
    rows = cur.fetchall()
    conn.close()
    return rows


def report_cli():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--db", type=str, required=False, default="scandb.sqlite")
    parser.add_argument("--plugin", type=int, default=None, required=False, help="Nessus Plugin-ID")
    parser.add_argument("--docx", metavar="FILE", required=True, type=str,
                        help="The docx template file.")
    parser.add_argument("-o", "--outfile", required=False, default="scandb-finding", help="Prefix for output files.")
    args = parser.parse_args()

    # initialize the database
    database = init_db(args.db)

    doc = DocxTemplate(args.docx)
    context = {'vulns': []}

    if args.plugin is not None:
        result = get_hosts_by_plugin(args.db, HOST_BY_PID, args.plugin)
        vulns = []
        for v in result:
            address, port, protocol, service, severity, plugin_id, plugin_name, plugin, info, xref, description, synopsis, solution = v
            vuln = Vuln(addr=address, port=port, protocol=protocol, service=service, severity=severity, info=info,
                        xref=xref, plugin_id=plugin_id, plugin_name=plugin_name, plugin=plugin, description=description,
                        synopsis=synopsis, solution=solution)
            vulns.append(vuln)
        context['vulns'] = vulns

    doc.render(context)
    f = BytesIO()
    doc.save(f)