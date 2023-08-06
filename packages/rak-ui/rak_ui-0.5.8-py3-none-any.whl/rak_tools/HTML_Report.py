__author__ = "INTEL_DCPAE"
__version__ = "0.1"
import datetime
from xml.sax import saxutils
import sys

# ----------------------------------------------------------------------
# Template

class Template_HTML_Report(object):
    """
    Define a HTML template for report customerization and generation.

    Overall structure of an HTML report

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    DEFAULT_TITLE = 'RAK Report'
    DEFAULT_DESCRIPTION = ''
    DEFAULT_TESTER='dcpae'

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    %(stylesheet)s
</head>
<body >
%(heading)s
%(report)s
%(ending)s

</body>
</html>
"""
    # variables: (title, generator, stylesheet, heading, report, ending)


    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 80%; }
table       { font-size: 100%; }

/* -- heading ---------------------------------------------------------------------- */
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}

.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}

/* -- report ------------------------------------------------------------------------ */
#total_row  { font-weight: bold; }
.passCase   { color: #5cb85c; }
.failCase   { color: #d9534f; font-weight: bold; }
.errorCase  { color: #f0ad4e; font-weight: bold; }
.hiddenRow  { display: none; }
</style>
"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """<div class='heading'>
<h1>%(title)s</h1>
%(parameters)s
<p class='description' style="font-size: 14px;">%(description)s</p>
</div>

""" # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute' style="font-size: 14px;"><strong>%(name)s : </strong> %(value)s</p>
""" # variables: (name, value)


    # ------------------------------------------------------------------------
    # Report
    #
    REPORT_TMPL = """
<p id='show_detail_line'>
<a class="btn btn-primary" >Summary{ %(passrate)s }</a>
<button onclick="btnFailed_Click()" class="btn btn-danger" >Failed{ %(fail)s }</button>
<button onclick="btnPassed_Click()" class="btn btn-success" >Passed{ %(Pass)s }</button>
<button onclick="btnAll_Click()" class="btn btn-info" >ALL{ %(count)s }</button>
</p>
<table id='result_table' class="table table-condensed table-bordered table-hover">
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
    <td width= "150">Automation Level</td>
    <td width= "200">Date</td>
    <td width= "150">Running Time</td>
    <td width= "200">Case_name</td>
    <td width= "100">Result</td>
    <td>Details</td>
    <td>Log</td>
</tr>
%(test_list)s
</table>
""" # variables: (test_list, count, Pass, fail, error ,passrate)

    # ------------------------------------------------------------------------
    # failed cases with log output
    REPORT_FAILED_CASE_TMPL = r"""
<tr class="text-center" style="font-size: 14px;">
    <td width= "150"><div>%(automation_level)s</div></td>
    <td width= "200"><div>%(date)s</div></td>
    <td width= "150"><div>%(runtime)s</div></td>
    <td width= "200"><div>%(case_name)s</div></td>
    <td class='%(style)s' width= "100"><div>%(result)s</div></td>
    <td class='%(style)s'><div>%(details)s</div></td>
    <td colspan='5' align='center'>
        %(serial_log_output)s 
        %(bmc_log_output)s 
        %(os_log_output)s 
        %(cscripts_log_output)s
        %(sel_log_output)s
    </td>
</tr>

<script type="text/javascript">
    function btnFailed_Click(){
        var tableId = document.getElementById('result_table');
        var rowsLength = tableId.rows.length;
        for(var i=1;i<rowsLength;i++){
            var searchText = tableId.rows[i].cells[4].innerText;//取得table行，列的值
            console.log(searchText)
            if(searchText == "failed"){//用match函数进行筛选，如果input的值，即变量 key的值为空，返回的是ture，
                tableId.rows[i].style.display='';//显示行操作，
            }else{
                tableId.rows[i].style.display='none';//隐藏行操作
            }
        }
    }
    
    function btnPassed_Click(){
        var tableId = document.getElementById('result_table');
        var rowsLength = tableId.rows.length;
        for(var i=1;i<rowsLength;i++){
            var searchText = tableId.rows[i].cells[4].innerText;//取得table行，列的值
            console.log(searchText)
            if(searchText == "pass"){//用match函数进行筛选，如果input的值，即变量 key的值为空，返回的是ture，
                tableId.rows[i].style.display='';//显示行操作，
            }else{
                tableId.rows[i].style.display='none';//隐藏行操作
            }
        }
    }
    
    function btnAll_Click(){
        var tableId = document.getElementById('result_table');
        var rowsLength = tableId.rows.length;
        for(var i=1;i<rowsLength;i++){
            tableId.rows[i].style.display='';//显示行操作，
        }
    }
</script>
""" # variables: (style, date, case_name, result, details, log_url)

    # ------------------------------------------------------------------------
    #passed cases
    REPORT_PASSED_CASE_TMPL = r"""
<tr class="text-center" style="font-size: 14px;">
    <td width= "150"><div>%(automation_level)s</div></td>
    <td width= "200"><div>%(date)s</div></td>
    <td width= "150"><div>%(runtime)s</div></td>
    <td width= "200"><div>%(case_name)s</div></td>
    <td class='%(style)s' width= "100"><div>%(result)s</div></td>
    <td class='%(style)s'><div>%(details)s</div></td>
    <td colspan='5' align='center'>
        %(serial_log_output)s 
        %(bmc_log_output)s 
        %(os_log_output)s 
        %(cscripts_log_output)s
        %(sel_log_output)s
    </td>
</tr>
""" # variables: ( style, date, case_name, result, details, serial_log_output, bmc_log_output)

    REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
""" # variables: (id, output)

    # ------------------------------------------------------------------------
    # ENDING
    #
    ENDING_TMPL = """<div id='ending'>&nbsp;</div>
    <div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
    <a href="#"><span class="glyphicon glyphicon-eject" style = "font-size:30px;" aria-hidden="true">
    </span></a></div>
    """

# -------------------- The end of the Template class -------------------

# class CaseResult:
#     def __init__(self, time, case, res, errorMsg, serialLog, bmcLog, osLog, cscriptLog):
#         self.time = time
#         self.case = case
#         self.res = res
#         self.errorMsg = errorMsg
#         self.serialLog = serialLog
#         self.bmcLog = bmcLog
#         self.osLog = osLog
#         self.cscriptLog = cscriptLog

#refactor the format of result（if necessary）
class Result():
    def __init__(self, result):
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.cases = []
        self.passrate = 0
        try:
            for case in result:
                self.cases.append(case)
                if "pass" in case:
                    self.success_count += 1
                elif "failed" in case:
                    self.failure_count += 1
                else:
                    self.error_count += 1
            self.passrate = str("%.2f%%" % (float(self.success_count) / float(
                    self.success_count + self.failure_count + self.error_count) * 100))
        except Exception as e:
            pass

class HTMLReport_Generator(Template_HTML_Report):
    """
    """
    def __init__(self, stream=sys.stdout, title=None, description=None, tester=None):
        self.stream = stream
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description
        if tester is None:
            self.tester = self.DEFAULT_TESTER
        else:
            self.tester = tester

        self.startTime = datetime.datetime.now()


    def report(self, result):
        self.generateReport(result)
        print('\nGenerate HTML Report Success' , file=sys.stderr)
        return

    def getReportAttributes(self, result):
        """
        Override this to add custom attributes.
        """
        status = []
        status.append('ALL %s' % (result.success_count + result.failure_count + result.error_count))
        if result.success_count: status.append('Pass %s' % result.success_count)
        if result.failure_count: status.append('Failure %s' % result.failure_count)
        if result.error_count:   status.append('Error %s' % result.error_count)
        if status:
            status = ' '.join(status)
            self.passrate = str("%.2f%%" % (float(result.success_count) / float(
                result.success_count + result.failure_count + result.error_count) * 100))
        else:
            status = 'none'
        return [
            ('Tester', self.tester),
            ('Result', status + ", Passing rate: " + result.passrate),
        ]

    def generateReport(self, result):
        report_attrs = self.getReportAttributes(result)
        generator = 'RAK_HTML_Report %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(
            title=saxutils.escape(self.title),
            generator=generator,
            stylesheet=stylesheet,
            heading=heading,
            report=report,
            ending=ending,
        )
        self.stream.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=saxutils.escape(name),
                value=saxutils.escape(value),
            )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title=saxutils.escape(self.title),
            parameters=''.join(a_lines),
            description=saxutils.escape(self.description),
            tester=saxutils.escape(self.tester),
        )
        return heading

    def _generate_report(self, result):
        rows = []
        for case in result.cases:
            if "pass" in case:
                tmpl = self.REPORT_PASSED_CASE_TMPL
            else:
                tmpl = self.REPORT_FAILED_CASE_TMPL

            serial_log_output = ""
            bmc_log_output= ""
            os_log_output = ""
            cscripts_log_output = ""
            sel_log_output = ""
            if case[6] == "None":
                serial_log_output = " serial_log "
            else:
                serial_log_output = "<a href="+case[6]+">serial_log&nbsp&nbsp</a>"        #add serial log link
            if case[7] == "None":
                bmc_log_output = " bmc_log "
            else:
                bmc_log_output = "<a href="+case[7]+">bmc_log&nbsp&nbsp</a>"                        #add bmc log link
            if case[8] == "None":
                os_log_output = " os_log "
            else:
                os_log_output = "<a href="+case[8]+">os_log&nbsp&nbsp</a>"
            if case[9] == "None":
                cscripts_log_output = " cscripts_log "
            else:
                cscripts_log_output = "<a href="+case[9]+">cscripts_log</a>"
            if case[10] == "None":
                sel_log_output = " sel_log "
            else:
                sel_log_output = "<a href="+case[10]+">sel_log</a>"

            row = tmpl % dict(
                style = "passCase" if "pass" in case else "failCase",
                automation_level = case[0],
                date = case[1],
                runtime = case[2],
                case_name = case[3],
                result = case[4],
                details = case[5],
                serial_log_output = serial_log_output,
                bmc_log_output = bmc_log_output,
                os_log_output = os_log_output,
                cscripts_log_output = cscripts_log_output,
                sel_log_output = sel_log_output,
            )
            rows.append(row)

        report = self.REPORT_TMPL % dict(
            test_list=''.join(rows),
            count=str(result.success_count + result.failure_count + result.error_count),
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
            passrate=self.passrate,
        )
        return report

    def _generate_ending(self):
        return self.ENDING_TMPL