from datetime import datetime
from pathlib import Path
import os
import platform
import shutil
import subprocess
import webbrowser

import pyautogui
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from tools.agent_controller import run_task


# ==========================================
# ETERNITY API
# ==========================================

app = FastAPI(
    title="ETERNITY API",
    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# REQUEST MODELS
# ==========================================

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    status: str


class QuickToolRequest(BaseModel):
    tool: str


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():

    return {
        "name": "ETERNITY",
        "status": "online",
        "version": "1.0.0"
    }


# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "ETERNITY API"
    }


# ==========================================
# NORMAL AI CHAT
# ==========================================

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    user_message = request.message.strip()

    if not user_message:

        return ChatResponse(
            response="Please enter a message.",
            status="error"
        )

    try:

        response = run_task(
            user_message
        )

        return ChatResponse(
            response=str(response),
            status="completed"
        )

    except Exception as error:

        return ChatResponse(
            response=f"Error: {error}",
            status="error"
        )


# ==========================================
# QUICK TOOLS
# ==========================================

@app.post(
    "/quick-tool",
    response_model=ChatResponse
)
def quick_tool(request: QuickToolRequest):

    tool = request.tool.lower().strip()

    try:

        # ==================================
        # NOTEPAD
        # ==================================

        if tool == "notepad":

            subprocess.Popen(
                ["notepad.exe"]
            )

            return ChatResponse(
                response="Notepad opened successfully.",
                status="completed"
            )


        # ==================================
        # CALCULATOR
        # ==================================

        if tool == "calculator":

            subprocess.Popen(
                ["calc.exe"]
            )

            return ChatResponse(
                response="Calculator opened successfully.",
                status="completed"
            )


        # ==================================
        # FILE EXPLORER
        # ==================================

        if tool == "file_explorer":

            os.startfile(
                os.path.expanduser("~")
            )

            return ChatResponse(
                response="File Explorer opened successfully.",
                status="completed"
            )


        # ==================================
        # SCREENSHOT
        # ==================================

        if tool == "screenshot":

            screenshot_folder = (
                Path(__file__).resolve().parent
                / "screenshots"
            )

            screenshot_folder.mkdir(
                exist_ok=True
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            screenshot_path = (
                screenshot_folder
                / f"eternity_{timestamp}.png"
            )

            image = pyautogui.screenshot()

            image.save(
                screenshot_path
            )

            return ChatResponse(
                response=(
                    "Screenshot captured successfully.\n"
                    f"Saved to: {screenshot_path}"
                ),
                status="completed"
            )


        # ==================================
        # SYSTEM INFORMATION
        # ==================================

        if tool == "system_info":

            system = platform.system()
            release = platform.release()
            version = platform.version()
            machine = platform.machine()
            processor = platform.processor()
            hostname = platform.node()
            cpu_count = os.cpu_count()

            disk = shutil.disk_usage(
                Path.home()
            )

            total_disk_gb = (
                disk.total / (1024 ** 3)
            )

            free_disk_gb = (
                disk.free / (1024 ** 3)
            )

            response = (
                "System Information\n\n"

                f"Operating System: "
                f"{system}\n"

                f"Version: "
                f"{release}\n"

                f"Build: "
                f"{version}\n"

                f"Machine: "
                f"{machine}\n"

                f"Processor: "
                f"{processor or 'Unknown'}\n"

                f"CPU Cores: "
                f"{cpu_count}\n"

                f"Computer Name: "
                f"{hostname}\n"

                f"Disk Space: "
                f"{free_disk_gb:.1f} GB free / "
                f"{total_disk_gb:.1f} GB total"
            )

            return ChatResponse(
                response=response,
                status="completed"
            )


        # ==================================
        # WEB SEARCH
        # ==================================

        if tool == "web_search":

            webbrowser.open(
                "https://www.google.com"
            )

            return ChatResponse(
                response="Web Search opened successfully.",
                status="completed"
            )


        # ==================================
        # UNKNOWN TOOL
        # ==================================

        return ChatResponse(
            response=f"Unknown Quick Tool: {tool}",
            status="error"
        )


    except Exception as error:

        return ChatResponse(
            response=f"Quick Tool error: {error}",
            status="error"
        )