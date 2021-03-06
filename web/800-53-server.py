#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, os.path
import sys
import random
import string
import json
import yaml
import cherrypy
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('web/templates'))

sys.path.append(os.path.join('lib'))
sys.path.append(os.path.join('data'))
from seccontrol import SecControl
from seccontrolviz import SecControlViz
from utilities import *


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head>
            <title>800-53 Controls</title>
            <link rel="stylesheet" type="text/css" href="/assets/css/main.css">
          </head>
      <body>

        <form id="form_lookup" method="get" action="control">
          800-53 control id: <input type="text" value="" name="id" />
              <button type="submit">Show me!</button>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <a href="/">families</a>

        </form>

        <div id="container_index">
            <h2>NIST SP 800-53 Control Families</h2>

            <div class="cfh"><div class="cfh_id"><a href="/family?id=AC">AC</a></div> - Access Control</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=AU">AU</a></div> - Audit and Accountability</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=AT">AT</a></div> - Awareness and Training</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=CM">CM</a></div> - Configuration Management</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=CP">CP</a></div> - Contingency Planning</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=IA">IA</a></div> - Identification and Authentication</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=IR">IR</a></div> - Incident Response</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=MA">MA</a></div> - Maintenance</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=MP">MP</a></div> - Media Protection</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=PS">PS</a></div> - Personnel Security</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=PE">PE</a></div> - Physical and Environmental Protection</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=PL">PL</a></div> - Planning</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=PM">PM</a></div> - Program Management</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=RA">RA</a></div> - Risk Assessment</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=CA">CA</a></div> - Security Assessment and Authorization</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=SC">SC</a></div> - System and Communications Protection</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=SI">SI</a></div> - System and Information Integrity</div>
            <div class="cfh"><div class="cfh_id"><a href="/family?id=SA">SA</a></div> - System and Services Acquisition</div>
        </div>

      </body>
    </html>"""

    @cherrypy.expose
    def family(self, id="AC", format="html"):
        id = id.upper()
        family_control_count =  {"AC": 25, "AU": 16, "AT": 5, "CM": 11, "CP": 13, "IA": 11, "IR": 10, "MA": 6, "MP": 8,
            "PS": 8, "PE": 20, "PL": 9, "PM": 16, "RA": 6, "CA": 9, "SC": 44, "SI": 17, "SA": 22}
        families = {"AC": "Access Control", "AU": "Audit and Accountability", "AT": "Awareness and Training", "CM": "Configuration Management",
            "CP": "Contingency Planning", "IA": "Identification and Authentication", "IR": "Incident Response", "MA": "Maintenance",
            "MP": "Media Protection", "PS": "Personnel Security", "PE": "Physical and Environmental Protection", "PL": "Planning",
            "PM": "Program Management", "RA": "Risk Assessment", "CA": "Security Assessment and Authorization",
            "SC": "System and Communications Protection", "SI": "System and Information Integrity", "SA": "System and Services Acquisition"}

        control_list = []
        for control in range(1,family_control_count[id]+1):
            sc = SecControl("%s-%d" % (id, control))
            control_list.append('<div><a href="/control?id=%s-%d">%s-%d</a> - %s</div>' % (id, control, id, control, sc.title.title()))

        return """<html>
          <head>
            <title>800-53 Controls - {sc_id}</title>
            <link rel="stylesheet" type="text/css" href="/assets/css/main.css">
          </head>
      <body>

        <form id="form_lookup" method="get" action="control">
          800-53 control id: <input type="text" value="" name="id" />
              <button type="submit">Show me!</button>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <a href="/">families</a>
        </form>

        <div id="container_index">
            <h2>{sc_id} - {sc_family}</h2>

            <div class="control_list">
                {sc_list}
            </div>
        </div>

      </body>
    </html>""".format(sc_id = id, sc_family = families[id], sc_list = "\n".join(control_list))

    @cherrypy.expose
    def generate(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

    @cherrypy.expose
    def error404(self):
        return """<html>
          <head>
            <title>800-53 Control Error 404</title>
            <link rel="stylesheet" type="text/css" href="/assets/css/main.css">
          </head>
      <body>

        <form id="form_lookup" method="get" action="control">
          800-53 control id: <input type="text" value="" name="id" />
              <button type="submit">Show me!</button>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <a href="/">families</a>
        </form>
        

        <h2>Error - 404</h2>
        These are not the controls you are looking for...
        """

    # http://localhost:8080/control?id=AU-4
    @cherrypy.expose
    def control(self, id="AU-4", format="html"):
        id = id.upper()
        sc = SecControl(id)
        if sc.title is None and sc.description is None and format == "html":
            # control does not exist, return 404
            print "\n*** control does not exist"
            raise cherrypy.HTTPRedirect("/error404")
        cv = SecControlViz(id)

        # create graphviz file
        cv.precursor_list(cv.dep_dict, id, cv.nodes)
        # create edges
        for node in cv.nodes:
            cv.precursor_edges(cv.dep_dict, node, cv.edges)
        digraph = cv.add_nodes(cv.digraph(), cv.node_options_tuples(cv.nodes))
        # print "<%s>" % digraph

        # determine graph image size
        node_count = len(cv.nodes)
        if node_count <= 5: cv.width,cv.height = 2.5,2.5
        if node_count <= 2: cv.width,cv.height = 2.5,2.5
        if node_count >= 6: cv.width,cv.height = 2.75,2.75
        if node_count >= 10: cv.width,cv.height = 3,3
        if node_count >= 20: cv.width,cv.height = 3,3
        if node_count >= 40: cv.width,cv.height = 4,4
        if node_count >= 100: cv.width,cv.height = 12,10
        print "node_count", node_count
        print "w, h", cv.width, cv.height

        # weak test, first delete file if exists
        try:
            os.remove("output/img/%s-precursors" % id)
            os.remove("output/img/%s-precursors.%s" % (id, cv.vizformat))
        except OSError:
            pass
        # generate graphviz file
        graph_label = "%s Control Chain" % (id)
        cv.add_edges(cv.add_nodes(cv.digraph(engine='dot', body={'size ="%d,%d";' % (cv.width, cv.height)}, graph_attr={'label': graph_label, 'labelloc': 'bottom', 'labeljust': 'center', 'fontcolor':'slategray', 'fontname':'Arial', 'fontsize': '14', 'K': '4.6'}), cv.node_options_tuples(cv.nodes)),
            cv.edges
        ).render("output/img/%s-precursors" % id)

        # read contents of svg file into variable
        with open("output/img/%s-precursors.svg" % id, "r") as svg_file:
            svg_content = svg_file.read()

        # render json
        if format == "json":
            cherrypy.response.headers['Content-Type'] = 'application/json'
            if sc.title is None and sc.description is None:
                raise cherrypy.HTTPError("404 Not Found", "The requested resource does not exist")
            return json.dumps(sc.get_control_json())

        with open('compliance/system/project_info.yml', 'r') as f:
            project = yaml.load(f)

        sc_desc = use_org_name(sc.description.encode('utf-8'), project['organization']['name'])
        sc_desc = replace_assignments(sc_desc, project)
        sc_desc = replace_line_breaks(replace_line_breaks(sc_desc, "\n", "<br /><br />"), "\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        # render html page
        tmpl = env.get_template('control.html', project)
        return tmpl.render( sc_id = id, sc_title = sc.title, sc_desc = sc_desc,
            sc_svg = svg_content, sc_graph_height = cv.height*96,
            path=os.path.abspath(os.getcwd()) )

    # http://localhost:8080/controllist/?ids=AU-4,AU-6
    # http://localhost:8080/controllist/?ids=AU-4,AU-6&format=html
    # http://localhost:8080/controllist/?ids=AU-4,AU-6&format=json
    # http://localhost:8080/controllist/?ids=AU-4,AU-6&format=yaml
    # http://localhost:8080/controllist/?ids=AU-4,AU-6&format=control-masonry
    @cherrypy.expose
    def controllist(self, ids="AU-4,AU-6", format="html"):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        controllist = []
        j = dict()
        y = dict()
        # return ids.split(',')
        for id in ids.split(','):
            id = id.upper()
            sc = SecControl(id)
            if sc.title is None and sc.description is None and format == "html":
                # control does not exist, return 404
                print "\n*** control does not exist"
                raise cherrypy.HTTPError("404 Not Found", "The requested resource does not exist")
            controllist.append(sc.get_control_json())
            j[id] = sc.get_control_json()
            y[id] = sc.get_control_yaml()

        # render yaml
        if format == "yaml":
            if sc.title is None and sc.description is None:
                raise cherrypy.HTTPError("404 Not Found", "The requested resource does not exist")
            cherrypy.response.headers['Content-Type'] = 'text/yaml'
            return yaml.safe_dump(y, default_flow_style=False)

        #  render for 18F's control-masonry YAML format with separate subsections
        if format == "control-masonry":
            cherrypy.response.headers['Content-Type'] = 'text/yaml'
            tmpl = env.get_template('control-masonry.yaml')
            return tmpl.render(controllist=controllist)

        # render json
        if format == "json":
            cherrypy.response.headers['Content-Type'] = 'application/json'
            if sc.title is None and sc.description is None:
                raise cherrypy.HTTPError("404 Not Found", "The requested resource does not exist")
            return json.dumps(controllist)
        else:
            # render html
            cherrypy.response.headers['Content-Type'] = 'text/html'
            tmpl = env.get_template('controllist.html')
            return tmpl.render(controllist=controllist)

    # http://localhost:8080/projectinfo
    @cherrypy.expose
    def project(self, format="html"):
        print "executing projectinfo"
        with open('compliance/system/project_info.yml', 'r') as f:
            project = yaml.load(f)

        # render html
        if format == "html":
            cherrypy.response.headers['Content-Type'] = 'text/html'
            # override env
            env = Environment(loader=FileSystemLoader('compliance/system/fisma/templates'))
            tmpl = env.get_template('project.html')
            return tmpl.render(project=project)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.encode.on': True,
            'tools.encode.encoding': 'utf-8'
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        },
        '/output': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'output'
        },
        '/assets': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'web/assets'
        }
    }
    # Comment out next line to not serve on default 127.0.0.1 and not publicly
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080,
            })
    cherrypy.quickstart(StringGenerator(), '/', conf)