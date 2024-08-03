from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# Configure the API key
API_KEY = 'AIzaSyDLc3ztQij66SFI3YsHtsH3s5TYPJ3VaKE'
genai.configure(api_key=API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to generate content
def create_feedback_classification(feedback):
    prompt = f'''
    you are a sentiment classification model. refer the below example and classify feedback into "p" or "n" category. return only the category in output.
    ###
    feedback: what a lovely product
    sentiment: p
    ###
    feedback: what a worst product
    sentiment: n
    ###
    feedback: {feedback}
    sentiment:
    '''
    response = model.generate_content(prompt, generation_config={"temperature": 0.5})
    return response.text.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_content = ''
    if request.method == 'POST':
        feedback = request.form['prompt']
        if feedback:
            generated_content = create_feedback_classification(feedback)
    return render_template('index.html', generated_content=generated_content)

if __name__ == '__main__':
    app.run(debug=True)
