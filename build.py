import execjs
import yaml
import re
import os
import hashlib

html_form = """
                <form id="answerForm" class="mt-3">
                    <div class="input-group mb-3">
                        <input type="text" class="form-control" id="inputText" placeholder="Ditt svar her" required>
                        <button class="btn btn-primary" type="submit">Send</button>
                    </div>
                </form>
"""

class JSFuckObfuscator:
    _jsf_compiled = None

    @staticmethod
    def _load_jsfuck():
        """Private method to load and compile the JSFuck code once"""
        with open("jsfuck.js", "r") as f:
            jsf_code = f.read()
        JSFuckObfuscator._jsf_compiled = execjs.compile(jsf_code)

    @staticmethod
    def obfuscate(code):
        """Obfuscate the given JavaScript code using JSFuck"""
        if JSFuckObfuscator._jsf_compiled is None:
            JSFuckObfuscator._load_jsfuck()
        return JSFuckObfuscator._jsf_compiled.call("JSFuck", code, "1")

# Load the template and config for the challenges
with open("templates/challenge.html", "r") as template:
    template = template.read()
    
with open("challenges.yaml", "r") as challenges:
    challenges = yaml.safe_load(challenges)

# Create the docs directory if it doesnt exist
os.makedirs("docs", exist_ok=True) 


# Add path to first challenge in index.html for auto redirect
if challenges:
    first_challenge_name = challenges[0].get("name")
    with open("templates/index.html", "r") as template_file:
        content = template_file.read().replace("{FIRST_CHALL}", first_challenge_name)
    
    with open("docs/index.html", "w") as output_file:
        output_file.write(content)


for count, challenge in enumerate(challenges):
    # Extract challenge config values
    name = challenge.get("name")
    description = challenge.get("description")
    md5_answer = hashlib.md5(str(challenge.get("answer")).upper().encode()).hexdigest()
    is_final = challenge.get("is_final")

    # Fetch the name of the next challenge dynamically
    if count < len(challenges) - 1:
        next_challenge = f"{challenges[count + 1].get("name")}.html"
    else:
        next_challenge = None
        
    # Format the description into paragraphs. Kinda hacky, but it works
    description = description.strip().split("\n")
    formatted_description = []
    for line in description:
        if classes := re.findall(r"{{([a-z-\s]+)}}", line):
            classes = classes[0]
            line = line.replace(f"{{{{{classes}}}}}", "")
            formatted_description.append(f"<p class=\"{classes}\">{line}</p>")
        else:
            formatted_description.append(f"<p>{line}</p>")
            
    config = f"window.challConfig = {{ h: \"{md5_answer}\", n: \"{next_challenge}\"}}" 
    
    # Obfuscate the config using JSFuck. This decreases the ability to cheat
    jsf_config = JSFuckObfuscator.obfuscate(config)
    
    # Replace placeholders in the template
    challenge_page = (
        template
        .replace("{DESCRIPTION}", "\n".join(formatted_description))
        .replace("{CONFIG}", jsf_config)
        .replace("{CHALL_NUMBER}", str(count + 1))
    )
    
    # Answer submission form is not needed for the last challenge
    challenge_page = challenge_page.replace("{FORM}", html_form if next_challenge else "")
    

    with open(f"docs/{name}.html", "w") as f:
        f.write(challenge_page)
