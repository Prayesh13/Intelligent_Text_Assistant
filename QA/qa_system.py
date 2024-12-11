from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
# from QA.database import insert_question_answer

# Load the saved model and tokenizer
# model_path = r"D:\Model-scet\Model\QA_Model"  # Ensure this path matches where you saved the model
# model = AutoModelForQuestionAnswering.from_pretrained(model_path)
# tokenizer = AutoTokenizer.from_pretrained(model_path)
#
# # Initialize the question-answering pipeline with the saved model
# qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
# Initialize the question-answering pipeline with the saved model
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

def process_questions(questions_input, context):
    """Process questions and return their answers."""
    answers = []  # Store answers for the questions

    # Limit to 5 questions
    for question in questions_input[:5]:
        question = question.strip()
        if question:  # Only process non-empty questions
            result = qa_pipeline(question=question, context=context,
                                 max_answer_len=100,  # Adjust this to increase answer length
                                 min_answer_len=50,  # Adjust this to set a minimum length
                                 max_seq_len=512,  # Ensure the context is fully considered
                                 top_k=1)
            answers.append((question, result['answer']))  # Store tuple of question and answer

            # Insert question and answer into the database
            # insert_question_answer(question, result['answer'])

    return answers
