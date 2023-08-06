import pathlib

path = pathlib.Path(".", "settings.py")
if not path.exists():
    with open("settings.py", "w") as f:
        f.write("""
MIDDLEWARES = {
    "REQUESTS_MIDDLEWARE": [
    ],
    "PRODUCT_URL_MIDDLEWARE": [
    ]
}
        """.strip())
