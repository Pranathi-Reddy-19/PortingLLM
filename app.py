
from flask import Flask, request, jsonify
        from flask_cors import CORS
        import subprocess
        import re
        import json

        app = Flask(__name__)
        CORS(app)

        LLAMA_CLI_PATH = /var/www/llama.cpp/build/bin/llama-cli
        MODEL_PATH = /var/www/llama.cpp/models/orca_mini_3b-Q5_K_S.gguf

        SYSTEM_PROMPT = (
            "You are an assistant who extracts calendar events from user messages.\n"
            "If the user mentions anything like 'meeting tomorrow at 2 PM' or similar, "
            "you must return a JSON like this:\n"
            "{ \"event\": \"meeting\", \"date\": \"YYYY-MM-DD\", \"time\": \"14:00\" }\n"
            "Support words like 'afternoon', 'forenoon', 'yesterday', 'tomorrow', etc.\n"
            "If there is no calendar-related info, respond normally as an assistant.\n"
        )

        @app.route('/query', methods=['POST'])
        def query():
            data = request.get_json()
            prompt = data.get("prompt", "")

            if not prompt:
                return jsonify({"error": "Prompt missing"}), 400

            try:
                full_prompt = f"""### System:
        {SYSTEM_PROMPT}

        ### User:
        {prompt}

        ### Assistant:
        """

                result = subprocess.run(
                    [
                        LLAMA_CLI_PATH,
                        "-m", MODEL_PATH,
                        "-p", full_prompt,
                        "--n-predict", "64",
                        "--top-k", "20",
                        "--temp", "0.7"
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=180
                )

                raw_output = result.stdout.strip()

                # Extract only the assistant's reply
                match = re.search(r"### Assistant:\s*(.*)", raw_output, re.DOTALL)
                if match:
                    assistant_output = match.group(1).strip()
                else:
                    assistant_output = "No valid assistant response found."

                # Remove [end of text], <|endoftext|>, or other endings
                assistant_output = re.sub(r"(\[end of text\]|<\|endoftext\|>|end of text)", "", assistant_output, flags=re.IGNORECASE).strip()

                # Try to parse JSON response if possible
                try:
                    json_output = json.loads(assistant_output)
                    return jsonify(json_output)
                except json.JSONDecodeError:
                    # Return as plain string if not valid JSON
                    return jsonify({"response": assistant_output})

            except subprocess.TimeoutExpired:
                return jsonify({"error": "Model timed out"}), 500
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        if __name__ == '__main__':
            app.run(host='0.0.0.0', port=5000)
