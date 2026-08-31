import subprocess
import webbrowser


ALLOWED_APPLICATIONS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
}


def launch_application(application):
    """
    Launch a permitted Windows application.
    """

    application = application.lower().strip()

    if application not in ALLOWED_APPLICATIONS:
        return f"I can't launch '{application}' yet."

    try:

        subprocess.Popen(
            ALLOWED_APPLICATIONS[application]
        )

        return f"Launched {application}."

    except Exception as error:

        return f"Failed to launch {application}: {error}"


def open_website(url):
    """
    Open a website using the default browser.
    """

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:

        webbrowser.open(url)

        return f"Opened {url}."

    except Exception as error:

        return f"Failed to open website: {error}"