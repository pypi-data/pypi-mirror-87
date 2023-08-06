"""
This module provides verification of user's email and password.


"""

import miupload.runningConfiguration as cfg
import requests
import time
import miupload.skins as skins
import urllib.parse

name = "miupload"
log = ""

# Check if module is configu red and ready.
try:
    if (cfg.configured):
        ready = True
    else:
        ready = False
except:
    ready = False

try:
    if (cfg.base_url):
        base_url = cfg.base_url
    else:
        base_url = "http://sss-data.minerva.community"
except:
    base_url = "http://sss-data.minerva.community"


def get_status():
    """
    For DEBUG. Returns login status and server base_url.
    :return:
    """
    global ready
    global base_url
    print(ready, base_url)
    return ready


def login(token):
    """
    Function checks access token and then saves configuration data for later use.

    :param token:
    :return:
    """
    global ready
    global base_url
    if (ready):
        Q = input("Module is already configured. Rewrite? (y/n): ")
        if (Q == "y"):
            pass
        else:
            "Answer is not y. Configuration aborted."
            return None

    print("Contacting data server...")

    r = requests.post(base_url + "/User/validate_v2", data={'psw': token})
    res = str(r.content, 'utf-8', 'ignore')
    if (res == "FALSE"):
        print("Verification failed! Please check your Minerva email and password. Try again!")
        return False
    elif (res.split(";")[0] == 'TRUE'):  # TODO
        print("Verification successful! Saving Configuration " + res.split(";")[1] + "...")
        cfg.email = res.split(";")[1]
        cfg.psw = token
        cfg.configured = True
        ready = True
    else:
        print("Verification failed! Please check your Minerva email and password. Try again!")
        return False

    print("MiUpload configuration saved successfully!")


def login_gui():
    """
    Ask user to login with prompt for email and password.

    :return:
    """
    return login(input("Enter your unique access token: "))


def set_server(new_url):
    """
    For DEBUG only. Allows to change server address and redirect communication to alternative server.

    :param url:
    :return:
    """
    global base_url

    cfg.base_url = new_url
    base_url = new_url
    return True


def submit_notebook(assignment=None, guest=False, websubmit=False):
    """

    :param assignment:
    :return:
    """
    global ready
    global base_url
    global log

    if (not ready) and not guest:
        print("You are not logged in!")
        print("Please run miupload.login_gui()")
        return False
    else:
        if guest:
            author = guest
        else:
            author = cfg.email

    try:
        from IPython.display import display, Javascript, HTML, IFrame
        display(Javascript("IPython.notebook.save_notebook()"),
                include=['application/javascript'])
        display(HTML(skins.HTML_PROGRESS_BAR))
    except ImportError:
        print("Autosaving failed. Please make sure to save your notebook before submitting notebook.")
    else:
        print("Autosaving notebook...")  # save notebook before reading of file

    def progress_bar_step(name, step=10):
        try:
            display(Javascript("""
                var current_progress = parseInt($("#submitprogress").attr("aria-valuenow"));
                  current_progress += """ + str(step) + """;  
                  $("#""" + name + """")
                  .css("width", current_progress + "%")
                  .attr("aria-valuenow", current_progress)
                  .text(current_progress + "% Complete");
                  """))
            return True
        except:
            return False

    progress_bar_step("submitprogress", step=5)

    display(Javascript("IPython.notebook.save_notebook()"),
            include=['application/javascript'])
    display(Javascript(skins.JS_PROGRESS_BAR_INIT))
    time.sleep(5)

    print("Notebook saved.")
    print("Preparing .ipynb upload")
    # Get filename of notebook for uploading
    # Source: https://github.com/jupyter/notebook/issues/1000
    import json
    import os.path
    import re
    import ipykernel
    import requests

    # Alternative that works for both Python 2 and 3:
    from requests.compat import urljoin

    try:  # Python 3 (see Edit2 below for why this may not work in Python 2)
        from notebook.notebookapp import list_running_servers
    except ImportError:  # Python 2
        import warnings
        from IPython.utils.shimmodule import ShimWarning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=ShimWarning)
            from IPython.html.notebookapp import list_running_servers

    def get_notebook_name():
        global log
        """
        Return the full path of the jupyter notebook.
        """
        kernel_id = re.search('kernel-(.*).json',
                              ipykernel.connect.get_connection_file()).group(1)
        servers = list_running_servers()
        log += "[DEBUG] Getting Server List\n"
        log += "[DEBUG] Servers:" + repr(servers) + "\n"
        for ss in servers:
            log += "[DEBUG] URL:" + urljoin(ss['url'], 'api/sessions') + "\n"
            log += "[DEBUG] Params:" + str(repr(ss.get('token', ''))) + "\n"
            response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                    params={'token': ss.get('token', '')})
            log += "[DEBUG] Response:" + response.text + "\n"
            for nn in json.loads(response.text):
                try:
                    log += "[DEBUG] Kernel:" + str(repr(nn)) + "\n"
                    if nn['kernel']['id'] == kernel_id:
                        relative_path = nn['notebook']['path']
                        return os.path.join(ss['notebook_dir'], relative_path)
                except:
                    log += "[DEBUG] Failed to get kernel:" + repr(nn) + "\n"

                    # display(HTML(skins.HTML_KERNEL_API_CALL_FAILED))
                    # relative_path = input("path/filename.ipynb: ")
                    return False;

    if websubmit:
        filename = False;
    else:
        filename = get_notebook_name()

    if (filename == False):
        if guest:
            create = 1
        else:
            create = 0
        src = base_url + "/GUI/manual_upload/" + assignment + "/" + urllib.parse.quote(author) + "?guest=" + create
        if not websubmit:
            display(HTML(skins.HTML_MESSAGE_INPUT_REQUIRED))
        display(IFrame(src, 600, 100))
    else:
        display(Javascript(skins.JS_PROGRESS_BAR_FAST_STEP))
        display(Javascript(skins.JS_PROGRESS_BAR_STEPS))
        files = {'upload_file': open(filename, 'rb')}
        values = {'email': author, 'assignment': assignment, "debug": log, "guest": guest}
        try:
            r = requests.post(base_url + "/Notebook/submit", files=files, data=values)
            if (str(r.content, 'utf-8', 'ignore')[0] == "Y"):

                display(HTML("""<div class="alert alert-block alert-success">
        <b>Upload successful!</b> You can view your submitted notebook on """ + '<a target="_blank" href="https://nbviewer.jupyter.org/urls/' + base_url.replace(
                    "https://", "").replace("http://", "") + "/uploads/" + str(r.content, 'utf-8', 'ignore')[1:] + '"' + """ class="alert-link"> nbviewer.</a>
        </div>"""))
                display(Javascript(skins.JS_PROGRESS_BAR_FINAL))

                return True
            else:
                display(HTML(skins.HTML_UPLOAD_ERROR_CUSTOM_START + str(r.content, 'utf-8',
                                                                        'ignore') + skins.HTML_UPLOAD_ERROR_CUSTOM_END))
                display(Javascript(skins.JS_PROGRESS_BAR_DANGER))
                return False
        except ConnectionError:
            display(HTML(skins.HTML_MESSAGE_CONNECTION_FAILED))
            display(Javascript(skins.JS_PROGRESS_BAR_DANGER))
            return False
        except:
            display(HTML(skins.HTML_MESSAGE_CONNECTION_FAILED))
            display(Javascript(skins.JS_PROGRESS_BAR_DANGER))
            return False


def send_group_workbook(assignment=None, emails=[], skip_email_check = False):
    """

    :param assignment:
    :return:
    """
    import re, json, base64
    global ready
    global base_url

    # Check if valid emails are provided
    emails_new = []
    for email in emails:
        if email != "":
            emails_new.append(email)
    emails=emails_new


    if (len(emails)==0):
        print("Please enter your email and run this code again.")
        return False
    if (skip_email_check == False):
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
        for i in range(len(emails)):
            if not EMAIL_REGEX.match(emails[i]):
                print(emails[i], "is not a valid email. If needed edit email and run this code again.")

    # Encode emails for easy transfer
    emails_json = json.dumps(emails)
    emails_base64 = base64.b64encode(emails_json.encode("ascii"))

    try:
        from IPython.display import display, Javascript, HTML, IFrame
        display(HTML("<b>Preparing submission</b>"))
    except ImportError:
        print("Failed to load IPython library. Is IPython installed?")

    try:
        import uuid
        rand_code = str(uuid.uuid4())
    except ImportError:
        print("Failed to load uuid library. Using rand() instead.")
        import random
        rand_code = random.randrange(1, 99999999999999)

    # Prepare json code for submission
    js_submission_code = """
    var xhttp = new XMLHttpRequest();
    var notebook_url = window.location.href;
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {    
        //alert(this.responseText);
        }
    };
    xhttp.open("POST", "https://sss-data.minerva.community/ForumCode/submit/""" + str(assignment) + """",true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("rand=""" + str(
        rand_code) + '&url=".concat(btoa(notebook_url),"&data=",notebook_url,"&emails=","' + str(emails_base64, 'utf-8') + '"));'
    display(Javascript(js_submission_code))

    # Use UUID to check if submission was successful
    import requests
    time.sleep(5)
    r = requests.get(base_url + "/ForumCode/check/" + str(assignment) + "/" + str(rand_code))
    if (str(r.content, 'utf-8', 'ignore')[0] == "Y"):
        print(str(r.content, 'utf-8', 'ignore')[1:])
        display(HTML("<b>Notebook Submitted Successfully</b>"))
    else:
        time.sleep(10)
        r = requests.get(base_url + "/ForumCode/check/" + str(assignment) + "/" + str(rand_code))
        if (str(r.content, 'utf-8', 'ignore')[0] == "Y"):
            print(str(r.content, 'utf-8', 'ignore')[1:])
            display(HTML("<b>Notebook Submitted Successfully</b>"))
        else:
            print("Submission Failed, Please try again in a few seconds or contact PT!")
            return False
    return True

def send_grades(assignment=None, emails=[], grades=[], skip_email_check = False):
    """

    :param assignment:
    :return:
    """
    import re, json, base64,requests
    global ready
    global base_url

    # Check if valid emails are provided
    if (len(emails)==0):
        print("Please enter your email and run this code again.")
        raise ValueError("No email provided: Please enter your email and run this code again.");

    grades_new = []
    for grade in grades:
        if grade != None:
            grades_new.append(grade)
        else:
            grades_new.append(" ")
    grades = grades_new
    if (len(grades)==0):
        print("List of grades is empty. Did you run autograding cell?")
        raise ValueError("No grades provided! List of grades is empty. Did you run autograding cell?");

    if (skip_email_check == False):
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
        for i in range(len(emails)):
            if not EMAIL_REGEX.match(emails[i]):
                print(emails[i], "is not a valid email (see variable email"+str(i+1)+"). If needed edit email and run this code again.")

    # Encode emails for easy transfer
    emails_json = json.dumps(emails)
    emails_base64 = base64.b64encode(emails_json.encode("ascii"))

    # Encode emails for easy transfer
    grades_json = json.dumps(grades)
    grades_base64 = base64.b64encode(grades_json.encode("ascii"))

    import requests
    values = {'email': emails_base64, 'assignment': assignment, "grades": grades_base64}
    try:
        r = requests.post(base_url + "/ForumCode/grades", data=values)
        if (str(r.content, 'utf-8', 'ignore')[0] == "Y"):
            return True
        else:
            print(str(r.content, 'utf-8', 'ignore'))
            return False
    except:
        print("Connection Failed")
        return False
    return True


def send_grades_js(assignment=None, grades=[]):
    """

    :param assignment:
    :return:
    """
    import json, base64
    global ready
    global base_url

    # Check if valid grades are provided
    if (len(grades)==0):
        print("List of grades is empty. Did you run autograding cell?")
        raise ValueError("No grades provided! List of grades is empty. Did you run autograding cell?");

    # Encode grades for easy transfer
    grades_json = json.dumps(grades);
    grades_base64 = base64.b64encode(grades_json.encode("ascii"))

    try:
        from IPython.display import display, Javascript, HTML, IFrame
        display(HTML("<b>Preparing submission</b>"))
    except ImportError:
        print("Failed to load IPython library. Is IPython installed?")

    # Prepare json code for submission
    js_submission_code = """
    var xhttp = new XMLHttpRequest();
    var notebook_url = window.location.href;
    xhttp.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {    
        //alert(this.responseText);
        }
    };
    xhttp.open("POST", "https://sss-data.minerva.community/ForumCode/grades_js/""" + str(assignment) + """",true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("rand=""" + str(
        rand_code) + '&url=".concat(btoa(notebook_url),"&data=",notebook_url,"&grades=","' + str(grades_base64,'utf-8') + '"));'
    display(Javascript(js_submission_code))
    return True

def send_notebook(assignment=None, guest=True, websubmit=False, grades=False, makeup=False, emails=[]):
    """

    :param assignment:
    :return:
    """
    global ready
    global base_url
    global log
    import json, base64

    # Encode emails for easy transfer
    emails_json = json.dumps(emails)
    emails_base64 = base64.b64encode(emails_json.encode("ascii"))

    # Encode emails for easy transfer
    grades_json = json.dumps(grades)
    grades_base64 = base64.b64encode(grades_json.encode("ascii"))

    if (not ready) and not guest:
        print("You are not logged in!")
        print("Please run miupload.login_gui()")
        return False
    else:
        if guest:
            author = emails_base64
        else:
            author = base64.b64encode(json.dumps([cfg.email]).encode("ascii"))



    try:
        from IPython.display import display, Javascript, HTML, IFrame
        display(Javascript("IPython.notebook.save_notebook()"),
                include=['application/javascript'])
        display(HTML(skins.HTML_PROGRESS_BAR))
    except ImportError:
        print("Autosaving failed. Please make sure to save your notebook before submitting notebook.")
    else:
        print("Autosaving notebook...")  # save notebook before reading of file

    def progress_bar_step(name, step=10):
        try:
            display(Javascript("""
                var current_progress = parseInt($("#submitprogress").attr("aria-valuenow"));
                  current_progress += """ + str(step) + """;  
                  $("#""" + name + """")
                  .css("width", current_progress + "%")
                  .attr("aria-valuenow", current_progress)
                  .text(current_progress + "% Complete");
                  """))
            return True
        except:
            return False

    progress_bar_step("submitprogress", step=5)

    display(Javascript("IPython.notebook.save_notebook()"),
            include=['application/javascript'])
    display(Javascript(skins.JS_PROGRESS_BAR_INIT))
    time.sleep(5)

    print("Notebook saved.")
    print("Preparing .ipynb upload")
    # Get filename of notebook for uploading
    # Source: https://github.com/jupyter/notebook/issues/1000
    import json
    import os.path
    import re
    import ipykernel
    import requests

    # Alternative that works for both Python 2 and 3:
    from requests.compat import urljoin

    try:  # Python 3 (see Edit2 below for why this may not work in Python 2)
        from notebook.notebookapp import list_running_servers
    except ImportError:  # Python 2
        import warnings
        from IPython.utils.shimmodule import ShimWarning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=ShimWarning)
            from IPython.html.notebookapp import list_running_servers

    def get_notebook_name():
        global log
        """
        Return the full path of the jupyter notebook.
        """
        kernel_id = re.search('kernel-(.*).json',
                              ipykernel.connect.get_connection_file()).group(1)
        servers = list_running_servers()
        log += "[DEBUG] Getting Server List\n"
        log += "[DEBUG] Servers:" + repr(servers) + "\n"
        for ss in servers:
            log += "[DEBUG] URL:" + urljoin(ss['url'], 'api/sessions') + "\n"
            log += "[DEBUG] Params:" + str(repr(ss.get('token', ''))) + "\n"
            response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                    params={'token': ss.get('token', '')})
            log += "[DEBUG] Response:" + response.text + "\n"
            for nn in json.loads(response.text):
                try:
                    log += "[DEBUG] Kernel:" + str(repr(nn)) + "\n"
                    if nn['kernel']['id'] == kernel_id:
                        relative_path = nn['notebook']['path']
                        return os.path.join(ss['notebook_dir'], relative_path)
                except:
                    log += "[DEBUG] Failed to get kernel:" + repr(nn) + "\n"

                    # display(HTML(skins.HTML_KERNEL_API_CALL_FAILED))
                    # relative_path = input("path/filename.ipynb: ")
                    return False;

    if websubmit:
        filename = False;
    else:
        filename = get_notebook_name()

    if (filename == False):
        if guest:
            create = 1
        else:
            create = 0
        src = base_url + "/GUI/manual_upload/" + assignment + "/" + urllib.parse.quote(author) + "?guest=" + str(create)
        if not websubmit:
            display(HTML(skins.HTML_MESSAGE_INPUT_REQUIRED))
        display(IFrame(src, 600, 200))
    else:
        display(Javascript(skins.JS_PROGRESS_BAR_FAST_STEP))
        display(Javascript(skins.JS_PROGRESS_BAR_STEPS))
        files = {'upload_file': open(filename, 'rb')}
        values = {'emails': author, 'assignment': assignment, "debug": log, "guest": guest, "grades": grades_base64, "makeup": makeup}
        try:
            r = requests.post(base_url + "/ForumCode/notebook", files=files, data=values)
            if (str(r.content, 'utf-8', 'ignore')[0] == "Y"):

                display(HTML("""<div class="alert alert-block alert-success">
        <b>Upload successful!</b>
        </div>"""))
                display(Javascript(skins.JS_PROGRESS_BAR_FINAL))

                return True
            else:
                display(HTML(skins.HTML_UPLOAD_ERROR_CUSTOM_START + str(r.content, 'utf-8',
                                                                        'ignore') + skins.HTML_UPLOAD_ERROR_CUSTOM_END))
                display(Javascript(skins.JS_PROGRESS_BAR_DANGER))
                return False
        except ConnectionError:
            display(HTML(skins.HTML_MESSAGE_CONNECTION_FAILED))
            display(Javascript(skins.JS_PROGRESS_BAR_DANGER))
            return False
        except:
            display(HTML(skins.HTML_MESSAGE_CONNECTION_FAILED))
            display(Javascript(skins.JS_PROGRESS_BAR_DANGER))
            return False


def nbgrader_download(assignment, token=None, group=None, filename=None, folder=None):
    import os
    import requests
    import json
    if (filename == None):
        filename = assignment
    if (folder == None):
        folder = assignment

    if (token != None):
        pass
    else:
        token = cfg.psw
    print("Contacting data server")
    try:
        if group == None:
            r = requests.get(base_url + "/Notebook/download_list/" + str(token) + "/" + str(assignment))
        else:
            r = requests.get(
                base_url + "/Notebook/download_list/" + str(token) + "/" + str(assignment) + "/" + str(group))
    except:
        print("Failed to connect with the server, please check your internet connection")
        return False
    print("Parsing received data")
    try:
        data = json.loads(r.content)
    except:
        print("Failed to parse received data")
        print("RAW DATA:", data)
        return False
    print("Found ", len(data), "submitted notebooks.")
    print("Preparing required folder structure")

    # create submitted folder
    if not os.path.exists(os.getcwd() + "/submitted"):
        os.makedirs(os.getcwd() + "/submitted")
    for row in data:
        # create user folder
        if not os.path.exists(os.getcwd() + "/submitted/" + row["u_name"].replace(" ", "_")):
            os.makedirs(os.getcwd() + "/submitted/" + row["u_name"].replace(" ", "_"))
        # create assignment folder
        if not os.path.exists(os.getcwd() + "/submitted/" + row["u_name"].replace(" ", "_") + "/" + folder):
            os.makedirs(os.getcwd() + "/submitted/" + row["u_name"].replace(" ", "_") + "/" + folder)

        # download file
        url = base_url + "/uploads/" + row["s_filename"]
        r = requests.get(url, allow_redirects=True)
        open(os.getcwd() + "/submitted/" + row["u_name"].replace(" ", "_") + "/" + folder + "/" + filename + ".ipynb",
             'wb').write(r.content)

        print("Assignment saved successfully")

    print("Notebook are ready to be graded")
