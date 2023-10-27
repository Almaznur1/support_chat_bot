from google.cloud import dialogflow
import json

from config import project_id


def create_intent(project_id, display_name,
                  training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print(f"Intent created: {response}")


def main():
    with open('questions.json', 'r', encoding='utf-8') as file:
        questions_json = file.read()

    questions = json.loads(questions_json)

    for question in questions:

        create_intent(
            project_id=project_id,
            display_name=question,
            training_phrases_parts=questions[question]['questions'],
            message_texts=questions[question]['answer']
        )


if __name__ == '__main__':
    main()
