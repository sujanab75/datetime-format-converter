from flask import Flask, render_template, request
from datetime import datetime
import re

app = Flask(__name__)

# Set of valid strftime format codes
VALID_CODES = {
    '%a', '%A', '%w', '%d', '%b', '%B', '%m', '%y', '%Y', '%H', '%I', '%p',
    '%M', '%S', '%f', '%z', '%Z', '%j', '%U', '%W', '%c', '%x', '%X', '%%'
}


# Function to find invalid codes
def has_invalid_codes(fmt):
    codes = set(re.findall(r'%[a-zA-Z%]', fmt))
    return codes - VALID_CODES


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        fmt = request.form["format"]
        now = datetime.now()

        # Check for invalid format codes first
        invalid = has_invalid_codes(fmt)
        if invalid:
            # Try to show example with valid codes only
            valid_codes = set(re.findall(r'%[a-zA-Z%]', fmt)) & VALID_CODES
            if valid_codes:
                # Create a format string with only valid codes for demonstration
                try:
                    # Show what valid codes would produce
                    sample_valid_fmt = ' '.join(valid_codes)
                    valid_example = now.strftime(sample_valid_fmt)
                    result = f"Invalid format code(s): {', '.join(sorted(invalid))}. Valid codes in your input would produce: {valid_example}"
                except:
                    result = f"Invalid format code(s): {', '.join(sorted(invalid))}"
            else:
                result = f"Invalid format code(s): {', '.join(sorted(invalid))}"
        else:
            try:
                example = now.strftime(fmt)
                result = f"Example: {example}"
            except Exception as e:
                result = f"Error: {str(e)}"

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
