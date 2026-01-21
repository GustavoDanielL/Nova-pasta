"""Wrapper to run the FastAPI app with uvicorn in a way that is easy to
package with PyInstaller (entrypoint script).
"""
import uvicorn


def main():
    # Import here to avoid PyInstaller analysis issues
    uvicorn.run("backend.api:app", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
